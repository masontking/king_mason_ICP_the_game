import pygame as pg
from pygame.sprite import Sprite
from settings import *
from utils import *

from os import path

vec = pg.math.Vector2

def collide_hit_rect(one, two):
    return one.hit_rect.colliderect(two.rect)

# if we collide with walls, this function runs.
def collide_with_walls(sprite, group, dir):
    if dir == "x":
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            # checks to see if collision is from the left
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
            # checks for collision from the right
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
    if dir == "y":
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            # checks to see if collision is from the top
            if hits[0].rect.centery > sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
            # checks for collision from the bottom
            if hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y
class Player(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.game = game
        self.spritesheet = Spritesheet(path.join(self.game.img_dir, "sprite_sheet.png"))
        self.image = pg.Surface((TILESIZE,TILESIZE))
        self.image = self.spritesheet.get_image(0,0,TILESIZE,TILESIZE)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.hit_rect = PLAYER_HIT_RECT
        self.vel = vec(0,0)
        self.pos = vec(x*TILESIZE,y*TILESIZE)
    def get_keys(self):
        # reset v to 0
        # get events based on keys
        # change vel baesd on keys
        self.vel = vec(0,0)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]: # if a or left arrow is pressed, the player moves left.
            self.vel.x = -PLAYER_SPEED
            self.vx = -PLAYER_SPEED
        if keys[pg.K_RIGHT] or keys[pg.K_d]: # if d or right arrow is pressed, the player moves right.
            self.vel.x = PLAYER_SPEED
            self.vx = PLAYER_SPEED
        if keys[pg.K_UP] or keys[pg.K_w]: # if w or up arrow is pressed, the player moves up.
            self.vel.y = -PLAYER_SPEED
            self.vy = -PLAYER_SPEED
        if keys[pg.K_DOWN] or keys[pg.K_s]: # if s or down arrow is pressed, the player moves down.
            self.vel.y = PLAYER_SPEED
            self.vy = PLAYER_SPEED
        
        if self.vel.x != 0 and self.vel.y != 0:
            self.vel *= 0.7071
    def update(self):
        self.get_keys()
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.all_walls,'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.all_walls,'y')
        self.rect.center = self.hit_rect.center
        

class Wall(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_walls
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE,TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0,0
        self.x = x*TILESIZE
        self.y = y*TILESIZE
        self.rect.x = self.x
        self.rect.y = self.y
        print("initiated wall")
        print(self.rect.x)
        print(self.rect.y)

class Mob(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_mobs
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE,TILESIZE))
        self.image.fill(RED)
        self.speed = 1
        self.rect = self.image.get_rect()
        self.vx, self.vy = 200,200
        self.x = x*TILESIZE
        self.y = y*TILESIZE
        self.rect.x = self.x
        self.rect.y = self.y
        print("initiated mob")
        print(self.rect.x)
        print(self.rect.y)
    
    def update(self):
        self.x += self.vx * self.game.dt * self.speed
        self.rect.x = self.x
        self.y += self.vy * self.game.dt * self.speed
        self.rect.y = self.y
        if self.x > WIDTH - TILESIZE or self.x < 0:
            self.vx *= -1
        if self.y > HEIGHT - TILESIZE or self.y < 0:
            self.vy *= -1

# this file was created by MASON KING
# code inspired by Chris Bradfield who was inspired by Notch

# import everything needed to run the code
import pygame as pg
from os import path
from settings import *
from sprites import *
from utils import *

class Game:
    def __init__(self):
        pg.init()   # initiate pygame
        pg.mixer.init()   # initiate audio within pygame
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        print("initiated game")
        pg.display.set_caption(TITLE) # sets the name of the window to TITLE
        self.running = True
        self.playing = True
        self.clock = pg.time.Clock()

    def load_data(self, map):
        self.game_dir = path.dirname(__file__) # game directory 
        self.img_dir = path.join(self.game_dir, 'images') # image directory
        self.snd_dir = path.join(self.game_dir, 'audio') # audio directory
        self.map = Map(path.join(self.game_dir, map)) # tilemap directory

    def new(self):
        self.load_data('level1.txt')
        self.all_sprites = pg.sprite.Group() # creates a group where the sprites data will coincide
        self.all_walls = pg.sprite.Group() # creates a group where the wall sprites data will coincide
        self.all_mobs = pg.sprite.Group() # creates a group where the enemy sprites data will coincide
        self.mob = Mob(self,5,5)
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row)
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == 'P':
                    Player(self, col, row)
    # if the game is running, do stuff
    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000 # dt = delta time
            self.events()
            self.update()
            self.draw()
    # checks if you've closed the window
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
    # just update the sprites, man
    def update(self):
        self.all_sprites.update()

    def draw(self):
        self.screen.fill(BGCOLOR) # change the color of the background
        self.all_sprites.draw(self.screen) # fill the bg with the color of choosing
        pg.display.flip()

# run the game :D
if __name__ == "__main__":
    g = Game()
while g.running:
    g.new()
    g.run()
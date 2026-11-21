
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
        self.text_queue = []
        self.units = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

    def load_data(self, map):
        self.game_dir = path.dirname(__file__) # game directory 
        self.game_save_file = path.join(self.game_dir, "levelnum.txt")
        self.img_dir = path.join(self.game_dir, 'images') # image directory
        # for sound handling
        self.snd_dir = path.join(self.game_dir, 'audio') # audio directory
        self.coin_snd = pg.mixer.Sound(path.join(self.snd_dir, "coin.wav"))
        self.map = Map(path.join(self.game_dir, map)) # tilemap directory
        try:
            with open(self.game_save_file, "x", encoding="utf-8") as c:
                c.write("hell yeah")
            print("file created")
        except FileExistsError:
            pass
        with open(self.game_save_file, "r") as c:
            try:
                self.level = int(c.read())
            except:
                pass
            

    def new(self):
        self.load_data('map.txt')
        self.all_sprites = pg.sprite.Group() # creates a group where the sprites data will coincide
        self.all_walls = pg.sprite.Group() # creates a group where the wall sprites data will coincide
        self.all_mobs = pg.sprite.Group() # creates a group where the enemy sprites data will coincide
        self.all_coins = pg.sprite.Group() # creates a group where the coin sprites data will coincide
        self.all_particles = pg.sprite.Group() # creates a group where particle data will coincide
        self.all_buildings = pg.sprite.Group() # creates a group where building data will coincide
        self.all_barracksmenu = pg.sprite.Group() # you get the idea at this point.
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row, BGCOLOR, False)
                if tile == '2':
                    Wall(self, col, row, False, 'house')
                if tile == '3':
                    Building(self, col, row, 'barracks')
                if tile == 'p':
                    BGSprite(self, col, row, PATHCOLOR, False)
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == 'C':
                    Coin(self, col, row)
                if tile == 'E':
                    self.mob = Mob(self, col, row)
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == 'P':
                    self.player = Player(self, col, row)
        pg.mixer.music.load(path.join(self.snd_dir, "bgmusic.mp3"))
        pg.mixer.music.play(loops=-1)
    # if the game is running, do stuff
    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000 # dt = delta time
            self.events()
            self.update()
            self.draw()
    def events(self):
        for event in pg.event.get():
            # checks if you've closed the window or the game has quit
            if event.type == pg.QUIT:
                with open(path.join(self.game_dir, self.game_save_file), "w") as c:
                    c.write(str(self.level))
                if self.playing:
                    self.playing = False
                self.running = False
                # checking for exceptions to know whether or not the save file code is working


    def draw(self):
        self.screen.fill(BGCOLOR) # change the color of the background
        self.all_sprites.draw(self.screen) # puts the sprites on the screen
        self.draw_text("FPS: " + str(floor(1/self.dt)), 24, WHITE, WIDTH-50, 0)
        for i in self.text_queue: # goes through a text queue created by the sprites
            self.draw_text(i[0], i[1], i[2], i[3], i[4])
        self.text_queue = []
        pg.display.flip()
    
    # draws text (pretty self explanitory)      
    def draw_text(self, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        self.screen.blit(text_surface, text_rect)
    
    # just update the sprites, man
    def update(self):
        self.all_sprites.update()

# run the game :D
if __name__ == "__main__":
    g = Game()
while g.running:
    g.new()
    g.run()
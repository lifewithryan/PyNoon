# PyNoon
import pygame, sys, os
from pygame.locals import *

import random
import time

DIRNAME = os.path.abspath(os.path.dirname(__file__).decode('utf-8'))
RESOURCE_DIR = os.path.join(DIRNAME, '../resources/')
RED = pygame.Color(255, 0, 0)
GREEN  = pygame.Color(0, 255, 0)
BLUE = pygame.Color(0, 0, 255)
WHITE = pygame.Color(255, 255, 255)



class Game(object):
    """
    An object to manage the game
    """
    def __init__(self):
        self.screen = pygame.display.set_mode((1024, 768))
        self.game_clock = pygame.time.Clock()
        pygame.display.set_caption("PyNoon")
        self.cowboy = pygame.image.load(RESOURCE_DIR + 'cowboy.png')
        self.gunshot = None
        self.got_me = None
        self.draw_em = None
        self.bang = None
        self.whistle = None
        self.laugh = None

    
    #def load_sound(self, name):
    #    """
    #    completely stolen from a tutorial here:
    #    http://pygame.org/docs/tut/chimp/ChimpLineByLine.html
    #    """
    #    class NoneSound:
    #        def play(self): pass
    #    
    #    if not pygame.mixer:
    #        return NoneSound()
    #    
    #    fullname = os.path.join('data', name)
#
    #    try:
    #        sound = pygame.mixer.Sound(RESOURCE_DIR + fullname)
    #    except pygame.error, message:
    #        print 'Cannot load sound:', wav
    #        raise SystemExit, message
    #    return sound

    def load_sound(self, name):
        fullname = os.path.join('data', name)
        try:
            sound = pygame.mixer.Sound(fullname)
        except pygame.error, message:
            print message
            print 'Cannot load sound:', wav
            raise SystemExit, message
        return sound

    def screen_color(self, color):
        self.screen.fill(color)

    def reset(self):
        self.screen_color(WHITE)

    def random_pos(self):
        pos = (random.randint(0,540), random.randint(0, 400))
        print pos
        return pos

    def rand_time(self):
        return random.random() * 4

    def start(self):
        # load the sounds first
        print "Loading sounds from " + RESOURCE_DIR
        self.gunshot = self.load_sound(RESOURCE_DIR + 'pow.wav')
        self.got_me = self.load_sound(RESOURCE_DIR + 'got_me.wav')
        self.draw_em = self.load_sound(RESOURCE_DIR + 'draw_em.wav')
        self.bang = self.load_sound(RESOURCE_DIR + 'bang.wav')
        self.whistle = self.load_sound(RESOURCE_DIR + 'whistle.wav')
        self.laugh = self.load_sound(RESOURCE_DIR + 'laugh.wav')
        self.reset()
        return self

    def show_cowboy(self):
        self.reset()
        time.sleep(self.rand_time())
        self.draw_em.play() 
        self.screen.blit(self.cowboy, self.random_pos())


    def hit_target(self, click_pos):
        color = self.screen.get_at(click_pos)
        if color != WHITE:
            return True
        else:
            return False

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
                elif event.type == KEYDOWN:
                    self.show_cowboy()
                elif event.type == MOUSEBUTTONDOWN:
                    self.bang.play()
                    position = event.pos
                    if self.hit_target(position):
                        time.sleep(.5)
                        self.got_me.play()
                        self.screen_color(GREEN)
                        print "Target Hit"
                    else:
                        self.gunshot.play()
                        time.sleep(1)
                        self.laugh.play()
                        self.screen_color(RED)
                        print "Missed me!"

            pygame.display.update()
            self.game_clock.tick(30)

def main():
    game = Game()
    game.start().run()

if __name__ == "__main__":
    main()


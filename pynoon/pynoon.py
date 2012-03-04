# PyNoon
import pygame, sys, os
from pygame.locals import *

import random
import time

DIRNAME = os.path.dirname(__file__)
RESOURCE_DIR = os.path.join(DIRNAME, 'resources/')
RED = pygame.Color(255, 0, 0)
GREEN  = pygame.Color(0, 255, 0)
BLUE = pygame.Color(0, 0, 255)
WHITE = pygame.Color(255, 255, 255)

pygame.init()

class Game(object):
    """
    An object to manage the game
    """
    def __init__(self):
        
        self.screen = pygame.display.set_mode((1024, 768))
        self.game_clock = pygame.time.Clock()
        pygame.display.set_caption("PyNoon")
        # probably shouldn't load the images init...dunno why, but seems like a bad idea? gut check?
        self.cowboy = pygame.image.load(RESOURCE_DIR + 'cowboy.png')
        self.gunshot = pygame.mixer.Sound(RESOURCE_DIR + 'pow.wav')
        self.got_me = pygame.mixer.Sound(RESOURCE_DIR + 'ya_got_me.wav') 
        self.draw_em = pygame.mixer.Sound(RESOURCE_DIR + 'draw.wav') 
        self.bang = pygame.mixer.Sound(RESOURCE_DIR + 'bang.wav') 
        self.whistle = pygame.mixer.Sound(RESOURCE_DIR + 'whistle.wav' )
        self.laugh = pygame.mixer.Sound(RESOURCE_DIR + 'laugh.wav') 

    def screen_color(self, color):
        self.screen.fill(color)

    def reset(self):
        self.screen_color(WHITE)

    def random_pos(self):
        pos = (random.randint(0,540), random.randint(0, 400))
        return pos

    def rand_time(self):
        return random.random() * 4

    def start(self):
        self.whistle.play()
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


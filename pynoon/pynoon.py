"""
 PyNoon is a small python game leveraging PyGame used as a learning project
"""
import random
import time
import sys
import os
import pygame
from pygame.locals import *

DIRNAME = os.path.dirname(__file__)
RESOURCE_DIR = os.path.join(DIRNAME, 'resources/')
RED = pygame.Color(255, 0, 0)
GREEN  = pygame.Color(0, 255, 0)
BLUE = pygame.Color(0, 0, 255)
WHITE = pygame.Color(255, 255, 255)
GUNSLINGER = 30
SHERIFF = 60
WEASEL = 90

pygame.init()

class Cowboy(object):
    """
    The villain in our game
    """
    def __init__(self):
        self.image = pygame.image.load(RESOURCE_DIR + 'cowboy.png')
        self.gunshot = pygame.mixer.sound(RESOURCE_DIR + 'pow.wav')
        self.lose = pygame.mixer.sound(RESOURCE_DIR + 'ya_got_me.wav')
        self.win = pygame.mixer.sound(RESOURCE_DIR + 'laugh.wav')
        self.is_showing = False
        self.is_dead = False

class Player(object):
    """
    The player one type person
    """
    def __init__(self):
        self.gunshot = pygame.mixer.sound(RESOURCE_DIR + 'bang.wav')
        self.is_dead = False

    def death(self):
        """ future home of player death"""

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
        self.beltch = pygame.mixer.Sound(RESOURCE_DIR + 'beltch.wav')
        self.egg = ""
        self.cowboy_is_showing = False
        self.cowboy_is_dead = False
        self.player_is_dead = False
        self.game_tick = 0
        #self.GUNSLINGER = 30 #approx 1 second since game tick is set to 30
        #self.SHERIFF = 60
        #self.WEASEL = 90


    def screen_color(self, color):
        """
        Receives a color for the screen to painted and hides the cowboy
        """
        self.cowboy_is_showing = False #if we're refilling the screen, cowboy is not active
        self.screen.fill(color)

    def reset(self):
        """
        resets the game state
        """
        self.game_tick = 0
        self.cowboy_is_showing = False
        self.cowboy_is_dead = False
        self.player_is_dead = False
        self.screen_color(WHITE)

    def random_pos(self):
        """
        pick a random position for the cowboy in our window
        """
        pos = (random.randint(0,540), random.randint(0, 400))
        return pos

    def rand_time(self):
        """
        wait some amount of time before showing the cowboy
        """
        return random.random() * 4

    def start(self):
        """
        Perhaps this is where I'd prompt for player name
        Read config inputs, maybe show current record of player, etc
        """
        self.whistle.play()
        self.reset()
        return self

    def show_cowboy(self):
        """
        draw the cowboy and get ready to shoot
        """
        self.reset()
        time.sleep(self.rand_time())
        self.draw_em.play()
        self.screen.blit(self.cowboy, self.random_pos())
        self.cowboy_is_showing = True

    def hit_target(self, click_pos):
        """
        detect whether the mouse click was on the cowboy or missed
        """
        color = self.screen.get_at(click_pos)
        if color != WHITE and self.cowboy_is_showing:
            return True
        else:
            return False

    def easter(self, key):
        """
        check to see if someone types the necessary keys to produce the easter egg
        """
        self.egg = self.egg + key
        if "burp" in self.egg:
            self.beltch.play()
            self.egg = ""

    def player_death(self):
        """
        things to do when the player dies
        """
        self.gunshot.play()
        self.player_is_dead = True
        time.sleep(1)
        self.laugh.play()
        self.screen_color(RED)

    def cowboy_death(self):
        """
        things to do when the cowboy dies
        """
        self.cowboy_is_dead = True
        time.sleep(.5)
        self.got_me.play()
        self.screen_color(GREEN)

    def cowboy_fired(self):
        """
        determine if the cowboy has fired based on the game ticks from within the run method
        """
        return (self.cowboy_is_showing and \
                self.player_is_dead is False and \
                self.game_tick >= GUNSLINGER)

    def run(self):
        """
        This is the main cycle of the game
        """
        while True:
            self.game_tick = self.game_tick + 1
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
                elif event.type == KEYDOWN:
                    # put my beltch easter egg in here
                    if event.key == K_b:
                        self.easter('b')
                    elif event.key == K_u:
                        self.easter('u')
                    elif event.key == K_r:
                        self.easter('r')
                    elif event.key == K_p:
                        self.easter('p')
                    else:
                        self.show_cowboy()
                elif event.type == MOUSEBUTTONDOWN:
                    if self.cowboy_is_showing and self.player_is_dead is False:
                        self.bang.play()
                        position = event.pos
                        if self.hit_target(position):
                            self.cowboy_death()
                        else:
                            self.player_death()
            if self.cowboy_fired():
                self.player_death()

            pygame.display.update()
            self.game_clock.tick(30)

def main():
    """
    start the game
    """
    game = Game()
    game.start().run()

if __name__ == "__main__":
    main()

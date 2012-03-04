import pygame, sys, os
from pygame.locals import *

import random
import time


pygame.init()

DIRNAME = os.path.abspath(os.path.dirname(__file__).decode('utf-8'))
RESOURCE_DIR = os.path.join(DIRNAME, 'resources/')
RED = pygame.Color(255, 0, 0)
GREEN  = pygame.Color(0, 255, 0)
BLUE = pygame.Color(0, 0, 255)
WHITE = pygame.Color(255, 255, 255)


fpsClock = pygame.time.Clock()

windowSurfaceObj = pygame.display.set_mode((640,480))
pygame.display.set_caption('High Noon')

cowboy = pygame.image.load(RESOURCE_DIR + 'cowboy.png')


def load_sound(name):
    """
    completely stolen from a tutorial here:
    http://pygame.org/docs/tut/chimp/ChimpLineByLine.html
    """
    class NoneSound:
        def play(self): pass
    
    if not pygame.mixer:
        return NoneSound()
        
    fullname = os.path.join('data', name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error, message:
        print 'Cannot load sound:', wav
        raise SystemExit, message
    return sound

gunshot = load_sound(RESOURCE_DIR + 'pow.wav')
got_me = load_sound(RESOURCE_DIR + 'ya_got_me.wav')
draw_em = load_sound(RESOURCE_DIR + 'draw.wav')
bang = load_sound(RESOURCE_DIR + 'bang.wav')
whistle = load_sound(RESOURCE_DIR + 'whistle.wav')
laugh = load_sound(RESOURCE_DIR + 'laugh.wav')


def random_pos():
    pos = (random.randint(0,540), random.randint(0, 400))
    print pos
    return pos

def rand_time():
    return random.random() * 4

def show_cowboy():
    windowSurfaceObj.fill(WHITE)
    time.sleep(rand_time())
    draw_em.play() 
    windowSurfaceObj.blit(cowboy, random_pos())


def hit_target(click_pos):
    color = windowSurfaceObj.get_at(click_pos)
    if color != WHITE:
        return True
    else:
        return False

windowSurfaceObj.fill(WHITE) 
whistle.play()   

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
        elif event.type == KEYDOWN:
            show_cowboy()
        elif event.type == MOUSEBUTTONDOWN:
            bang.play()
            position = event.pos
            if hit_target(position):
                time.sleep(.5)
                got_me.play()
                windowSurfaceObj.fill(GREEN)
                print "Target Hit"
            else:
                gunshot.play()
                time.sleep(1)
                laugh.play()
                windowSurfaceObj.fill(RED)
                print "Missed me!"

    pygame.display.update()
    fpsClock.tick(30)




    

    

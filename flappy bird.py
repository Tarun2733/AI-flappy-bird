import pygame
import random
import os
import time
import neat

# Window size
WIN_HEIGHT = 800
WIN_WIDTH = 600

# Load images
BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))),pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))),pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")))]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))

class Bird:
    IMGS = BIRD_IMGS
    MAX_ROTATION = 25                # How much the bird will tilt
    ROT_VEL = 20                     # How much we will rotate on each frame
    ANIMATION_TIME = 5               # How long each bird animation will last

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0               # How much the image is tilted
        self.tick_count = 0         # Physics of the bird
        self.vel = 0                # Velocity
        self.height = self.y        # Height of the bird
        self.img_count = 0          # Which image of the bird we are showing
        self.img = self.IMGS[0]     # Which image of the bird we are showing

    def jump(self):
        self.vel = -10.5            # Negative velocity means going up
        self.tick_count = 0         # When we last jumped
        self.height = self.y        # Where the bird jumped from
    
    def move(self):


while True:
    bird.move()

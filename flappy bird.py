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
bg_img = pygame.transform.scale(BG_IMG, (WIN_WIDTH, WIN_HEIGHT))

class Bird:
    IMGS = BIRD_IMGS
    MAX_ROTATION = 25                # How much the bird will tilt
    ROT_VEL = 20                     # How much we will rotate on each frame
    ANIMATION_TIME = 5               # How long each bird animation will last

    def __init__(self, x, y):
        self.x = x                  # Starting position
        self.y = y                  # Starting position
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
        self.tick_count += 1                                  # How many times we moved since the last jump
        d = self.vel*self.tick_count + 1.5*self.tick_count**2 # How many pixels we move up or down
        if d >= 16:                                           
            d = 16
        if d < 0:
            d -= 2
        self.y = self.y + d                                    # Move the bird up or down

        if d < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:                 # Tilt the bird up
                self.tilt = self.MAX_ROTATION
            else:
                if self.tilt > -90:                           # Tilt the bird down
                    self.tilt -= self.ROT_VEL
    
    def draw(self, win):
        self.img_count += 1
        if self.img_count < self.ANIMATION_TIME:               # Which image of the bird we are showing
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME*2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME*3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME*4:
            self.img = self.IMGS[1]
        elif self.img_count == self.ANIMATION_TIME*4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0
        
        if self.tilt <= -80:                                   # When the bird is nose diving
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME*2
        
        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft=(self.x,self.y)).center) # Rotate the image around the center
        win.blit(rotated_image, new_rect.topleft)              # Draw the image


    def get_mask(self):
        return pygame.mask.from_surface(self.img)              # Get the mask of the bird




class Pipe:
    GAP = 200                                                   # Space between the pipes
    VEL = 5                                                     # How fast the pipes are moving

    def __init__(self, x):
        self.x = x
        self.height = 0

        self.top = 0                                            # Where the top of the pipe is
        self.bottom = 0                                         # Where the bottom of the pipe is
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True) # Flip the pipe image
        self.PIPE_BOTTOM = PIPE_IMG
        self.passed = False                                     # If the bird passed the pipe
        self.set_height()                                       # Set the height of the pipe
    
    def set_height(self):
        self.height = random.randrange(50, 450)                 # Random height for the pipe
        self.top = self.height - self.PIPE_TOP.get_height()      # Where the top of the pipe is
        self.bottom = self.height + self.GAP                     # Where the bottom of the pipe is

    def move(self):
        self.x -= self.VEL                                      # Move the pipe
    
    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.x, self.top))              # Draw the top pipe
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))        # Draw the bottom pipe

    def collide(self, bird):
        bird_mask = bird.get_mask()                              # Get the mask of the bird
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)       # Get the mask of the top pipe
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM) # Get the mask of the bottom pipe
    
        top_offset = (self.x - bird.x, self.top - round(bird.y)) # Offset between the bird and the top pipe
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        b_point = bird_mask.overlap(bottom_mask, bottom_offset)  # Point of collision with the bottom pipe
        t_point = bird_mask.overlap(top_mask, top_offset)        # Point of collision with the top pipe

        if t_point or b_point:                                   # If there is a collision
            return True
        
        return False
    
class Base:
    VEL = 5
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG
    
    def __init__(self, y):
        self.y = y
        self.x1 = 0                                             # Position of the first base
        self.x2 = self.WIDTH                                     # Position of the second base
    
    def move(self):
        self.x1 -= self.VEL                                      # Move the first base
        self.x2 -= self.VEL                                      # Move the second base

        if self.x1 + self.WIDTH < 0:                             # If the first base is off the screen
            self.x1 = self.x2 + self.WIDTH                       # Move the first base to the right of the second base
        if self.x2 + self.WIDTH < 0:                             # If the second base is off the screen
            self.x2 = self.x1 + self.WIDTH                       # Move the second base to the right of the first base
    
    def draw(self, win):
        win.blit(self.IMG, (self.x1, self.y))                     # Draw the first base
        win.blit(self.IMG, (self.x2, self.y))                     # Draw the second base







def draw_window(win, bird, pipes, base):
    win.blit(bg_img, (0,0))
    for pipe in pipes:
        pipe.draw(win)
    base.draw(win)
    bird.draw(win)
    pygame.display.update()



def main():
    bird = Bird(230,350)
    base = Base(730)
    pipes = [Pipe(700)]
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()

    run = True
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:                       # If we close the application
                run = False
        #bird.move()
        add_pipe = False
        score = 0
        rem = []
        for pipe in pipes:
            
            if pipe.collide(bird):
                pass
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)
            if not pipe.passed and pipe.x < bird.x:             # If the bird passed the pipe
                pipe.passed = True
                add_pipe = True

            pipe.move()
        if add_pipe:
            score += 1
            pipes.append(Pipe(700))
        for r in rem:
            pipes.remove(r)
        
        base.move()
        draw_window(win, bird, pipes, base)
    pygame.quit()
    quit()
            
main()


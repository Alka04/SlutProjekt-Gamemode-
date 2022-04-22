from tkinter import Scale
from turtle import Screen
import pygame
pygame.init()

Screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Shooter')

#set framerate
clock = pygame.time.Clock()
FPS = 60

#define player action variables
moving_left = False
moving_right = False


#define colors
BG = (144, 201, 120)

def draw_bg():
    Screen.fill(BG)


class Soldier(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.speed = speed 
        img = pygame.image.load('img/player/Idle/0.png')
        self.image = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

def draw(self, moving_left, moving_right):
    #reset movement variables
    dx = 0
    dy = 0

    #assign movement variables if moving left or right
    if moving_left:
        dx = -self.speed
    if moving_right:
        dx = self.speed

    #Update rectangle position
    self.rect.x += dx
    self.rect.y += dy


    def draw(self):
        Screen.blit(self.image, self.rect)

player = Soldier(200, 200, 3, 5)





open = True
while open:

    clock.tick(FPS)

    draw_bg()

    player.draw()
    
    player.move(moving_left, moving_right)

    for event in pygame.event.get():
        #quit game
        if event.type == pygame.QUIT:
            open = False
        #Keyboard presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_ESCAPE:
                run = False

        #Keyboard button released
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False

        pygame.display.update()

pygame.quit()

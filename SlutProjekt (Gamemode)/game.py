from tkinter import Scale
from turtle import Screen
import pygame
pygame.init()

Screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Shooter')


#define player action variables
moving_left = False
moving_right = False


class Soldier(pygame.sprite.Sprite):
    def __init__(self, x, y, scale,):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/player/Idle/0.png')
        self.image = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def draw(self):
        Screen.blit(self.image, self.rect)

player = Soldier(200, 200, 3)
player2 = Soldier(400, 200, 3)




open = True
while open:

    player.draw()
    player2.draw()

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

        pygame.display.update()

pygame.quit()

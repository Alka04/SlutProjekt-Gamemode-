import imp
from tkinter import Scale
from turtle import Screen
import pygame
import os

pygame.init()


SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Shooter')

#bestäm framerate
clock = pygame.time.Clock()
FPS = 60

#definera spelets variabler
GRAVITY = 0.75

#definera spelarens handling variabler
moving_left = False
moving_right = False
shoot = False
grenade = False
grenade_thrown = False

#ladda in bilder
#kula
bullet_img = pygame.image.load('img/icons/bullet.png').convert_alpha()
#granat
grenade_img = pygame.image.load('img/icons/grenade.png').convert_alpha()


#definera färger
BG = (144, 201, 120)
RED = (255, 0, 0)


def draw_bg():
    screen.fill(BG)
    pygame.draw.line(screen, RED, (0, 300), (SCREEN_WIDTH, 300))



class Soldier(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed, ammo, grenades,):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type
        self.speed = speed
        self.ammo = ammo
        self.start_ammo = ammo
        self.shoot_cooldown = 0
        self.grenades = grenades
        self.health = 100
        self.max_health = self.health
        self.direction = 1
        self.vel_y = 0
        self.jump = False
        self.in_air = True
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        
        #ladda in all bilder för spelaren
        animation_types = ['Idle', 'Run', 'Jump', 'Death']
        for animation in animation_types:
            #starta om den temporära listan av bilder
            temp_list = []
            #räckna antalet av filerna i mappen
            num_of_frames = len(os.listdir(f'img/{self.char_type}/{animation}'))
            for i in range(num_of_frames):
                img = pygame.image.load(f'img/{self.char_type}/{animation}/{i}.png').convert_alpha()
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


    def update(self):
        self.update_animation()
        self.check_alive()
        #uppdatera nedräckning
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def move(self, moving_left, moving_right):
        #starta om rörelse variablerna
        dx = 0
        dy = 0

        #ge ut rörelse variablerna om man rör sig vänster eller höger
        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1

        #Hoppa
        if self.jump == True and self.in_air == False:
            self.vel_y = -11
            self.jump = False
            self.in_air = True


        #Lägg till gravitation
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y
        dy += self.vel_y 

        #Kolla kollision med Golvet
        if self.rect.bottom + dy > 300:
            dy = 300 - self.rect.bottom
            self.in_air = False


        #Uppdatera rectangelens position
        self.rect.x += dx
        self.rect.y += dy

    def shoot(self):
        if self.shoot_cooldown == 0 and self.ammo > 0:
            self.shoot_cooldown = 20
            bullet = Bullet(self.rect.centerx + (0.6 * self.rect.size[0] * self.direction), self.rect.centery, self.direction)
            bullet_group.add(bullet)
            #Minska ammo
            self.ammo -= 1
            

    def update_animation(self):
        #Uppdatera animation
        ANIMATION_COOLDOWN = 100
        #Uppdatera bilderna beroende på nuvarande frame
        self.image = self.animation_list[self.action][self.frame_index]
        #Kolla om tillräckligt med tid har g¨tt sen förra uppdateringen
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        #Om animationerna har tagit slut starta då om från starten
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) -1
            else:
                self.frame_index = 0



    def update_action(self, new_action):
        #Kolla om den nya aktivitet är anorlund från förra
        if new_action != self.action:
            self.action = new_action
            #uppdatera animations inställningarna 
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(3)

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

    def update(self):
        #Flytta på kulan
        self.rect.x += (self.direction * self.speed)
        #Kontrollera om kulan har försvunnit från skärmen
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()

        #Kolla kollision med karaktärer
        if pygame.sprite.spritecollide(player, bullet_group, False):
            if player.alive:
                player.health -= 5
                self.kill()
        if pygame.sprite.spritecollide(enemy, bullet_group, False):
            if enemy.alive:
                enemy.health -= 25
                self.kill()


class Grenade(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.timer = 100
        self.vel_y = -11
        self.speed = 7
        self.image = grenade_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

    def update(self):
        self.vel_y += GRAVITY
        dx = self.direction * self.speed
        dy = self.vel_y


        #Kontrollera kollision med golvet
        if self.rect.bottom + dy > 300:
            dy = 300 - self.rect.bottom
            self.speed = 0

        #Kontrollera kollision med väggarna
        if self.rect.left + dx < 0 or self.rect.right +dx > SCREEN_WIDTH:
            self.direction *= -1
            dx = self.direction * self.speed

        #uppdatera grenatens position
        self.rect.x += dx
        self.rect.y += dy

#Skapa sprite Grupper
bullet_group = pygame.sprite.Group()
grenade_group = pygame.sprite.Group()


player = Soldier('player', 200, 200, 3, 5, 20, 5)
enemy = Soldier('enemy', 400, 200, 3, 5, 20, 0)


run = True
while run:

    clock.tick(FPS)

    draw_bg()

    player.update()
    player.draw()

    enemy.update()
    enemy.draw()

    #Uppdatera och rita ut grupperna
    bullet_group.update()
    grenade_group.update()
    bullet_group.draw(screen)
    grenade_group.draw(screen)


    #Uppdatera spelarens händelser
    if player.alive:
        #Skjut kula
        if shoot:
            player.shoot()
        #Kasta Granater
        elif grenade and grenade_thrown == False and player.grenades > 0:
            grenade = Grenade(player.rect.centerx + (0.5 * player.rect.size[0] * player.direction),\
                        player.rect.top, player.direction)
            grenade_group.add(grenade)
            #Minska antalet granater
            player.grenades -= 1
            grenade_thrown = True
        if player.in_air:
            player.update_action(2)#2: Jump
        elif moving_left or moving_right:
            player.update_action(1)#1: run
        else:
            player.update_action(0)#0: idle
        player.move(moving_left, moving_right)

    for event in pygame.event.get():
        #Avsluta Spelet
        if event.type == pygame.QUIT:
            run = False
        #Tangentbord aktiveringar
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_SPACE:
                shoot = True
            if event.key == pygame.K_q:
                grenade = True
            if event.key == pygame.K_w and player.alive:
                player.jump = True
            if event.key == pygame.K_ESCAPE:
                run = False


        #Tangentbord knapp släppt
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_SPACE:
                shoot = False
            if event.key == pygame.K_q:
                grenade = False
                grenade_thrown = False




    pygame.display.update()

pygame.quit()
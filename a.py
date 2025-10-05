import math
import pygame
import random


scrwid = 800
scrhei = 500
playbegx = 370
playbegy = 380
enebegymin = 50
enebegymax = 1500
enespdx = 4
enespdy = 40
bullspdy = 10
colldist = 27

pygame.init()
screen = pygame.display.set_mode((scrwid, scrhei))

background = pygame.image.load("background.png")

pygame.display.set_caption("Space Invaders Project")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

playerimg = pygame.image.load("player.png")
playerx = playbegx
playery = playbegy
playerxchange = 0

enemyimg = []
enemyx = []
enemyy = []
enemyxchange = []
enemyychange = []
numofenemies = 6

for i in range(numofenemies):
    enemyimg.append(pygame.image.load("enemy.png"))
    enemyx.append(random.randint(0, scrwid - 64))
    enemyy.append(random.randint(enebegymin, enebegymax))
    enemyxchange.append(enespdx)
    enemyychange.append(enespdy)

bulletimg = pygame.image.load("bullet.png")
bulletx = 0
bullety = playbegy
bulletxchange = 0
bulletychange = bullspdy
bulletstate = "ready"

score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)
textx = 10 
texty = 10

overfont = pygame.font.Font("freesansbold.ttf", 64)

def showscore(x, y):
    score = font.render("score: "+ str(score_value), True, (255, 255, 255))
    screen.blit(score, x, y)

def gameovertext():
    overtext = overfont.render("GAME OVER", True, (255, 255, 255))
    screen.blit(overtext, (200, 250))

def player(x, y):
    screen.blit(playerimg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyimg[i], (x, y))

def firebullet(x, y):
    global bulletstate
    bulletstate = "fire"
    screen.blit(bulletimg, (x + 16, y + 10))

def iscollosion(enemyx, enemyy, bulletx, bullety):
    distance = math.sqrt((enemyx - bulletx) ** 2 + (enemyy - bullety) ** 2)
    return distance < colldist

running  = True 
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerxchange = -5
            if event.key == pygame.K_RIGHT:
                playerxchange = 5
            if event.key == pygame.K_SPACE and bulletstate == "ready":
                bulletx = playerx
                firebullet(bulletx, bullety)
        if event.type == pygame.KEYUP and event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
            playerxchange = 0
    
    playerx += playerxchange
    playerx = max(0, min(playerx, scrwid - 64))

    for i in range(numofenemies):
        if enemyy[i] > 340:
            for j in range(numofenemies):
                enemyy[j] = 2000
            gameovertext()
            break

        enemyx[i] += enemyxchange[i]
        if enemyx[i] <= 0 or enemyx[i] >= scrwid - 64:
            enemyxchange[i] *= -1
            enemyy[i] += enemyychange[i]

        if iscollosion(enemyx[i], enemyy[i], bulletx, bullety):
            bullety = playbegy
            bulletstate = "ready"
        elif bulletstate == "fire":
            firebullet(bulletx, bullety)
            bullety -= bulletychange
        
        player(playerx, playery)
        showscore(textx, texty)
        pygame.display.update()
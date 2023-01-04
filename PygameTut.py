import random
import math
import pygame
from pygame import mixer

pygame.init()
# Create a Screen
screen = pygame.display.set_mode((800, 600))
font = pygame.font.SysFont("Arial", 25)
# Set Caption and Image
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('spaceship.png').convert_alpha()
pygame.display.set_icon(icon)

# Background
background = pygame.image.load('space.png').convert_alpha()
mixer.music.load('bgm.mp3')
mixer.music.play(-1)
# Player
playerimg = pygame.image.load('arcade-game.png').convert_alpha()
playerx = 370
playery = 480
playerx_change = 0


def player(x, y):
    screen.blit(playerimg, (x, y))


# Enemy
enemyImg = []
enemyx = []
enemyy = []
enemyx_change = []
enemyy_change = []
num_enemies = 6
for i in range(num_enemies):
    enemyImg.append(pygame.image.load('ufo.png'))
    enemyx.append(random.randint(0, 736))
    enemyy.append((random.randint(0, 20)))
    enemyx_change.append(0.3)
    enemyy_change.append(30)


def enemy(x, y, j):
    screen.blit(enemyImg[j], (x, y))


# Bullet
bulletImg = pygame.image.load('bullet.png').convert_alpha()
bulletx = 0
bullety = 480
bulletx_change = 0
bullety_change = 0.7
bulletState = "ready"


def fire_bullet(x, y):
    global bulletState
    bulletState = "fire"
    screen.blit(bulletImg, (x + 32, y + 32))


# Collision
def collision(x1, y1, x2, y2):
    dist = math.sqrt((math.pow((x1 - x2), 2)) + (math.pow((y1 - y2), 2)))
    if dist < 25:
        return True
    else:
        return False


# Score
score = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10


def show_score(x, y):
    score_val = font.render("Score:" + str(score), True, (255, 255, 255))
    screen.blit(score_val, (x, y))


running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerx_change = -0.5
            if event.key == pygame.K_RIGHT:
                playerx_change = 0.5
            if event.key == pygame.K_SPACE:
                if bulletState == "ready":
                    bulletx = playerx
                    fire_bullet(bulletx, bullety)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerx_change = 0

    playerx += playerx_change

    # Player
    if playerx <= 0:
        playerx = 0
    elif playerx >= 700:
        playerx = 700

    # Enemy
    for i in range(num_enemies):
        enemyx[i] += enemyx_change[i]
        enemyy[i] += enemyy_change[i]
        if enemyx[i] <= 0:
            enemyx_change[i] = 0.5
            enemyy[i] += enemyy_change[i]
        elif enemyx[i] >= 736:
            enemyx_change[i] = -0.5
            enemyy[i] += enemyy_change[i]

        # Collision
        coll = collision(enemyx[i], enemyy[i],bulletx, bullety)
        if coll:
            bullety = 480
            bulletState = "ready"
            score += 1
            mixer.music.load('mixkit-arcade-game-explosion-1699.wav')
            mixer.music.play()
            print(score)
            enemyx[i] = random.randint(0, 736)
            enemyy[i] = random.randint(10, 150)
        enemy(enemyx[i], enemyy[i], i)

    # Bullet Fire
    if bullety <= 0:
        bullety = 480
        bulletState = "ready"

    if bulletState == "fire":
        fire_bullet(bulletx, bullety)
        bullety -= bullety_change

    player(playerx, playery)
    show_score(textX, textY)
    pygame.display.update()

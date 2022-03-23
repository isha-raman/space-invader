# ctrl + alt + l formats your code
import pygame
import random  # lets you randomize
import math
from pygame import mixer  # mixer helps import music in pygame

# initialize pygame to acess all of its features
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))  # widthv-x axis height - y axis

# backgroung
background = pygame.image.load('space.jpg')

# background sound
mixer.music.load('background.wav')  # mixer.music is when you play it continously..for something short use mixer.sound
mixer.music.play(-1)  # -1 means it will play on loop

# title and icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# player
PlayerImg = pygame.image.load('spaceship.png')
PlayerX = 370
PlayerY = 480
PlayerX_Change = 0

# enemy
EnemyImg = []  # store all the values in the list so it appears one by one but will happen so fast that it will appear at once
EnemyX = []
EnemyY = []
EnemyX_Change = []
EnemyY_Change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    EnemyImg.append(pygame.image.load('enemy.png'))  # use append to add values to the list
    EnemyX.append(random.randint(0, 735))  # chooses a random integer in this range
    EnemyY.append(random.randint(50, 150))
    EnemyX_Change.append(0.3)  # 0.3 or 0 it wouldnt matter
    EnemyY_Change.append(40)

# bullet
BulletImg = pygame.image.load('bullet.png')
BulletX = 0
BulletY = 480  # since spaceship will always be at 480
BulletX_Change = 0
BulletY_Change = 0.3
# ready state - you cant see bullet on screen
# fire state - bullet is currently moving
Bullet_State = "ready"

# score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)  # 32 x 32 px

TextX = 10
TextY = 10

# game over
over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (123, 140, 168))  # instead of blit we render font first
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (123, 140, 168))
    screen.blit(over_text, (200, 250))


def player(x, y):  # function to draw the player on screen....call the function in the game loop
    # here x and y just means first and second values of player(PlayerX,PlayerY) calling function
    screen.blit(PlayerImg, (x, y))  # blit means to draw the image on screen


def enemy(x, y, i):
    screen.blit(EnemyImg[i], (x, y))


def fire_bullet(x, y):
    global Bullet_State  # global to access the values
    Bullet_State = "fire"
    screen.blit(BulletImg, (x + 16, y + 10))  # to make sure bullet appears at the centre of spaceship


def is_collision(EnemyX, EnemyY, BulletX, BulletY):
    distance = math.sqrt((math.pow(EnemyX - BulletX, 2)) + (math.pow(EnemyY - BulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# to keep the window open add game loop (while infinite loop) and also quit function (to make sure laptop does not hang)
running = True
while running:

    # anything that you want to appear constantly has to be in while loop
    # r g b - red green blue
    screen.fill((52, 139, 158))  # backgroundcolor
    screen.blit(background, (0, 0))
    # PlayerX -= 0.1
    # PlayerY -= 0.1
    # print(PlayerX) # to see the x coordinate of player change

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                PlayerX_Change = -0.3
            if event.key == pygame.K_RIGHT:
                PlayerX_Change = 0.3
            if event.key == pygame.K_SPACE:
                if Bullet_State == "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()  # no repeat so no -1
                    # get the current x coordinate of spaceship
                    BulletX = PlayerX
                    fire_bullet(BulletX, BulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                PlayerX_Change = 0

    PlayerX += PlayerX_Change  # + because + - is already -

    # boundary for spaceship
    if PlayerX <= 0:
        PlayerX = 0
    elif PlayerX >= 736:
        PlayerX = 736

    # enemy movement
    for i in range(num_of_enemies):  # add for loop so computer knows which enemy we are taking about
        # game over
        if EnemyY[i] > 440:
            for j in range(num_of_enemies):
                EnemyY[j] = 2000  # we want all enemies to move out of screen
            game_over_text()
            break

        EnemyX[i] += EnemyX_Change[i]

        if EnemyX[i] <= 0:
            EnemyX_Change[i] = 0.3
            EnemyY[i] += EnemyY_Change[i]
        elif EnemyX[i] >= 736:
            EnemyX_Change[i] = -0.3
            EnemyY[i] += EnemyY_Change[i]

        # collision
        collision = is_collision(EnemyX[i], EnemyY[i], BulletX,
                                 BulletY)  # if is_collison is true its value will get stored here
        if collision:
            collision_sound = mixer.Sound('explosion.wav')
            collision_sound.play()
            BulletY = 480
            Bullet_State = "ready"
            score_value += 1
            EnemyX[i] = random.randint(0, 735)
            EnemyY[i] = random.randint(50, 150)

        enemy(EnemyX[i], EnemyY[i], i)

    # bullet movement
    if BulletY <= 0:  # in order to fire multiple bullet we need to reset state of bullet
        BulletY = 480
        Bullet_State = "ready"
    if Bullet_State == "fire":
        fire_bullet(BulletX, BulletY)
        BulletY -= BulletY_Change

    player(PlayerX,
           PlayerY)  # call the function after the screen is drawn or else player would be drawn underneath the screen
    show_score(TextX, TextY)
    pygame.display.update()  # innit and update code is very important...update to constantly update your screen

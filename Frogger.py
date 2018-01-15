import random
import pygame
import time
import os
import re
from pygame.locals import *

pygame.init()
pygame.font.init()

display_width = 1080
display_height = 720

black = (0, 0, 0)
grey = (100, 100, 100)
white = (255, 255, 255)
red = (255, 0, 0)
violet = (236, 3, 150)
blue = (15, 100, 180)

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Frogger')
clock = pygame.time.Clock()

bg = pygame.image.load('BackGroundUpd4.png')  # optional
bg = pygame.transform.scale(bg, (display_width, display_height))

frog_width = 70
frog_height = 70
frogImg = pygame.transform.scale(pygame.image.load('frogfinal.png'), (frog_width - 5, frog_height - 5))
pygame.mixer.music.load('nightcall.mp3')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.1)


def scorePoints(count):
    font = pygame.font.Font('font2.ttf', 20)
    text = font.render('Score: ' + str(count), True, blue)
    gameDisplay.blit(text, (850, display_height - 30))


def lifeCount(lives):
    fontLives = pygame.font.Font('font2.ttf', 20)
    textLives = fontLives.render('Lives: ' + str(lives), True, violet)
    gameDisplay.blit(textLives, (10, display_height - 30))


def message_display(text, color=white, font='font.ttf'):
    largeText = pygame.font.Font(font, 60)
    TextSurf, TextRect = text_objects(text, largeText, color)
    TextRect.center = ((display_width / 2), (display_height / 2))
    gameDisplay.blit(TextSurf, TextRect)
    pygame.display.update()


def small_message_display(msg, x, y, w, h, textcolor):
    smallText = pygame.font.Font('font.ttf', 12)
    textSurf, textRect = text_objects(msg, smallText, textcolor)
    textRect.center = ((x + (w / 2)), (y + (h / 2)))
    gameDisplay.blit(textSurf, textRect)


def carCreate():
    car_w = 100
    car_h = 50
    carImg = pygame.transform.flip(pygame.transform.scale(pygame.image.load('NCar1.png'), (car_w, car_h)), 1, 0)


def carAdd(x, y, j):
    carImg = pygame.image.load('N1.png')
    if j % 5 == 2:
        carImg = pygame.image.load('N2.png')
    elif j % 5 == 3:
        carImg = pygame.image.load('N3.png')
    elif j % 5 == 4:
        carImg = pygame.image.load('N41.png')
    elif j % 5 == 1:
        carImg = pygame.image.load('N5.png')
    w = 100  # optional
    h = 50  # optional
    carImg = pygame.transform.scale(carImg, (w, h))  # optional
    carImg = pygame.transform.flip(carImg, 1, 0)
    gameDisplay.blit(carImg, (x, y))


def woodAdd(x, y):
    woodImg = pygame.image.load('logtest.png')
    w = 225  # optional
    h = 50  # optional
    woodImg = pygame.transform.scale(woodImg, (w, h))  # optional
    gameDisplay.blit(woodImg, (x, y))


def carsFunc(carx, cary, carw, carh, j):
    carAdd(carx, cary, j)


def woodFunc(woodx, woody):
    woodAdd(woodx, woody)


def frog(x, y):
    gameDisplay.blit(frogImg, (x, y))


def text_objects(text, font, color=white):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()


def crash(lives):
    death = pygame.mixer.Sound('death.wav')
    death.play()
    message_display('You have died!', violet)
    time.sleep(2)
    lives = lives - 1
    if lives == 0:
        gameDisplay.fill(black)
        message_display('Game over!', violet)
        time.sleep(2)
        game_intro()
    return lives


def winDisp(score):
    gameDisplay.fill(black)
    message_display('You Won!', blue)
    time.sleep(2)
    gameDisplay.fill(black)
    finalText = 'Your score  ' + str(score)
    message_display(finalText, blue)
    time.sleep(3)


def button(msg, x, y, w, h, acolor, icolor, action=None, textcolor=white):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    # print(mouse)

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, acolor, (x, y, w, h))
        if click[0] == 1 and action != None:
            if action == 'play':
                game_loop()
            elif action == 'quit':
                pygame.quit()
                quit()
            elif action == 'hard':
                game_loop(0)
    else:
        pygame.draw.rect(gameDisplay, icolor, (x, y, w, h))

    small_message_display(msg, x, y, w, h, textcolor)


def game_intro(won=0):
    intro = True
    textarr = ['I\'s not a crab! It\'s a frog!',
               '"Game of the year" - IGN ', '"Best. Game. Ever." - Wired UK', '"Mom\'s spaghetti" - Eminem',
               'A Breath of Fresh Air - AVGN', '"Masterfully Crafted Game" - GameSpot',
               '98/100 - Polygon', '"Can\'t stop playing" - The Kotaku']
    rnd = random.randrange(0, len(textarr) - 1)
    while intro:
        bg = pygame.image.load('intro3.jpg')
        bg = pygame.transform.scale(bg, (display_width, display_height))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        gameDisplay.blit(bg, (0, 0))
        message_display('Frogger', violet)
        small_message_display(textarr[rnd], 900 - len(textarr[rnd]) * 5, 0, 100, 100, white)
        button('Start', 150, 600, 100, 50, black, white, 'play', violet)
        rect2 = display_width - 250
        button('Exit', rect2, 600, 100, 50, black, white, 'quit', violet)
        if won:
            button('Nightmare', 500, 600, 150, 50, black, red, 'hard', white)

        pygame.display.update()
        clock.tick(10)
    bg = pygame.image.load('BackGroundUpd1.png')
    bg = pygame.transform.scale(bg, (display_width, display_height))


def game_loop(yc=60):
    win = 0
    score = 50000
    flags = [0, 0, 0, 0, 0]
    lives = 3
    x_change = 0
    y_change = 0

    canMove = 1
    timeCheck = time.time()

    x = (display_width * 0.5) - 50
    y = (display_height * 0.5) + 230

    car_speed = 10
    car_width = 100
    car_height = 50

    wood_speed = 8
    wood_width = 225
    wood_height = 50

    woodDirection = [1, 1, -1]
    woodX = [-1050, -250, 950]
    woodY = [65, 185, 125]

    wood2Direction = [1, 1, -1]
    wood2X = [-550, -650, 250]
    wood2Y = [65, 185, 125]

    carsX = [-100, -450, -800, -200, -750, -450, -1100, -300, -650, -1000, -250, -800]
    carsY = [305, 305, 305, 365, 365, 425, 425, 485, 485, 485, 545, 545]

    gameExit = False

    while not gameExit:
        score -= 1
        flag = 1
        # print(pygame.mouse.get_pos())
        gameDisplay.blit(bg, (0, 0))
        scorePoints(score)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and canMove != 0:
                    x_change = -yc
                    canMove = 0
                elif event.key == pygame.K_RIGHT and canMove != 0:
                    x_change = yc
                    canMove = 0
                elif event.key == pygame.K_UP and canMove != 0:
                    y_change = -60
                    canMove = 0
                elif event.key == pygame.K_DOWN and canMove != 0:
                    y_change = 60
                    canMove = 0

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    y_change = 0

        x += x_change
        y += y_change
        y_change = 0
        x_change = 0

        for j in range(0, len(carsX)):
            carsFunc(carsX[j], carsY[j], car_width, car_height, j)
            carsX[j] += car_speed

        for j in range(0, len(woodX)):
            woodFunc(woodX[j], woodY[j])
            if woodDirection[j] == -1:
                woodX[j] -= wood_speed
            else:
                woodX[j] += wood_speed

        for j in range(0, len(wood2X)):
            woodFunc(wood2X[j], wood2Y[j])
            if wood2Direction[j] == -1:
                wood2X[j] -= wood_speed
            else:
                wood2X[j] += wood_speed

        frog(x, y)
        lifeCount(lives)

        if x > display_width + 30 - frog_width or x < -30:
            x = (display_width * 0.5) - 50
            y = (display_height * 0.5) + 230
            lives = crash(lives)

        if y > display_height + 30 - frog_height or y < -30:
            x = (display_width * 0.5) - 50
            y = (display_height * 0.5) + 230
            lives = crash(lives)

        for j in range(0, len(carsX)):
            if carsX[j] > display_width:
                carsX[j] = 0 - car_width

        for j in range(0, len(woodX)):
            if woodDirection[j] == 1 and woodX[j] > display_width:
                woodX[j] = 0 - wood_width
            elif woodDirection[j] == -1 and woodX[j] + wood_width < 0:
                woodX[j] = display_width + wood_width

        for j in range(0, len(wood2X)):
            if wood2Direction[j] == 1 and wood2X[j] > display_width:
                wood2X[j] = 0 - wood_width
            elif wood2Direction[j] == -1 and wood2X[j] + wood_width < 0:
                wood2X[j] = display_width + wood_width

        for j in range(0, len(carsX)):
            if y + 5 < carsY[j] + car_height and y + frog_height > carsY[j] + 5:
                if x + frog_width > carsX[j] + 5 and x + 5 < carsX[j] + car_width:
                    x = (display_width * 0.5) - 50
                    y = (display_height * 0.5) + 230
                    lives = crash(lives)

        for j in range(0, len(woodX)):
            if woodY[j] >= y and woodY[j] + wood_height <= y + frog_height:
                if x + frog_width >= woodX[j] and x + frog_width <= woodX[j] + wood_width and woodDirection[
                    j] != -1:
                    x_change = wood_speed
                    flag = 1
                    break
                elif x >= woodX[j] and x + frog_width <= woodX[j] + wood_width + 50 and woodDirection[j] == -1:
                    x_change = -wood_speed
                    flag = 1
                    break
                elif x + frog_width < woodX[j] or x > woodX[j] + wood_width:
                    flag = 0

        for j in range(0, len(wood2X)):
            if wood2Y[j] >= y and wood2Y[j] + wood_height <= y + frog_height:
                if x + frog_width >= wood2X[j] and x + frog_width <= wood2X[j] + wood_width and wood2Direction[
                    j] != -1:
                    x_change = wood_speed
                    flag = 1
                    break
                elif x >= wood2X[j] and x + frog_width <= wood2X[j] + wood_width + 50 and wood2Direction[j] == -1:
                    x_change = -wood_speed
                    flag = 1
                    break
                elif (x + frog_width < wood2X[j] or x > wood2X[j] + wood_width) and flag == 0:
                    x = (display_width * 0.5) - 50
                    y = (display_height * 0.5) + 230
                    lives = crash(lives)
                    break
        if time.time() - timeCheck > 0.2:
            timeCheck = time.time()
            canMove = 1
        if win == 5:
            winDisp(score)
            gameExit = True
            won = 1
            game_intro(won)  # delete if necessary
        winPoints = [150, 340, 540, 740, 940]
        if y < 30:
            for i in range(0, len(winPoints)):
                if x < winPoints[i] and x + frog_width > winPoints[i] and flags[i] != 1:
                    x = (display_width * 0.5) - 50
                    y = (display_height * 0.5) + 230
                    flags[i] = 1
                    score += 10000
                    win += 1
                    message_display('+10k', violet, 'font2.ttf')
                    time.sleep(1.5)
                    break
                elif i == len(winPoints) - 1:
                    x = (display_width * 0.5) - 50
                    y = (display_height * 0.5) + 230
                    lives = crash(lives)

        for i in range(0, len(flags)):
            if flags[i] == 1:
                winImg = pygame.transform.scale(pygame.image.load('frogfinal.png'), (frog_width, frog_height))
                winImg = pygame.transform.flip(winImg, 0, 1)
                gameDisplay.blit(winImg, (winPoints[i] - frog_width / 2, 5))

        pygame.display.update()
        clock.tick(60)


game_intro()
game_loop()
pygame.quit()
pygame.font.quit()
quit()

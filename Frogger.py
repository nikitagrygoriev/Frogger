import random
import pygame
import time

pygame.init()

display_width = 1080
display_height = 720

black = (0, 0, 0)
grey = (100, 100, 100)
white = (255, 255, 255)
red = (255, 0, 0)

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Frogger')
clock = pygame.time.Clock()

bg = pygame.image.load("BackGroundUpd.png")  # optional
bg = pygame.transform.scale(bg, (display_width, display_height))

frogImg = pygame.image.load('frog.png')
frog_width = 75
frog_height = 75
frogImg = pygame.transform.scale(frogImg, (frog_width, frog_height))

def cars_dodged(count):
    font = pygame.font.SysFont(None, 25)
    text = font.render("Dodged: " + str(count), True, white)
    gameDisplay.blit(text, (0, 0))



def carAdd(x,y):
    car1Img = pygame.image.load('Car1.png')  # optional
    w = 100  # optional
    h = 50  # optional
    car1Img = pygame.transform.scale(car1Img, (w, h))  # optional
    car1Img = pygame.transform.flip(car1Img,1,0)
    gameDisplay.blit(car1Img,(x,y))


def cars(carx, cary, carw, carh, color):
    # pygame.draw.rect(gameDisplay, color, [carx, cary, carw, carh])
    carAdd(carx,cary)


def frog(x, y):
    gameDisplay.blit(frogImg, (x, y))


def text_objects(text, font, color=white):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()


def message_display(text, color=white):
    largeText = pygame.font.Font('freesansbold.ttf', 120)
    TextSurf, TextRect = text_objects(text, largeText, color)
    TextRect.center = ((display_width / 2), (display_height / 2))
    gameDisplay.blit(TextSurf, TextRect)
    pygame.display.update()


def small_message_display(msg, x, y, w, h, textcolor):
    smallText = pygame.font.Font("freesansbold.ttf", 20)
    textSurf, textRect = text_objects(msg, smallText, textcolor)
    textRect.center = ((x + (w / 2)), (y + (h / 2)))
    gameDisplay.blit(textSurf, textRect)


def crash():
    message_display("You lost", red)
    time.sleep(2)
    game_intro()


def button(msg, x, y, w, h, acolor, icolor, action=None, textcolor=white):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    # print(mouse)

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, acolor, (x, y, w, h))
        if click[0] == 1 and action != None:
            if action == "play":
                game_loop()
            elif action == "quit":
                pygame.quit()
                quit()
    else:
        pygame.draw.rect(gameDisplay, icolor, (x, y, w, h))

    small_message_display(msg, x, y, w, h, textcolor)


def game_intro():
    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        gameDisplay.fill(white)
        message_display("Frogger", black)

        # largeText = pygame.font.Font('freesansbold.ttf', 120)
        # TextSurf, TextRect = text_objects("Frogger", largeText, black)
        # TextRect.center = ((display_width / 2), (display_height / 2))
        # gameDisplay.blit(TextSurf, TextRect)

        button("Start", 150, 550, 100, 50, grey, black, "play")
        rect2 = display_width - 250
        button("Exit", rect2, 550, 100, 50, grey, black, "quit")
        pygame.display.update()
        clock.tick(10)


def game_loop():
    x = (display_width * 0.5) - 50
    y = (display_height * 0.5) + 230

    x_change = 0
    y_change = 0

    car_startx = -200
    car_starty = random.randrange(100, display_height - 500)
    car_speed = 10
    car_width = 100
    car_height = 50

    dodged = 0
    gameExit = False
    while not gameExit:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -50
                elif event.key == pygame.K_RIGHT:
                    x_change = 50
                elif event.key == pygame.K_UP:
                    y_change = -50
                elif event.key == pygame.K_DOWN:
                    y_change = 50

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    y_change = 0

        x += x_change
        y += y_change

        # gameDisplay.fill(white)
        gameDisplay.blit(bg, (0, 0))  # optional

        cars(car_startx, car_starty, car_width, car_height, black)
        car_startx += car_speed
        frog(x, y)
        cars_dodged(dodged)

        if x > display_width + 30 - frog_width or x < -30:
            crash()
            # gameExit = True
        if y > display_height + 30 - frog_height or y < -30:
            crash()

        if car_startx > display_width:
            car_startx = 0 - car_height
            car_starty = random.randrange(0, display_height)
            dodged += 1

        if x < car_startx + car_width and x > car_startx:
            if y + car_height > car_starty and y < car_starty + car_height:
                crash()

        pygame.display.update()
        # time.sleep(0.25)  # opional
        clock.tick(150)


game_intro()
game_loop()
pygame.quit()
quit()

import pygame
import time
import random
pygame.init()

white = (255,255,255)
red = (255,0,0)
green = (5,102,8)
blue = (0,0,255)
black = (0,0,0)
yellow = (255,255,0)
light_blue = (173,216,230)

display_width = 800
display_height = 600

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Poison Reloaded')
icon = pygame.image.load('Apple.png')
pygame.display.set_icon(icon)
img = pygame.image.load('snakehead.png')
appleimg = pygame.image.load('Apple.png')


block_size = 20
appleThickness = 30
fps = 20
direction = "right"
clock = pygame.time.Clock()

smallfont = pygame.font.Font("comicsansms.ttf", 30)
mediumfont = pygame.font.Font("comicsansms.ttf", 40)
largefont = pygame.font.Font("comicsansms.ttf", 50)

def pause():
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
        #gameDisplay.fill(light_blue)
        message_screen("Game Paused", black, -100, "large")
        message_screen("Press C to resume or Q to Quit", black, 25)
        pygame.display.update()
        clock.tick(5)

def score(score):
    text = smallfont.render("Score: " + str(score), True, black)
    gameDisplay.blit(text, [0,0])

def RandAppleGen():
    randApple_X = round(random.randrange(0, display_width-appleThickness))
    randApple_Y = round(random.randrange(0, display_height-appleThickness))
    return randApple_X, randApple_Y

def gameIntro():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    intro = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        gameDisplay.fill(yellow)
        message_screen("Welcome to Poison Reloaded", blue, -100, "large")
        message_screen("Eat red apples", black, -30)
        message_screen("Eating increases length of the snake", black, 10)
        message_screen("Don't run over yourself", black, 50)
        message_screen("Press C to play or Q to Quit", black, 180)
        message_screen("Press P during gameplay to pause", black, 220)
        pygame.display.update()
        clock.tick(15)

def text_objects(text, color, size):
    if size == "small":
        text_surf = smallfont.render(text, True, color)
    elif size == "medium":
        text_surf = mediumfont.render(text, True, color)
    elif size == "large":
        text_surf = largefont.render(text, True, color)    
    return text_surf, text_surf.get_rect()

def message_screen(msg, color, y_displace = 0, size = "small"):
    text_surf, text_rect = text_objects(msg, color, size)
    text_rect.center = (display_width/2, display_height/2 + y_displace)
    gameDisplay.blit(text_surf, text_rect)
    
def snake(block_size, snakelist):
    if direction == "right":
        head = pygame.transform.rotate(img, 270) 
    if direction == "left":
        head = pygame.transform.rotate(img, 90)
    if direction == "up":
        head = img
    if direction == "down":
        head = pygame.transform.rotate(img, 180)
    gameDisplay.blit(head, (snakelist[-1][0], snakelist[-1][1]))
    for XnY in snakelist[:-1]:
        pygame.draw.rect(gameDisplay, green, [XnY[0],XnY[1],block_size,block_size])

def GameLoop():
    global direction
    gameExit = False
    gameOver = False
    lead_x = display_width/2
    lead_y = display_height/2
    lead_x_change = 0
    lead_y_change = 0
    randApple_X, randApple_Y = RandAppleGen()
    snakelist = []
    snakelength = 1

    while not gameExit:
        while gameOver == True:
            gameDisplay.fill(light_blue)
            message_screen("Game over!!", red, -50, size = "large")
            message_screen("Press C to play again and Q to quit", black, 50)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameExit = True
                    gameOver = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False
                    if event.key == pygame.K_c:
                        GameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True    
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    direction = "left"
                    lead_x_change = -block_size
                    lead_y_change = 0
                elif event.key == pygame.K_RIGHT:
                    direction = "right"
                    lead_x_change = block_size
                    lead_y_change = 0
                elif event.key == pygame.K_UP:
                    direction = "up"
                    lead_y_change = -block_size
                    lead_x_change = 0
                elif event.key == pygame.K_DOWN:
                    direction = "down"
                    lead_y_change = block_size
                    lead_x_change = 0
                elif event.key == pygame.K_p:
                    pause()

        if lead_x >= display_width or lead_x < 0 or lead_y >= display_height or lead_y < 0:
            gameOver = True
        
        lead_x += lead_x_change
        lead_y += lead_y_change
        gameDisplay.fill(light_blue)
        
        ## DRAWING THE AAPLE
        gameDisplay.blit(appleimg, (randApple_X, randApple_Y))

        ## DRAWING THE SNAKE
        snakehead = []
        snakehead.append(lead_x)
        snakehead.append(lead_y)
        snakelist.append(snakehead)
        if len(snakelist) > snakelength:
            del snakelist[0]
            
        for each_segment in snakelist[:-1]:
            if each_segment == snakehead:
                gameOver = True
        snake(block_size, snakelist)
        score(snakelength-1)

        pygame.display.update()
        
        ## EATING THE APPLE
        if lead_x > randApple_X and lead_x < randApple_X+30 or lead_x+block_size > randApple_X and lead_x+block_size < randApple_X+appleThickness:  
            if lead_y > randApple_Y and lead_y < randApple_Y+30:
                randApple_X, randApple_Y = RandAppleGen()
                snakelength += 1
            elif lead_y+block_size > randApple_Y and lead_y+block_size < randApple_Y+appleThickness:
                randApple_X, randApple_Y = RandAppleGen()
                snakelength += 1
        
        clock.tick(fps)

    pygame.quit()

gameIntro()
GameLoop()
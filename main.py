import pygame
import sys
from pygame.locals import *
import time

def game_open():
    screen.blit(opening, (0, 0))
    pygame.display.update()
    time.sleep(5)
    screen.fill(white)

    # Drawing vertical lines
    pygame.draw.line(screen,line_color,(width/3,0),(width/3, height),7)
    pygame.draw.line(screen,line_color,(width/3*2,0),(width/3*2, height),7)

    # Drawing horizontal lines
    pygame.draw.line(screen,line_color,(0,height/3),(width, height/3),7)
    pygame.draw.line(screen,line_color,(0,height/3*2),(width, height/3*2),7)
    draw_status()

def draw_status():
    global draw

    if winner is None:
        message = xo.upper() + "'s Turn"
    else:
        message = winner.upper() + " won!"
    if draw:
        message = 'Game Draw!'

    font = pygame.font.Font(None, 30)
    text = font.render(message, 1, (255, 255, 255))

    # copy the rendered message onto the board
    screen.fill ((0, 0, 0), (0, 400, 500, 100))
    text_rect = text.get_rect(center=(width/2, 500-50))
    screen.blit(text, text_rect)
    pygame.display.update()

def check_win():
    global TTT, winner, draw

    # check for winning rows
    for row in range(0, 3):
        if ((TTT[row][0] == TTT[row][1] == TTT[row][2]) and (TTT[row][0] is not None)):
            # this row won
            winner = TTT[row][0]
            pygame.draw.line(screen, (250, 0, 0), (0, (row + 1) * height / 3 - height / 6), \
                         (width, (row + 1) * height / 3 - height / 6), 4)
            break

    # check for winning columns
    for col in range(0, 3):
        if (TTT[0][col] == TTT[1][col] == TTT[2][col]) and (TTT[0][col] is not None):
            # this column won
            winner = TTT[0][col]
            # draw winning line
            pygame.draw.line(screen, (250, 0, 0), ((col + 1) * width / 3 - width / 6, 0), \
                         ((col + 1) * width / 3 - width / 6, height), 4)
            break

    # check for diagonal winners
    if (TTT[0][0] == TTT[1][1] == TTT[2][2]) and (TTT[0][0] is not None):
        # game won diagonally left to right
        winner = TTT[0][0]
        pygame.draw.line(screen, (250, 70, 70), (50, 50), (350, 350), 4)

    if (TTT[0][2] == TTT[1][1] == TTT[2][0]) and (TTT[0][2] is not None):
        # game won diagonally right to left
        winner = TTT[0][2]
        pygame.draw.line(screen, (250, 70, 70), (350, 50), (50, 350), 4)

    if (all([all(row) for row in TTT]) and winner is None):
        draw = True
    draw_status()

def drawXO(row,col):
    global TTT,xo
    if row==1:
        posx = 30
    if row==2:
        posx = width/3 + 30
    if row==3:
        posx = width/3*2 + 30

    if col==1:
        posy = 30
    if col==2:
        posy = height/3 + 30
    if col==3:
        posy = height/3*2 + 30
    TTT[row-1][col-1] = xo
    if(xo == 'x'):
        screen.blit(x_img,(posy,posx))
        xo= 'o'
    else:
        screen.blit(o_img,(posy,posx))
        xo= 'x'
    pygame.display.update()
    #print(posx,posy)
    #print(TTT)

def userClick():
    #get coordinates of mouse click
    x,y = pygame.mouse.get_pos()

    #get column of mouse click (1-3)
    if(x<width/3):
        col = 1
    elif (x<width/3*2):
        col = 2
    elif(x<width):
        col = 3
    else:
        col = None

    #get row of mouse click (1-3)
    if(y<height/3):
        row = 1
    elif (y<height/3*2):
        row = 2
    elif(y<height):
        row = 3
    else:
        row = None
    #print(row,col)

    if(row and col and TTT[row-1][col-1] is None):
        global XO

        #draw the x or o on screen
        drawXO(row,col)
        check_win()

def reset_game():
    global TTT, winner,XO, draw
    time.sleep(3)
    XO = 'x'
    draw = False
    game_open()
    winner=None
    TTT = [[None]*3,[None]*3,[None]*3]

#Initialize Global Variables
#Game Variables
xo = "x"
winner = None
draw = False

#Window Variables
width = 400
height = 400
white = (255, 255, 255) #RGB
line_color = (10, 10, 10) #RGB as well

#The 3x3 board that is going to be used
TTT = [[None] * 3, [None] * 3, [None] * 3]

#Pygame Window
pygame.init()
fps = 30
clock = pygame.time.Clock()
screen = pygame.display.set_mode((width, height + 100), 0, 32)
pygame.display.set_caption("Tic Tac Toe")

#loading the images
opening = pygame.image.load('tic tac opening.png')
x_img = pygame.image.load('x.png')
o_img = pygame.image.load('o.png')


#resizing images
x_img = pygame.transform.scale(x_img, (80,80))
o_img = pygame.transform.scale(o_img, (80,80))
opening = pygame.transform.scale(opening, (width, height+100))

game_open()

# run the game loop forever
while(True):
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            # the user clicked; place an X or O
            userClick()
            if(winner or draw):
                reset_game()

    pygame.display.update()
    clock.tick(fps)
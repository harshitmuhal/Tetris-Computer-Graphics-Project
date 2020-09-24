#!/usr/bin/env python
# coding: utf-8

# In[4]:


import pygame
import random

pygame.init()

# GLOBALS VARS
s_width = 1000
s_height = 700
play_width = 300
play_height = 600
block_size = 30

top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height

S = [['.....',
      '......',
      '..00..',
      '.00...',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

shapes = [S, Z, I, O, J, L, T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]

class Piece(object):
    # x= current x coordinate of piece
    # y=current y coordinate of piece
    # rotation = integer variable to specify current orientation
    # shape = list of all possible orientations for particular piece
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0

def create_grid(locked_pos={}):
    BLACK=(0,0,0)
    grid = [[BLACK for _ in range(10)] for _ in range(20)]
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_pos:
                c = locked_pos[(j,i)]
                grid[i][j] = c
    return grid

# translate shape of a piece into a form that the computer can understand.
def convert_shape_format(shape):
    #shape is an object of class Piece
    positions = []
    format = shape.shape[shape.rotation % len(shape.shape)]
    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((shape.x + j, shape.y + i))
    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)
    return positions

def valid_space(shape, grid):
    accepted_pos = [[(j, i) for j in range(10) if grid[i][j] == (0,0,0)] for i in range(20)]
    accepted_pos = [j for sub in accepted_pos for j in sub]
    formatted = convert_shape_format(shape)
    for pos in formatted:
        if pos not in accepted_pos:
            if pos[1] > -1:
                return False
    return True

#generic function to write text on surface in the middle of screen
def draw_text_middle(surface, text, size, color):
    font = pygame.font.SysFont("comicsans", size, bold=True)
    label = font.render(text, 1, color)
    surface.blit(label, (top_left_x + play_width /2 - (label.get_width()/2), top_left_y + play_height/2 - label.get_height()/2))
    
    
# Checking if We Lose the Game
def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y <= 1:
            return True
    return False

#Get random shape from shapes list
def get_shape():
    return Piece(5, 0, random.choice(shapes))

    
#This function is used to draw grid lines to visualise grid better
def draw_grid(surface, grid):
    sx = top_left_x
    sy = top_left_y
    GREY_COLOR=(128,128,128)
    for i in range(len(grid)):
        pygame.draw.line(surface, GREY_COLOR, (sx, sy + i*block_size), (sx+play_width, sy+ i*block_size))
        for j in range(len(grid[i])):
            pygame.draw.line(surface, GREY_COLOR, (sx + j*block_size, sy),(sx + j*block_size, sy + play_height))

def draw_window(surface, grid):
    surface.fill((0, 0, 0))
    pygame.font.init()
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render('Tetris', 1, (255, 0, 255))
    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), 30))
    # current score
    font = pygame.font.SysFont('comicsans', 30)
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (top_left_x + j*block_size, top_left_y + i*block_size, block_size, block_size), 0)
    pygame.draw.rect(surface, (255, 0, 0), (top_left_x, top_left_y, play_width, play_height), 5)
    draw_grid(surface, grid)
    #pygame.display.update()

def main(win):  #
    locked_positions = {}
    grid = create_grid(locked_positions)
    change_piece = False
    run = True
    current_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    # speed at which pieces will be falling
    fall_speed = 0.1
    while run:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        #clock.get_rawtime tells us the amount of time from the last time clock was ticked
        #(clock is ticked when clock.tick() function was called = time taken by while loop to
        # complete )
        clock.tick()
        #This will control how the pieces will fall
        if fall_time/1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not(valid_space(current_piece, grid)) and current_piece.y > 0:
                #If this condition is true then piece has hit the bottom
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.x += 1
                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.x -= 1
                elif event.key == pygame.K_UP:
                    current_piece.rotation = current_piece.rotation + 1 % len(current_piece.shape)
                    if not valid_space(current_piece, grid):
                        current_piece.rotation = current_piece.rotation - 1 % len(current_piece.shape)
                        
        shape_pos = convert_shape_format(current_piece)
        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1: #when piece starts falling a portion of piece is above grid so we don't want
                # to draw that portion hence, the condition y>-1
                grid[y][x] = current_piece.color
        # if piece has hit the ground then add new piece to the game
        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = get_shape()
            change_piece = False
        draw_window(win, grid)
        pygame.display.update()
        
        if check_lost(locked_positions):
            draw_text_middle(win, "YOU LOST!", 80, (255,255,255))
            pygame.display.update()
            pygame.time.wait(1500)
            run = False
            
def draw_text_name(surface, x, y,text, size, color):
    font = pygame.font.SysFont("comicsans", size, bold=True)
    label = font.render(text, 1, color)
    surface.blit(label, (top_left_x+x , top_left_y+y))
    
#s_width = 1000
#s_height = 700
#top_left_x = 350
#top_left_y = 100
def main_menu(win):
    run = True
    while run:
        win.fill((10,250,50))
        #pygame.draw.rect(screen, [red, blue, green], [left, top, width, height], filled)
        
        pygame.draw.rect(win, (0,150,100), (top_left_x-150,50,600,600))
        pygame.display.update()
        
        text='Press Any Key To Play'
        draw_text_middle(win, text, 60, (255,255,255))
        
        t='Made by :'
        draw_text_name(win,60,0,t,40,(255,255,255))
        pygame.display.update()
        
        t='G.S.S.N.HIMABINDU 2K18/CO/127'
        draw_text_name(win,-30,100, t,30,(255,255,255))
        pygame.display.update()
        
        t='HARSHIT MUHAL 2K18/CO/145'
        draw_text_name(win,-20,150,t,30,(255,255,255))
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main(win)
        
    pygame.display.quit()

win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('Tetris')

main_menu(win)


# In[ ]:





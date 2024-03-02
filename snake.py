# -*- coding: utf-8 -*-
"""
Created on Wed May 25 20:53:26 2022

@author: dylan
"""

import pygame
import random
import time
import sys

snake_speed = 15
width = 720
height = 480

black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

pygame.init()
pygame.display.set_caption('Snake')
window = pygame.display.set_mode((width, height))
fps = pygame.time.Clock()

snake_pos = [600, 50]
snake_body = [[600, 50], [610, 50], [620, 50], [630, 50]]
fruit_pos = [random.randrange(1, (width//10)) * 10, random.randrange(1, (height//10))*10]
fruit_spawn = True
direction = 'left'
score = 0

def show_score(choice, color, font, size):
   
    # creating font object score_font
    score_font = pygame.font.SysFont(font, size)
     
    # create the display surface object
    # score_surface
    score_surface = score_font.render('Score : ' + str(score), True, color)
     
    # create a rectangular object for the
    # text surface object
    score_rect = score_surface.get_rect()
     
    # displaying text
    window.blit(score_surface, score_rect)

def game_over():
   
    # creating font object my_font
    my_font = pygame.font.SysFont('times new roman', 50)
     
    # creating a text surface on which text
    # will be drawn
    game_over_surface = my_font.render('Your Score is : ' + str(score), True, red)
     
    # create a rectangular object for the text
    # surface object
    game_over_rect = game_over_surface.get_rect()
     
    # setting position of the text
    game_over_rect.midtop = (width/2, height/4)
     
    # blit will draw the text on screen
    window.blit(game_over_surface, game_over_rect)
    pygame.display.flip()
     
    # after 2 seconds we will quit the
    # program
    time.sleep(2)
     
    # deactivating pygame library
    pygame.quit()
     
    # quit the program
    sys.exit()

while (True):
    for event in pygame.event.get():
        if (event.type == pygame.KEYDOWN):
            if (event.key == pygame.K_DOWN) & (direction != 'up'):
                direction = 'down'
            elif (event.key == pygame.K_UP) & (direction != 'down'):
                direction = 'up'
            elif (event.key == pygame.K_LEFT) & (direction != 'right'):
                direction = 'left'
            elif (event.key == pygame.K_RIGHT) & (direction != 'left'):
                direction = 'right'
                
    if direction == 'up':
        snake_pos[1] -= 10
    elif direction == 'down':
        snake_pos[1] += 10
    elif direction == 'left':
        snake_pos[0] -= 10
    else:
        snake_pos[0] += 10
        
    snake_body.insert(0, list(snake_pos))
    if snake_pos[0] == fruit_pos[0] and snake_pos[1] == fruit_pos[1]:
        score+=1
        fruit_spawn = False
    else:
        snake_body.pop()
        
    if not fruit_spawn:
        fruit_pos = [random.randrange(1, (width//10)) * 10, random.randrange(1, (height//10))*10]
    fruit_spawn= True
        
    window.fill(black)
    
    for pos in snake_body:
        pygame.draw.rect(window, green, pygame.Rect(pos[0], pos[1], 10, 10))
        
    pygame.draw.rect(window, white, pygame.Rect(
        fruit_pos[0], fruit_pos[1], 10, 10))
 
        
    if snake_pos[0] < 0 or snake_pos[0] > width-10:
        game_over()
    if snake_pos[1] < 0 or snake_pos[1] > height-10:
        game_over()
     
    # Touching the snake body
    for block in snake_body[1:]:
        if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
            game_over()
     
    # displaying score countinuously
    show_score(1, white, 'times new roman', 20)
     
    # Refresh game screen
    pygame.display.update()
 
    # Frame Per Second /Refresh Rate
    fps.tick(snake_speed)
        
        
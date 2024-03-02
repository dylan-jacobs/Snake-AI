# -*- coding: utf-8 -*-
"""
Created on Thu May 26 11:34:34 2022

@author: dylan
"""

# -*- coding: utf-8 -*-
"""
Created on Wed May 25 20:53:26 2022

@author: dylan
"""

import pygame
import random
import time
import math
import sys
import numpy as np
from collections import deque

snake_speed = 550
width = 720
height = 480

black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

class snake:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Snake')
        self.window = pygame.display.set_mode((width, height))
        self.fps = pygame.time.Clock()
        self.prev_moves = deque(maxlen=4)
        for i in range(0, 4):
            self.prev_moves.append([0, 0, 0])
        self.reset()
        
    def reset(self):
        self.frame = 0
        self.snake_pos = [600, 50]
        self.snake_body = [[600, 50], [610, 50], [620, 50], [630, 50]]
        self.fruit_pos = [random.randrange(1, (width//10)) * 10, random.randrange(1, (height//10))*10]
        while self.fruit_pos in self.snake_body:
            self.fruit_pos = [random.randrange(1, (width//10)) * 10, random.randrange(1, (height//10))*10]
        self.fruit_spawn = True
        self.direction = 'left'
        self.score = 0

    def show_score(self, choice, color, font, size):
       
        # creating font object score_font
        score_font = pygame.font.SysFont(font, size)
         
        # create the display surface object
        # score_surface
        score_surface = score_font.render('Score : ' + str(self.score), True, color)
         
        # create a rectangular object for the
        # text surface object
        score_rect = score_surface.get_rect()
         
        # displaying text
        self.window.blit(score_surface, score_rect)
        
    def move(self, move):
        # Action
        # straight = [1, 0, 0]
        # right = [0, 1, 0]
        # left = [0, 0, 1]
        
        clockwise = ['right', 'up', 'left', 'down']
        i = clockwise.index(self.direction)
        if (np.array_equal(move, [1, 0, 0])):
            new_dir = clockwise[i]
        if (np.array_equal(move, [0, 1, 0])):
            new_dir = clockwise[(i - 1) % 4]
        if (np.array_equal(move, [0, 0, 1])):
            new_dir = clockwise[(i + 1) % 4]
        self.direction = new_dir
        if self.direction == 'up':
            self.snake_pos[1] -= 10
        elif self.direction == 'down':
            self.snake_pos[1] += 10
        elif self.direction == 'left':
            self.snake_pos[0] -= 10
        else:
            self.snake_pos[0] += 10
     
    def step(self, action):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
                pygame.quit()
        self.frame+=1
        self.move(action)    
        
        if (action != [1, 0, 0]):
            self.prev_moves.append(action)
            
        self.snake_body.insert(0, list(self.snake_pos))
        reward = 0
        
        if (self.is_touching_self() and self.is_same_move(action)): # boxed itself in
            print("boxed in!")
            reward = -5 # important to set this rather than just subtract from initial value 
                        # because we only want to decrease by 7 ONCE if the head is close to any other part of its body
        if self.is_collision() or self.frame > 100 * len(self.snake_body):
            reward -= 10
            return reward, self.score, True
        
        if self.snake_pos[0] == self.fruit_pos[0] and self.snake_pos[1] == self.fruit_pos[1]:
            self.score+=1
            reward += 10
            self.fruit_spawn = False
        else:
            self.snake_body.pop()
            
        
            
        if not self.fruit_spawn:
            self.fruit_pos = [random.randrange(1, (width//10)) * 10, random.randrange(1, (height//10))*10]
            while (self.fruit_pos == self.snake_body):
                self.fruit_pos = [random.randrange(1, (width//10)) * 10, random.randrange(1, (height//10))*10]
        self.fruit_spawn = True
            
        self.window.fill(black)
        
        for pos in self.snake_body:
            pygame.draw.rect(self.window, green, pygame.Rect(pos[0], pos[1], 10, 10))
            
        pygame.draw.rect(self.window, white, pygame.Rect(
            self.fruit_pos[0], self.fruit_pos[1], 10, 10))
       
        # displaying score countinuously
        self.show_score(1, white, 'times new roman', 20)
         
        # Refresh game screen
        pygame.display.update()
     
        # Frame Per Second /Refresh Rate
        self.fps.tick(snake_speed)
        
        return reward, self.score, False
       
    def is_collision(self, ind=None):
        if ind is None:
            ind = self.snake_body[0]
            
        if ind[0] < 0 or ind[0] > width-10:
            return True
        if ind[1] < 0 or ind[1] > height-10:
            return True
         
        # Touching the snake body
        for block in self.snake_body[1:]:
            if ind[0] == block[0] and ind[1] == block[1]:
                return True
        return False
    
    def is_touching_self(self):
        for block in self.snake_body[2:]:
            if (block == [self.snake_pos[0] + 10, self.snake_pos[1]]) or (block == [self.snake_pos[0] - 10, self.snake_pos[1]]) or (block == [self.snake_pos[0], self.snake_pos[1] + 10]) or (block == [self.snake_pos[0], self.snake_pos[1] - 10]):
                return True 
            
        return False
    
    def is_same_move(self, new_move):
        return new_move == self.prev_moves[0] == self.prev_moves[1] == self.prev_moves[2] != [0,0,0] != [1, 0, 0]



            
            
# -*- coding: utf-8 -*-
"""
Created on Thu May 26 12:18:42 2022

@author: dylan
"""

import torch 
import random 
import numpy as np
import pandas as pd
from collections import deque
from snakeai import snake, width, height
from model import Linear_QNet, QTrainer
from Helper import plot

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class Agent: 
    def __init__(self):
        self.n_game = 0
        self.epsilon = 80 # randomness
        self.gamma = 0.9 # discount rate
        self.memory = deque(maxlen=MAX_MEMORY)
        self.model = Linear_QNet(15, 256, 3)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

        
    # state (11 Values)
    #[ danger straight, danger right, danger left,
    #   
    # direction left, direction right,
    # direction up, direction down
    # 
    # food left,food right,
    # food up, food down]
    
    def get_state(self, game, record):
        head = game.snake_body[0]
        up = [head[0], head[1] - 10]
        down = [head[0], head[1] + 10]
        left = [head[0] - 10, head[1]]
        right = [head[0] + 10, head[1]]
        
        dir_up = game.direction == 'up'
        dir_down = game.direction == 'down'
        dir_left = game.direction == 'left'
        dir_right = game.direction == 'right'
        
        state = [
            # danger straight
            (dir_up and game.is_collision(up)) or
            (dir_down and game.is_collision(down)) or
            (dir_left and game.is_collision(left)) or
            (dir_right and game.is_collision(right)),
            
            # danger right
            (dir_up and game.is_collision(right)) or
            (dir_down and game.is_collision(left)) or
            (dir_left and game.is_collision(up)) or
            (dir_right and game.is_collision(down)),
            
            # danger left
            (dir_up and game.is_collision(left)) or
            (dir_down and game.is_collision(right)) or
            (dir_left and game.is_collision(down)) or
            (dir_right and game.is_collision(up)),
            
            # move dir
            dir_up,
            dir_down,
            dir_left,
            dir_right,
            
            # apple info
            game.fruit_pos[0] < head[0],
            game.fruit_pos[0] > head[0],
            game.fruit_pos[1] < head[1],
            game.fruit_pos[1] > head[1],
            
            # best score
            (record + 3) / (width * height),
            
            game.is_touching_self() and game.is_same_move([0, 1, 0]),
            game.is_touching_self() and game.is_same_move([0, 0, 1]),
            
            game.frame / (len(game.snake_body) * 100)
            
        ]
        return np.array(state,dtype=float)
        
    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward,next_state, done))
        
    def train_long_memory(self):
        if (len(self.memory) > BATCH_SIZE):
            mini_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            mini_sample = self.memory 
            
        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)
        
    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)
    
    def get_action(self, state):
        final_move = [0, 0, 0]
        if (random.randint(0,200) < self.epsilon - self.n_game):
            move = random.randint(0, 2)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state,dtype=torch.float).cuda()
            prediction = self.model(state0).cuda()
            move = torch.argmax(prediction).item()
            final_move[move] = 1
        return final_move
   
dead_states = []
def train(load, train):
    agent = Agent()
    if load:
        agent.model.load_state_dict(torch.load('model.pth'))
        agent.epsilon = 0
    plot_scores = []
    plot_mean_scores = []
    sma = []
    total_score = 0
    record = 0
    game = snake()
    
    while True:
        
        state_old = agent.get_state(game, record)
        final_move = agent.get_action(state_old)
        
        reward, score, done = game.step(final_move)
        if (score > record):
            reward += 0

        state_new = agent.get_state(game, record)
        
        if train:
            agent.train_short_memory(state_old, final_move, reward, state_new, done)
            agent.remember(state_old, final_move, reward, state_new, done)
            
        if done:
            dead_states.append(state_old)
            game.reset()
            agent.n_game += 1
            if train:
                agent.train_long_memory()
                if (score > record and train):
                    agent.model.save()
                    print('Model saved!')
                    record = score
                print('Game:', agent.n_game, 'Score:', score, 'Record:', record)
            
            plot_scores.append(score)
            total_score+=score
            sma1 = pd.DataFrame(plot_scores).rolling(10)
            sma.append(sma1)
            mean_score = total_score / agent.n_game
            plot_mean_scores.append(mean_score)
            if agent.n_game < 1000:
                plot(plot_scores, plot_mean_scores)
            else:
                plot(plot_scores, sma)
            
        
if __name__=="__main__":
    train(load=False, train=True)  
   
        
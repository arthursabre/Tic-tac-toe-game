import random
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame as pg 
from pygame import mixer
import pygame_menu
import sys 
import csv
import time 
from pygame.locals import *
import qlearning as ql



def demo_game_stats(agent):
    results = [agent.demo_game() for i in range(10000)]
    game_stats = {k: results.count(k) /100 for k in ['W', 'L', 'D']}
    print('     percentage results: {}'.format(game_stats))

agent = ql.Agent(ql.TicTacToe, epsilon =0.5, alpha = 0.2)
print("gamma= "+str(agent.gamma))
print('Before learning')
demo_game_stats(agent)

agent.learning_episode(1000)
print('after 1000 learning games, '+"epsilon = "+str(agent.epsilon)+" ,alpha = "+str(agent.alpha))
demo_game_stats(agent)


agent.learning_episode(4000)
print('after 4000 learning games, '+"epsilon = "+str(agent.epsilon)+" ,alpha = "+str(agent.alpha))
demo_game_stats(agent)

agent.learning_episode(5000)
print('after 5000 learning games, '+"epsilon = "+str(agent.epsilon)+" ,alpha = "+str(agent.alpha))
demo_game_stats(agent)
agent.epsilon=0.4

agent.learning_episode(10000)
print('after 10000 learning games, '+"epsilon = "+str(agent.epsilon)+" ,alpha = "+str(agent.alpha))
demo_game_stats(agent)


agent.learning_episode(10000)
print('after 10000 learning games, '+"epsilon = "+str(agent.epsilon)+" ,alpha = "+str(agent.alpha))
demo_game_stats(agent)
agent.epsilon=0.2

agent.learning_episode(20000)
print('after 20000 learning games, '+"epsilon = "+str(agent.epsilon)+" ,alpha = "+str(agent.alpha))
demo_game_stats(agent)
agent.epsilon=0.1

agent.learning_episode(50000)
print('after 50000 learning games, '+"epsilon = "+str(agent.epsilon)+" ,alpha = "+str(agent.alpha))
demo_game_stats(agent)

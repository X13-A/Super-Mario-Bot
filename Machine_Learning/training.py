from pygame.locals import *
import pygame
from state import State
from settings import USE_KEYBOARD
from settings import SHOW_MINI_DISPLAY

class Training():
    def __init__(self, env, ram):
        self.env = env
        self.ram = ram
        self.done = True
        self.max_fitness = 0
        self.fitness = 0
        self.state = State()

    def getManualAction(self):
        action = 0
        keys = pygame.key.get_pressed()
        if keys[K_RIGHT] and keys[K_SPACE] and keys[K_LSHIFT]:
            action = 4  # Move right, jump and run
        elif keys[K_RIGHT] and keys[K_SPACE]:
            action = 2  # Move right and jump
        elif keys[K_RIGHT] and keys[K_LSHIFT]: 
            action = 3 # Move right and run
        elif keys[K_RIGHT]:
            action = 1  # Move right
        elif keys[K_LEFT]:
            action = 6 # Move left
        elif keys[K_SPACE]:
            action = 5  # Jump
        return action

    def getNextAction(self):
        # TODO: Use Q-Table or explore to pick action
        return self.env.action_space.sample()
    
    def update(self):
        if self.done:
            self.env.reset()
            self.fitness = 0
            if (self.fitness > self.max_fitness): self.max_fitness = self.fitness 
        
        if USE_KEYBOARD and SHOW_MINI_DISPLAY: action = self.getManualAction()
        else: action = self.getNextAction()

        frame, reward, self.done, truncated, info = self.env.step(action)
        self.state.update(self.ram)
        self.fitness += reward
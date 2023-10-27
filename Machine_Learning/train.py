from pygame.locals import *
import pygame
from state import State

class Training():
    def __init__(self, env, smb, ram):
        self.env = env
        self.q_table = self.initQTable()
        self.smb = smb
        self.ram = ram
        self.done = True
        self.step = 0
        self.max_fitness = 0
        self.fitness = 0
        self.state = State(self)

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
    
    # TODO: Get rid of gym environment and use nes_py instead
    def update(self):
        if self.done:
            self.env.reset()
            self.fitness = 0
            if (self.fitness > self.max_fitness): self.max_fitness = self.fitness 
        
        action = self.getManualAction()
        # action = self.getNextAction()

        gym_state, reward, self.done, truncated, info = self.env.step(action)
        self.state.update()

        self.fitness += reward
        self.env.render()
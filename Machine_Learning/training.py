from pygame.locals import *
import pygame
from state import State
from qTable import QTable
from settings import USE_KEYBOARD
from settings import SHOW_MINI_DISPLAY
from settings import EPSILON_START
from settings import EPSILON_SCALING
from settings import EPSILON_MIN
from settings import MAX_STUCK_TIME
import random

class Training():
    def __init__(self, env, ram):
        self.env = env
        self.ram = ram
        self.done = True
        self.max_fitness = 0
        self.fitness = 0
        self.state = State()
        self.q_table = QTable()
        self.alpha = 0.1
        self.gamma = 0.9
        self.epsilon = EPSILON_START

        self.last_pos = 0
        self.stuck_time = 0

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

    def getNextAction(self,epsilon):
        # Si on tire un nombre aléatoire inférieur à epsilon, on explore.
        if random.uniform(0, 1) < epsilon:
            return self.env.action_space.sample()
        else:
            # Sinon, on exploite en choisissant l'action avec la valeur Q la plus élevée pour l'état donné.
            state_combination = self.q_table.Q[str(self.state.combination())]
            return int(max(state_combination, key=state_combination.get))

    
    def update(self):
        if self.done:
            print("### DONE ###")
            print("Fitness: ", self.fitness)
            print("Epsilon: ", self.epsilon)
            self.q_table.saveQ()
            self.env.reset()
            if (self.fitness > self.max_fitness): self.max_fitness = self.fitness 
            self.fitness = 0
            print("Max fitness: ", self.max_fitness)
            print("")
            self.done = False

        if USE_KEYBOARD and SHOW_MINI_DISPLAY: action = self.getManualAction()
        else: action = self.getNextAction(self.epsilon)

        self.epsilon *= EPSILON_SCALING
        if (self.epsilon < EPSILON_MIN): self.epsilon = EPSILON_MIN
        frame, reward, done, truncated, info = self.env.step(action)

        # Stuck detection
        if (self.last_pos == info["x_pos"]): self.stuck_time += 1
        else: self.stuck_time = 0
        self.last_pos = info["x_pos"]

        # Workaround because done is not working
        self.done = info["life"] < 2 or self.stuck_time > 60 * MAX_STUCK_TIME

        old_state = self.state
        self.state.update(self.ram)
        if (reward < 0): reward *= 2

        self.q_table.update(old_state,self.state,action,self.gamma,self.alpha,reward)
        self.fitness += reward
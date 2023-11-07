from pygame.locals import *
import pygame
from state import State
from qTable import QTable
from utils import SMB

from settings import USE_KEYBOARD
from settings import SHOW_MINI_DISPLAY
from settings import EPSILON_START
from settings import EPSILON_SCALING
from settings import EPSILON_MIN
from settings import MAX_STUCK_TIME
from settings import SPEEDRUN_ACTIONS
from settings import ENABLE_TRAINING
import random
from debug import get_time_ms
from debug import ms_to_time_str

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

        self.last_x_pos = 0
        self.last_y_pos = 0
        self.stuck_time = 0
        self.just_hit_ground = False
        self.last_mario_state = "grounded"
        self.wins = 0
        self.run = 0
        self.run_start_time = get_time_ms()

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
        if self.just_hit_ground:
            return SPEEDRUN_ACTIONS[0], -1 # Don't spam jump
        # elif self.state.obstacle < 3: # Force jump if in front of obstacle
        #     return SPEEDRUN_ACTIONS[2], 2 - 1 # -1 because we ignore the first "DO NOTHING" action
        elif random.uniform(0, 1) < epsilon:
            index = random.randint(1, len(SPEEDRUN_ACTIONS)-1)
            return SPEEDRUN_ACTIONS[index], index-1 # -1 because we ignore the first "DO NOTHING" action
        else:
            # Sinon, on exploite en choisissant l'action avec la valeur Q la plus élevée pour l'état donné.
            state_combination = self.q_table.Q[str(self.state.combination())]
            index = int(max(state_combination, key=state_combination.get))
            return SPEEDRUN_ACTIONS[index + 1], index # +1 because we ignore the first "DO NOTHING" action

    def reset_env(self):
        run_duration = get_time_ms() - self.run_start_time
        self.fitness = self.last_x_pos - (run_duration//200)
        self.run_start_time = get_time_ms()

        self.q_table.saveQ()
        self.env.reset()

        if (self.fitness > self.max_fitness): self.max_fitness = self.fitness 
        if (self.fitness > 2800): self.wins += 1

        print(f"[Run {self.run}] Fitness: {self.fitness}/{self.max_fitness} in {ms_to_time_str(run_duration)} ({self.get_win_rate()}% win rate)")
        
        self.fitness = 0

        self.done = False
        self.run += 1

    def get_win_rate(self):
        if self.run == 0: return 0
        return (int) ((self.wins / self.run) * 100)

    def update(self):
        old_state = self.state
        self.state.update(self.ram)

        if self.done: self.reset_env()

        mario_state = SMB.get_mario_state(self.ram)
        self.just_hit_ground = self.last_mario_state == "floating" and mario_state == "grounded"
        self.last_mario_state = mario_state

        if USE_KEYBOARD and SHOW_MINI_DISPLAY: action = self.getManualAction()
        else: action, action_index = self.getNextAction(self.epsilon)

        self.epsilon *= EPSILON_SCALING
        if (self.epsilon < EPSILON_MIN): self.epsilon = EPSILON_MIN
        frame, reward, done, truncated, info = self.env.step(action)

        # Stuck detection
        if (self.last_x_pos == info["x_pos"]): self.stuck_time += 1
        else: self.stuck_time = 0
        self.last_x_pos = info["x_pos"]

        # Reward calculation
        if (reward < 0): reward *= 4
        if (reward == 0): 
            reward = -2 # Penalty when not moving right
            if (info["y_pos"] > self.last_y_pos): 
                reward += 1 # Little bonus when not moving but jumping

        self.last_y_pos = info["y_pos"]
        
        # Workaround because done is not working
        self.done = done or info["life"] < 2 or self.stuck_time > 60 * MAX_STUCK_TIME
        if not USE_KEYBOARD and ENABLE_TRAINING and action_index != -1:
            self.q_table.update(old_state,self.state,action_index,self.gamma,self.alpha,reward)
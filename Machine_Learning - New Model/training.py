from pygame.locals import *
import pygame
from state import State
from qTable import QTable
from utils import SMB
import copy
from settings import EPSILON_START
from settings import EPSILON_SCALING
from settings import EPSILON_MIN
from settings import MAX_STUCK_TIME
from settings import SPEEDRUN_ACTIONS
from settings import ENABLE_TRAINING
from settings import STAND_STILL_PENALTY
from settings import FRAMES_BEFORE_UPDATE
from settings import IDLE_ACTION
from settings import GAMMA
from settings import ALPHA
from settings import DEATH_PENALTY
import json
import random
from debug import get_time_ms

class StateActionBuffer():
    def __init__(self, jump_frame):
        self.buffer = []
        self.jump_frame = jump_frame
        self.land_frame = -1

    def set_land_frame(self, land_frame):
        self.land_frame = land_frame

    def append(self, state_action):
        self.buffer.append(state_action)
    
    def is_expired(self, frame, lifespan):
        return self.land_frame != -1 and frame - self.land_frame > lifespan

    def get_buffer(self):
        return self.buffer


class LatestBufferTracker():
    def __init__(self, lifespan):
        self.buffers = []
        self.lifespan = lifespan
        self.last_update_frame = 0

    def create_buffer(self, jump_frame):
        self.buffers.append(StateActionBuffer(jump_frame))

    def get_latest_buffer(self, frame):
        n_buffers = len(self.buffers)
        if n_buffers == 0: return None

        # Get the most recent buffer that is old enough 
        search_start = frame - self.lifespan

        for i in range(n_buffers - 1, -1, -1):
            buffer = self.buffers[i]
            if buffer.jump_frame <= search_start: 
                return buffer

        return self.buffers[n_buffers - 1]
    
    def reset(self):
        self.buffers.clear()

    def update(self, frame, state_action, last_jump_frame, last_hit_ground_frame):
        # Update all buffers
        if last_jump_frame > self.last_update_frame:
            self.buffers.append(StateActionBuffer(last_jump_frame))

        for buffer in self.buffers:
            buffer.append(state_action)
            if(last_hit_ground_frame > self.last_update_frame and buffer.land_frame == -1): 
                buffer.set_land_frame(last_hit_ground_frame)
        
        # Filter expired buffers
        temp = len(self.buffers)
        self.buffers = [buffer for buffer in self.buffers if not buffer.is_expired(frame, self.lifespan)]
        deleted = temp - len(self.buffers)

        self.last_update_frame = frame


class Training():
    def __init__(self, env, ram):
        self.env = env
        self.ram = ram
        self.done = True
        self.max_fitness = 0
        self.fitness = 0
        self.state = State(self)
        self.q_table = QTable()
        self.alpha = ALPHA
        self.gamma = GAMMA
        self.epsilon = EPSILON_START

        self.last_state_action = (None, None)
        self.state_action_buffer = LatestBufferTracker(FRAMES_BEFORE_UPDATE)

        self.last_x_pos = 0
        self.last_y_pos = 0
        self.stuck_time = 0
        self.last_mario_state = "grounded"
        self.frame = 0
        self.wins = 0
        self.run = 0
        self.run_start_time = get_time_ms()
        
        self.just_hit_ground = False
        self.just_jumped = False
        self.last_hit_ground_frame = -1
        self.last_jump_frame = -1

        self.active_action = (0, 0) # (action, index)
        self.last_state = None
        self.active_reward = 0
        self.must_train_asap = False

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
        if random.uniform(0, 1) < epsilon:
            index = random.randint(0, len(SPEEDRUN_ACTIONS) - 1)
            return SPEEDRUN_ACTIONS[index], index
        else:
            # On exploite en choisissant l'action avec la valeur Q la plus élevée pour l'état donné.
            state_combination = self.q_table.Q[str(self.state.combination())]
            index = int(max(state_combination, key=state_combination.get))
            return SPEEDRUN_ACTIONS[index], index

    def log_highscore(self):
        file_path = 'score_graph.json'
        with open(file_path, 'r') as file:
            data = json.load(file)
        
        new_entry = {"run": len(data), "fitness": int(self.fitness),"max_fitness": int(self.max_fitness)}
        data.append(new_entry)
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)


    def reset_env(self):
        self.state_action_buffer.reset()
        self.frame = 0
        self.active_reward = 0
        self.fitness = self.last_x_pos # - (self.frame//10)
        self.run_start_time = get_time_ms()

        self.q_table.saveQ()
        if self.run % 200 == 0:
            self.q_table.backupQ()
        self.env.reset()

        if (self.fitness > self.max_fitness): self.max_fitness = self.fitness 
        if (self.fitness > 2800): self.wins += 1

        if self.run > 0:
            self.log_highscore()

        print(f"[Run {self.run}] Fitness: {self.fitness}/{self.max_fitness} ({self.wins} wins)")
        
        self.fitness = 0

        self.done = False
        self.run += 1
        self.state.update(self.ram)
        self.last_state = copy.copy(self.state)

    def get_win_rate(self):
        if self.run == 0: return 0
        return (int) ((self.wins / self.run) * 100)

    def back_propagate_jump(self):
        state_action_set = {}

        latest_buffer = self.state_action_buffer.get_latest_buffer(self.frame)
        if not latest_buffer: return
        
        for state_action in latest_buffer.get_buffer():
            state_action_str = str(state_action)
            if not state_action_set.get(state_action_str):
                state_action_set[state_action_str] = state_action
        
        for key in state_action_set:
            state = state_action_set[key][0]
            action = state_action_set[key][1]
            self.q_table.Q[str(state)][str(action)] -= 1

    def detect_stuck(self, pos):
        if (self.last_x_pos == pos): self.stuck_time += 1
        else: self.stuck_time = 0

    def adjust_reward(self, reward, info):
        if (reward == -15): reward = DEATH_PENALTY
        if (reward == 5): reward *= 10 #TODO: back propagate to all level when winnning
        if (reward == 0):
            reward = STAND_STILL_PENALTY # Penalty when not moving right
            if (info["y_pos"] > self.last_y_pos): 
                reward += 1 # Little bonus when not moving but jumping
        return reward
    
    def is_done(self, done, info):
        # Workaround because done is not always working
        return done or info["life"] < 2 or self.stuck_time > 60 * MAX_STUCK_TIME
        
    def fill_buffer(self, action_index):
        # # TODO: Fix when repeating jump
        # if self.just_jumped and self.last_state_action[0]:
        #     self.state_action_buffer.update(self.frame, self.last_state_action, self.frame)
        # if self.just_hit_ground:
        #     self.state_action_buffer.clear()
        # if self.last_mario_state == "floating" or self.frames_since_hit_ground < 10:
        #     self.state_action_buffer.append((self.state.combination(), action_index))

        # self.last_state_action = self.state.combination(), action_index
        pass

    def fill_buffers(self):
        state_action = (self.last_state.combination(), self.active_action[1])
        self.state_action_buffer.update(self.frame, state_action, self.last_jump_frame, self.last_hit_ground_frame)

    def should_train(self):
        return ENABLE_TRAINING and (self.done or self.frame % FRAMES_BEFORE_UPDATE == 0)

    def set_jump_state(self):
        mario_state = SMB.get_mario_state(self.ram)
        self.just_hit_ground = self.last_mario_state == "floating" and mario_state == "grounded"
        self.just_jumped = self.last_mario_state == "grounded" and mario_state == "floating"
        self.last_mario_state = mario_state

        if self.just_hit_ground:
            self.last_hit_ground_frame = self.frame
        if self.just_jumped:
            self.last_jump_frame = self.frame - 1

    def update(self):
        if self.done: 
            self.reset_env()
        self.set_jump_state()

        action, action_index = self.active_action[0], self.active_action[1]
        if self.just_hit_ground:
            action, action_index = IDLE_ACTION, -1 # Don't spam jump
            
        frame, reward, done, truncated, info = self.env.step(action)

        self.detect_stuck(info["x_pos"])

        # Set reward
        reward = self.adjust_reward(reward, info)        
        if (reward == DEATH_PENALTY):
            self.active_reward = reward
        else: self.active_reward += reward

        self.last_x_pos = info["x_pos"]
        self.last_y_pos = info["y_pos"]
        self.done = self.is_done(done, info) 
        
        # Might seem unnecessary but it really is (bad architecture)
        must_train_asap_temp = self.must_train_asap
        should_train = self.should_train()

        if must_train_asap_temp or should_train:
            self.epsilon *= EPSILON_SCALING
            if (self.epsilon < EPSILON_MIN): self.epsilon = EPSILON_MIN

            # Update QTable
            self.fill_buffers()
            self.state.update(self.ram)
            self.q_table.update(
                self.last_state,
                self.state,
                self.active_action[1],
                self.gamma,
                self.alpha,
                self.active_reward
            )

            # Make next action
            train_action, action_index = self.getNextAction(self.epsilon)
            self.active_action = (train_action, action_index)

            if self.active_reward == DEATH_PENALTY:
                self.back_propagate_jump()

            self.last_state = copy.copy(self.state)
            self.active_reward = 0

        self.frame += 1
from utils import StaticTileType
import numpy as np
from pygame.locals import * # Import the constant for the right arrow key
import pygame
from itertools import product

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

    def getObstacleDist(self, tiles, mario_pos):
        if (mario_pos[0] >= tiles.shape[0] or mario_pos[1] >= tiles.shape[1]): return tiles.shape[1]
        if (mario_pos[0] < 0 or mario_pos[1] < 0): return tiles.shape[1]
        
        mario_row = tiles[mario_pos[0], mario_pos[1]:]
        obstacles = np.where(mario_row == StaticTileType.Fake)[0]
        
        if (obstacles.size): return obstacles[0]
        return tiles.shape[1]

    def getHoleDist(self, tiles, mario_pos):
        if (mario_pos[0] >= tiles.shape[0] or mario_pos[1] >= tiles.shape[1]): return tiles.shape[1]
        if (mario_pos[0] < 0 or mario_pos[1] < 0): return tiles.shape[1]
        
        bottom_row = tiles[-1, mario_pos[1]:]
        holes = np.where(bottom_row == StaticTileType.Empty)[0]

        if (holes.size): return holes[0]
        return tiles.shape[1]
    
    def getEnemyDist(self, mario_pos_in_level):
        mario_x_in_level, mario_y_in_level = mario_pos_in_level
        
        enemies = self.smb.get_enemy_locations(self.ram)
        forward_enemies = [enemy for enemy in enemies if enemy.location.x >= mario_x_in_level]

        if (not forward_enemies): return (16, 16)
        
        closest_enemy = min(forward_enemies, key=lambda e: (e.location.x - mario_x_in_level)**2 + (e.location.y - mario_y_in_level)**2)
        dx = round((closest_enemy.location.x - mario_x_in_level)/16)
        dy = round((closest_enemy.location.y - mario_y_in_level)/16)
        return (dx,dy)

    def setState(self):
        tiles = self.smb.get_tiles_array(self.ram)
        mario_pos_in_grid = self.smb.get_mario_row_col(self.ram)
        mario_pos_in_level = self.smb.get_mario_location_in_level(self.ram)

        obstacle = self.getObstacleDist(tiles, mario_pos_in_grid)
        hole = self.getHoleDist(tiles, mario_pos_in_grid)
        enemy = self.getEnemyDist(mario_pos_in_level)

    def getManualAction(self):
        action = 0
        keys = pygame.key.get_pressed()  # Get the state of all keys
        if keys[K_RIGHT] and keys[K_SPACE]:  # Right arrow + Space
            action = 2  # Move right and jump
        elif keys[K_RIGHT]:  # Right arrow
            action = 1  # Move right
        elif keys[K_LEFT] and keys[K_SPACE]:  # Left arrow + Space
            action = 4  # Currently, there's no "Move left and jump" in SIMPLE_MOVEMENT. This will just move left.
        elif keys[K_LEFT]:  # Left arrow
            action = 4  # Move left
        elif keys[K_SPACE]:  # Space
            action = 3  # Jump
        return action

    def update(self):
        if self.done:
            state = self.env.reset()
            self.fitness = 0
            if self.fitness > self.max_fitness:
                self.max_fitness = self.fitness 
        action = self.env.action_space.sample()
        action = self.getManualAction()

        state, reward, self.done, truncated, info = self.env.step(action)
        self.fitness += reward
        self.env.render()
        self.setState()

    def initQTable(self) :
        states = ['dx_e', 'dy_e', 'dx_o', 'dx_h']
        commands = ['right', 'a', 'b']
        state_values = [1,2,3,16]
        command_values = [0, 1]

        # Générer toutes les combinaisons possibles des valeurs d'états
        all_state_combinations = list(product(state_values, repeat=len(states)))

        # Générer toutes les combinaisons possibles des valeurs de commandes
        all_command_combinations = list(product(command_values, repeat=len(commands)))

        # Combinaison des états et des commandes
        all_combinations = [state_comb + cmd_comb for state_comb in all_state_combinations for cmd_comb in all_command_combinations]

        # Convertir en une matrice numpy
        matrix = np.array(all_combinations)

        # Ajouter une colonne pour les récompenses (initialement mise à zéro)
        rewards = np.zeros((matrix.shape[0], 1))
        full_matrix = np.hstack((matrix, rewards))
        print(full_matrix.size)
        return full_matrix

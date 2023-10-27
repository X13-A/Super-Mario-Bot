from itertools import product
import numpy as np

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

    def update(self):
        if self.done:
            state = self.env.reset()
            if self.fitness > self.max_fitness:
                self.max_fitness = self.fitness  
        state, reward, self.done, truncated, info = self.env.step(self.env.action_space.sample())
        self.fitness = info["x_pos"]
        self.env.render()
    
    def getDeltaEnemy(self):
        x,y = self.smb.get_mario_location_in_level(self.ram)
        enemies = self.smb.get_enemy_locations(self.ram)
        forward_enemies = [ennemi for ennemi in enemies if ennemi.x/16 >= int(x/16)]
        dx = 16
        dy = 16
        if(len(forward_enemies)>0) :
            closest_enemy = min(forward_enemies, key=lambda e: (e.location.x - x)**2 + (e.location.y - y)**2)
            dx = round((closest_enemy.location.x - x)/16)
            dy = round((closest_enemy.location.y - y)/16)
        return (dx,dy)

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
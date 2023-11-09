import numpy as np
from itertools import product

class QTable:
    def __init__(self):
        self.state_attributes = ['dx_e', 'dy_e', 'dx_o', 'dx_h']
        self.state_values = [1,2,3,16]
        self.commands = ['right', 'a', 'b']
        self.commands_values = [0, 1]

        # Générer toutes les combinaisons possibles des valeurs d'états
        self.all_state_combinations = list(product(self.state_values, repeat=len(self.state_attributes)))

        # Générer toutes les combinaisons possibles des valeurs de commandes
        self.all_command_combinations = list(product(self.commands_values, repeat=len(self.commands)))

        # Combinaison des états et des commandes
        self.all_combinations = [state_comb + cmd_comb for state_comb in self.all_state_combinations for cmd_comb in self.all_command_combinations]

        # Convertir en une matrice numpy
        matrix = np.array(self.all_combinations)

        # Ajouter une colonne pour les récompenses (initialement mise à zéro)
        rewards = np.zeros((matrix.shape[0], 1))
        self.matrix = np.hstack((matrix, rewards))
        print(self.matrix.size)

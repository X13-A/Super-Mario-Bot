import numpy as np
from itertools import product

class QTable:
    def __init__(self):
        self.state_values = [0,1,2,3,16]
        self.state_variables = 4
        self.n_actions = 7
        self.Q = {}

        # Générer toutes les combinaisons possibles des valeurs d'états
        self.all_state_combinations = list(product(self.state_values, repeat=self.state_variables))

        for state_combination in self.all_state_combinations :
            self.Q[state_combination] = {}
            for action in range(0,self.n_actions) :
                self.Q[state_combination][action] = 0

        
    def update(self,state,next_state,action,gamma,alpha,reward):
        combination = state.combination()
        next_combination = next_state.combination()
        next_max = max(self.Q[next_combination].values())
        self.Q[state.combination()][action] += alpha*(reward+gamma*next_max-self.Q[combination][action])
        

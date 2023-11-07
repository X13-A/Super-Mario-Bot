import numpy as np
from itertools import product
import json

class QTable:
    def __init__(self):
        self.state_values = [0,1,2,3,16]
        self.state_variables = 4
        self.n_actions = 2
        try:
            with open('qTable.json', 'r') as file:
                data = json.load(file)
            # Si le fichier est vide
            if not data:
                print("Could not load Q-Table, creating new one (JSON file was empty)")
                self.Q = self.initQ()
            else:
                print("Successfully loaded Q-Table from file")
                self.Q = data
        # Si le fichier n'existe pas ou s'il y a une autre erreur
        except (FileNotFoundError, json.JSONDecodeError):
            print("Could not load Q-Table from JSON, creating new one")
            self.Q = self.initQ()

    def initQ(self) : 
        Q= {}
        # Générer toutes les combinaisons possibles des valeurs d'états
        all_state_combinations = list(product(self.state_values, repeat=self.state_variables))

        for state_combination in all_state_combinations :
            Q[str(state_combination)] = {}
            for action in range(0,self.n_actions) :
                Q[str(state_combination)][str(action)] = 0
        return Q
    
    def saveQ(self):
        with open('qTable.json', 'w') as file:
            json.dump(self.Q, file)
            
    def update(self,state,next_state,action,gamma,alpha,reward):
        combination = state.combination()
        next_combination = next_state.combination()
        next_max = max(self.Q[str(next_combination)].values())
        self.Q[str(combination)][str(action)] += alpha*(reward+gamma*next_max-self.Q[str(combination)][str(action)])
        

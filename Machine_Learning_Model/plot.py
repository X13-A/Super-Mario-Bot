import matplotlib.pyplot as plt
import numpy as np
import json
from settings import WIN_SCORE

file_path = 'score_graph.json'
with open(file_path, 'r') as file:
    data = json.load(file)

runs = [item["run"] for item in data]
max_fitness = [item["max_fitness"] for item in data]
fitness = [item["fitness"] for item in data]
window_size = 500
average_fitness = [np.mean(fitness[max(i-window_size+1, 0):i+1]) for i in range(len(fitness))]
win_rate = [(sum(1 for f in fitness[max(i-window_size+1, 0):i+1] if f >= WIN_SCORE) / 
             min(window_size, i+1)) * 100 for i in range(len(fitness))]

plt.figure(figsize=(10, 6))
plt.plot(runs, max_fitness, label='Max fitness')
plt.plot(runs, average_fitness, label=f"{window_size}-run Moving Average Fitness", color='orange', linestyle='--')
plt.title('Progress of fitness over runs')
plt.xlabel('Run')
plt.ylabel('Fitness')
plt.legend()
plt.grid(True)
plt.show()

plt.figure(figsize=(10, 6))
plt.plot(runs, win_rate, label=f'{window_size}-run Win Rate', color='green', linestyle='-')
plt.title('Win Rate Over Runs')
plt.xlabel('Run')
plt.ylabel('Win Rate (%)')
plt.legend()
plt.grid(True)
plt.show()
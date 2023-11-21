import matplotlib.pyplot as plt
import numpy as np

# Provided data
data = [
    {
        "run": 0,
        "fitness": 314,
        "max_fitness": 314
    },
    {
        "run": 1,
        "fitness": 315,
        "max_fitness": 315
    },
    {
        "run": 2,
        "fitness": 701,
        "max_fitness": 701
    },
    {
        "run": 3,
        "fitness": 698,
        "max_fitness": 701
    },
    {
        "run": 4,
        "fitness": 808,
        "max_fitness": 808
    },
    {
        "run": 5,
        "fitness": 801,
        "max_fitness": 808
    },
    {
        "run": 6,
        "fitness": 700,
        "max_fitness": 808
    },
    {
        "run": 7,
        "fitness": 1130,
        "max_fitness": 1130
    },
    {
        "run": 8,
        "fitness": 700,
        "max_fitness": 1130
    },
    {
        "run": 9,
        "fitness": 1131,
        "max_fitness": 1131
    },
    {
        "run": 10,
        "fitness": 700,
        "max_fitness": 1131
    },
    {
        "run": 11,
        "fitness": 1130,
        "max_fitness": 1131
    },
    {
        "run": 12,
        "fitness": 700,
        "max_fitness": 1131
    },
    {
        "run": 13,
        "fitness": 1131,
        "max_fitness": 1131
    },
    {
        "run": 14,
        "fitness": 700,
        "max_fitness": 1131
    },
    {
        "run": 15,
        "fitness": 1130,
        "max_fitness": 1131
    },
    {
        "run": 16,
        "fitness": 700,
        "max_fitness": 1131
    },
    {
        "run": 17,
        "fitness": 1130,
        "max_fitness": 1131
    },
    {
        "run": 18,
        "fitness": 700,
        "max_fitness": 1131
    },
    {
        "run": 19,
        "fitness": 1130,
        "max_fitness": 1131
    },
    {
        "run": 20,
        "fitness": 700,
        "max_fitness": 1131
    },
    {
        "run": 21,
        "fitness": 1819,
        "max_fitness": 1819
    },
    {
        "run": 22,
        "fitness": 700,
        "max_fitness": 1819
    },
    {
        "run": 23,
        "fitness": 1130,
        "max_fitness": 1819
    },
    {
        "run": 24,
        "fitness": 700,
        "max_fitness": 1819
    },
    {
        "run": 25,
        "fitness": 1130,
        "max_fitness": 1819
    },
    {
        "run": 26,
        "fitness": 700,
        "max_fitness": 1819
    },
    {
        "run": 27,
        "fitness": 1130,
        "max_fitness": 1819
    },
    {
        "run": 28,
        "fitness": 814,
        "max_fitness": 1819
    },
    {
        "run": 29,
        "fitness": 1130,
        "max_fitness": 1819
    },
    {
        "run": 30,
        "fitness": 1130,
        "max_fitness": 1819
    },
    {
        "run": 31,
        "fitness": 1130,
        "max_fitness": 1819
    },
    {
        "run": 32,
        "fitness": 1130,
        "max_fitness": 1819
    },
    {
        "run": 33,
        "fitness": 1130,
        "max_fitness": 1819
    },
    {
        "run": 34,
        "fitness": 1130,
        "max_fitness": 1819
    },
    {
        "run": 35,
        "fitness": 1130,
        "max_fitness": 1819
    },
    {
        "run": 36,
        "fitness": 1130,
        "max_fitness": 1819
    },
    {
        "run": 37,
        "fitness": 1130,
        "max_fitness": 1819
    },
    {
        "run": 38,
        "fitness": 1130,
        "max_fitness": 1819
    },
    {
        "run": 39,
        "fitness": 1130,
        "max_fitness": 1819
    },
    {
        "run": 40,
        "fitness": 1130,
        "max_fitness": 1819
    },
    {
        "run": 41,
        "fitness": 1130,
        "max_fitness": 1819
    },
    {
        "run": 42,
        "fitness": 1130,
        "max_fitness": 1819
    },
    {
        "run": 43,
        "fitness": 1130,
        "max_fitness": 1819
    },
    {
        "run": 44,
        "fitness": 1130,
        "max_fitness": 1819
    },
    {
        "run": 45,
        "fitness": 1130,
        "max_fitness": 1819
    },
    {
        "run": 46,
        "fitness": 1130,
        "max_fitness": 1819
    },
    {
        "run": 47,
        "fitness": 1130,
        "max_fitness": 1819
    },
    {
        "run": 48,
        "fitness": 1130,
        "max_fitness": 1819
    },
    {
        "run": 49,
        "fitness": 1130,
        "max_fitness": 1819
    },
    {
        "run": 50,
        "fitness": 1130,
        "max_fitness": 1819
    },
    {
        "run": 51,
        "fitness": 1130,
        "max_fitness": 1819
    },
    {
        "run": 52,
        "fitness": 1130,
        "max_fitness": 1819
    },
    {
        "run": 53,
        "fitness": 1130,
        "max_fitness": 1819
    },
    {
        "run": 54,
        "fitness": 1130,
        "max_fitness": 1819
    },
    {
        "run": 55,
        "fitness": 1130,
        "max_fitness": 1819
    },
    {
        "run": 56,
        "fitness": 1130,
        "max_fitness": 1819
    },
    {
        "run": 57,
        "fitness": 1130,
        "max_fitness": 1819
    },
    {
        "run": 58,
        "fitness": 1130,
        "max_fitness": 1819
    },
    {
        "run": 59,
        "fitness": 1130,
        "max_fitness": 1819
    },
    {
        "run": 60,
        "fitness": 1130,
        "max_fitness": 1819
    },
    {
        "run": 61,
        "fitness": 1130,
        "max_fitness": 1819
    },
    {
        "run": 62,
        "fitness": 1130,
        "max_fitness": 1819
    },
    {
        "run": 63,
        "fitness": 1130,
        "max_fitness": 1819
    },
    {
        "run": 64,
        "fitness": 1130,
        "max_fitness": 1819
    },
    {
        "run": 65,
        "fitness": 1527,
        "max_fitness": 1819
    },
    {
        "run": 66,
        "fitness": 1130,
        "max_fitness": 1819
    },
    {
        "run": 67,
        "fitness": 1130,
        "max_fitness": 1819
    },
    {
        "run": 68,
        "fitness": 1130,
        "max_fitness": 1819
    },
    {
        "run": 69,
        "fitness": 1130,
        "max_fitness": 1819
    },
    {
        "run": 70,
        "fitness": 1130,
        "max_fitness": 1819
    },
    {
        "run": 71,
        "fitness": 1130,
        "max_fitness": 1819
    },
    {
        "run": 72,
        "fitness": 1130,
        "max_fitness": 1819
    },
    {
        "run": 73,
        "fitness": 1435,
        "max_fitness": 1819
    },
    {
        "run": 74,
        "fitness": 2475,
        "max_fitness": 2475
    },
    {
        "run": 75,
        "fitness": 2472,
        "max_fitness": 2475
    },
    {
        "run": 76,
        "fitness": 2472,
        "max_fitness": 2475
    },
    {
        "run": 77,
        "fitness": 2472,
        "max_fitness": 2475
    },
    {
        "run": 78,
        "fitness": 2472,
        "max_fitness": 2475
    },
    {
        "run": 79,
        "fitness": 2472,
        "max_fitness": 2475
    },
    {
        "run": 80,
        "fitness": 2472,
        "max_fitness": 2475
    },
    {
        "run": 81,
        "fitness": 2472,
        "max_fitness": 2475
    },
    {
        "run": 82,
        "fitness": 2472,
        "max_fitness": 2475
    },
    {
        "run": 83,
        "fitness": 3161,
        "max_fitness": 3161
    },
    {
        "run": 84,
        "fitness": 3161,
        "max_fitness": 3161
    },
    {
        "run": 85,
        "fitness": 3161,
        "max_fitness": 3161
    },
    {
        "run": 86,
        "fitness": 3161,
        "max_fitness": 3161
    },
    {
        "run": 87,
        "fitness": 3161,
        "max_fitness": 3161
    },
    {
        "run": 88,
        "fitness": 3161,
        "max_fitness": 3161
    },
    {
        "run": 89,
        "fitness": 3161,
        "max_fitness": 3161
    },
    {
        "run": 90,
        "fitness": 3161,
        "max_fitness": 3161
    },
    {
        "run": 91,
        "fitness": 3161,
        "max_fitness": 3161
    },
    {
        "run": 92,
        "fitness": 3161,
        "max_fitness": 3161
    },
    {
        "run": 93,
        "fitness": 3161,
        "max_fitness": 3161
    },
    {
        "run": 94,
        "fitness": 3161,
        "max_fitness": 3161
    },
    {
        "run": 95,
        "fitness": 3161,
        "max_fitness": 3161
    },
    {
        "run": 96,
        "fitness": 3161,
        "max_fitness": 3161
    },
    {
        "run": 97,
        "fitness": 3161,
        "max_fitness": 3161
    },
    {
        "run": 98,
        "fitness": 3161,
        "max_fitness": 3161
    },
    {
        "run": 99,
        "fitness": 3161,
        "max_fitness": 3161
    },
    {
        "run": 100,
        "fitness": 3161,
        "max_fitness": 3161
    }
]

# Extracting run numbers, max_fitness values and fitness values
runs = [item["run"] for item in data]
max_fitness = [item["max_fitness"] for item in data]
fitness = [item["fitness"] for item in data]

# Plotting the curves
plt.figure(figsize=(10, 6))
plt.plot(runs, max_fitness, label='Max fitness')
plt.plot(runs, fitness, label='fitness')  # Added line for fitness
plt.title('Progress of fitness over runs')
plt.xlabel('Run')
plt.ylabel('Fitness')
plt.legend()
plt.grid(True)
plt.show()
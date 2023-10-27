class Training():
    def __init__(self, env, smb, ram):
        self.env = env
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

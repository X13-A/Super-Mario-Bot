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
        print(self.getDeltaEnemy())
    
    def getDeltaEnemy(self):
        x,y = self.smb.get_mario_location_in_level(self.ram)
        enemies = self.smb.get_enemy_locations(self.ram)
        dx = 16
        dy = 16
        if(len(enemies)>0) :
            closest_enemy = min(enemies, key=lambda e: (e.location.x - x)**2 + (e.location.y - y)**2)
            dx = round((closest_enemy.location.x - x)/16)
            dy = round((closest_enemy.location.y - y)/16)
        return (dx,dy)

from utils import StaticTileType
import numpy as np
from utils import SMB
from settings import VISION_RANGE

class State:
    def __init__(self, training):
        self.training = training

        self.obstacle = 16
        self.hole = 16
        self.enemy = (16, 16)
        self.last_jump_hole_dist = 16
        
    def getObstacleDist(self, tiles, mario_pos):
        if (mario_pos[0] >= tiles.shape[0] or mario_pos[1] >= tiles.shape[1]): return tiles.shape[1]
        if (mario_pos[0] < 0 or mario_pos[1] < 0): return tiles.shape[1]
        
        mario_row = tiles[mario_pos[0], mario_pos[1]:]
        obstacles = np.where(mario_row == StaticTileType.Fake)[0]
        
        if (obstacles.size and obstacles[0] <= VISION_RANGE): return obstacles[0]
        return tiles.shape[1]

    def getHoleDist(self, tiles, mario_pos):
        if (mario_pos[1] >= tiles.shape[1]): return tiles.shape[1]
        if (mario_pos[1] < 0): return tiles.shape[1]
        
        bottom_row = tiles[-1, (mario_pos[1]):]
        holes = np.where(bottom_row == StaticTileType.Empty)[0]

        # TODO: check only hole
        if (holes.size and holes[0] <= VISION_RANGE): 
            return holes[0]
        return tiles.shape[1]
    
    def getEnemyDist(self, enemies, mario_pos_in_level):
        mario_x_in_level, mario_y_in_level = mario_pos_in_level
        
        forward_enemies = [enemy for enemy in enemies if enemy.location.x >= mario_x_in_level]
        if (not forward_enemies): return (16, 16)
        
        closest_enemy = min(forward_enemies, key=lambda e: (e.location.x - mario_x_in_level)**2 + (e.location.y - mario_y_in_level)**2)
        dx = round((closest_enemy.location.x - mario_x_in_level)/16)
        dy = round((closest_enemy.location.y - mario_y_in_level)/16)
        if dx>VISION_RANGE :
            dx = 16
        if dy>VISION_RANGE :
            dy = 16
        
        return (dx,dy)

    def getHoleDistOnJump(self, tiles, mario_pos):
        if self.training.just_jumped:
            return self.getHoleDist(tiles, mario_pos)
        elif self.training.just_hit_ground:
            return 16
        return self.last_jump_hole_dist

    def update(self, ram):
        tiles = SMB.get_tiles_array(ram)
        mario_pos_in_grid = SMB.get_mario_row_col(ram)
        mario_pos_in_level = SMB.get_mario_location_in_level(ram)
        enemies = SMB.get_enemy_locations(ram)
        
        self.last_jump_hole_dist = self.getHoleDistOnJump(tiles, mario_pos_in_grid)
        self.obstacle = self.getObstacleDist(tiles, mario_pos_in_grid)
        self.hole = self.getHoleDist(tiles, mario_pos_in_grid)
        self.enemy = self.getEnemyDist(enemies, mario_pos_in_level)

    def combination(self):
        return (self.enemy[0],self.enemy[1],self.obstacle,self.hole,self.last_jump_hole_dist)
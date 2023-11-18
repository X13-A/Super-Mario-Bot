import pygame
import sys
from utils import ColorMap
from utils import SMB
import time
from datetime import datetime
from datetime import timedelta
from settings import AVERAGE_FPS_CALCULATION_TIME

class MiniDisplay():
    def __init__(self, ram):
        self.ram = ram
        self.screen = pygame.display.set_mode((256, 240))
        pygame.display.set_caption('TileVision')
        pygame.init()

    def draw_tiles(self):
        tiles = SMB.get_tiles_array(self.ram)
        for row in range(tiles.shape[0]):
            for col in range(tiles.shape[1]):
                tile = tiles[row, col]
                color = ColorMap[tile.name].value if tile.name in ColorMap.__members__ else ColorMap.Generic_Static_Tile.value
                pygame.draw.rect(self.screen, color, (col * 16, row * 16, 16, 16))

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def update(self):
        self.draw_tiles()
        self.check_events()
        pygame.display.flip()

class FPSCounter():
    def __init__(self):
        self.frame_count = 0
        self.last_time = time.time()

    def update(self):
        self.frame_count += 1
        current_time = time.time()
        elapsed_time = current_time - self.last_time
        if elapsed_time > AVERAGE_FPS_CALCULATION_TIME:  # More than 1 second has passed
            fps = self.frame_count / elapsed_time
            print(f"Average FPS: {fps:.2f}")
            self.frame_count = 0
            self.last_time = current_time

def get_time_ms():
    return int(datetime.now().timestamp() * 1000)

def ms_to_time_str(milliseconds):
    delta = timedelta(milliseconds=milliseconds)
    hours, remainder = divmod(delta.total_seconds(), 3600)
    minutes, seconds = divmod(remainder, 60)
    time_str = '{:02}:{:02}:{:02}'.format(int(hours), int(minutes), int(seconds))
    return time_str
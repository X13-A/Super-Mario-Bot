import pygame
import sys
from utils import ColorMap, SMB

class MiniDisplay():

    def __init__(self, smb, ram):
        self.smb = smb
        self.ram = ram
        self.tiles = None
        self.screen = pygame.display.set_mode((256, 240))
        pygame.display.set_caption('T-Vision')
        pygame.init()

    def draw_tiles(self):
        self.tiles = self.smb.get_tiles_array(self.ram)
        if self.tiles is None:
            return
        for row in range(self.tiles.shape[0]):
            for col in range(self.tiles.shape[1]):
                tile = self.tiles[row, col]
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


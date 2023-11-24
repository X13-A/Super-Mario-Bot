from debug import MiniDisplay
from training import Training
from utils import SMB
import pygame
from pygame.locals import *
from nes_py import NESEnv
from nes_py.wrappers import JoypadSpace

ROM_PATH = "./Super Mario Bros. (World).nes"
STATE_PATH = "./save.pkl"

ACTIONS = [
    ['NOOP'],
    ['right'],
    ['right', 'A'],
    ['right', 'B'],
    ['right', 'A', 'B'],
    ['A'],
    ['left']
]

emulator = JoypadSpace(NESEnv(ROM_PATH), ACTIONS)

ram = emulator.ram
smb = SMB()
training = Training(smb, ram)
miniDisplay : MiniDisplay = MiniDisplay(smb, ram)

def controls():
    keys = pygame.key.get_pressed()
    if keys[K_LALT] and keys[K_1]:
        emulator.save_state(ROM_PATH)
    elif keys[K_1]:
        emulator.load_state(ROM_PATH)

emulator.reset()
for step in range(100000):
    controls();
    training.update()
    emulator.step()
    emulator.render()
    miniDisplay.update()
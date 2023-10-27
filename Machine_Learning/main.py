from nes_py.wrappers import JoypadSpace
import gym_super_mario_bros
from gym_super_mario_bros.actions import SIMPLE_MOVEMENT
from mini_display import *
from train import *
from pygame.locals import * # Import the constant for the right arrow key

env = gym_super_mario_bros.make('SuperMarioBros-v0', apply_api_compatibility=True, render_mode="human" )
env = JoypadSpace(env, SIMPLE_MOVEMENT)
ram = env.env.env.env.env.env.unwrapped.ram
smb = SMB()
training = Training(env, smb, ram)
miniDisplay : MiniDisplay = MiniDisplay(smb, ram)

for step in range(100000):
    training.update()
    miniDisplay.update()

env.close()
pygame.quit()
sys.exit()
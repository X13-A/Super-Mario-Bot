from nes_py.wrappers import JoypadSpace
import gym_super_mario_bros
from gym_super_mario_bros.actions import SIMPLE_MOVEMENT
from debug import *
from training import *
from settings import *

# Setup environment
env = gym_super_mario_bros.make('SuperMarioBros-v0', apply_api_compatibility=True, render_mode=RENDER_MODE)
env = JoypadSpace(env, SIMPLE_MOVEMENT)
ram = env.env.env.env.env.env.unwrapped.ram

# Setup training
training : Training = Training(env, ram)

# Init debug tools
if SHOW_MINI_DISPLAY: mini_display : MiniDisplay = MiniDisplay(ram)
if SHOW_FPS: fps_counter : FPSCounter = FPSCounter()

# Training loop
for step in range(10000):
    training.update()
    if SHOW_MINI_DISPLAY: mini_display.update()
    if SHOW_FPS: fps_counter.update()

training.q_table.saveQ()
env.close()
pygame.quit()
sys.exit()
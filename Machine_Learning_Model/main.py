from nes_py.wrappers import JoypadSpace
import gym_super_mario_bros
from gym_super_mario_bros.actions import COMPLEX_MOVEMENT
from debug import *
from training import *
from settings import *
import time
from settings import MAX_FRAMERATE

# Setup environment
env = gym_super_mario_bros.make(f"SuperMarioBros-1-1-v0", apply_api_compatibility=True, render_mode=RENDER_MODE)
env = JoypadSpace(env, COMPLEX_MOVEMENT)
ram = env.env.env.env.env.env.unwrapped.ram

# Setup training
training : Training = Training(env, ram)
print(COMPLEX_MOVEMENT)

# Init debug tools
if SHOW_MINI_DISPLAY: mini_display : MiniDisplay = MiniDisplay(ram)
if SHOW_FPS: fps_counter : FPSCounter = FPSCounter()

# Training loop
last_time = time.time()
while True:
    if (time.time() - last_time > 1/MAX_FRAMERATE):
        last_time = time.time()
        training.update()
        if SHOW_MINI_DISPLAY: mini_display.update()
        if SHOW_FPS: fps_counter.update()

training.q_table.saveQ()
env.close()
pygame.quit()
sys.exit()

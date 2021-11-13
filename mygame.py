import pico2d
import game_framework

import main_state

pico2d.open_canvas(1600, 600)
game_framework.run(main_state)
pico2d.close_canvas ()
import game_framework
from fireball import Fire_Ball
from pico2d import *

import game_world

# Boy Run Speed
# fill expressions correctly
PIXEL_PER_METER = (5.0 / 0.3)
RUN_SPEED_KMPH = 20.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Boy Action Speed
# fill expressions correctly
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 5



# Boy Event
RIGHT_DOWN, LEFT_DOWN, RIGHT_UP, LEFT_UP, SHIFT_UP, SHIFT_DOWN, SLEEP_TIMER,SPACE = range(8)

key_event_table = {
    (SDL_KEYDOWN, SDLK_RIGHT): RIGHT_DOWN,
    (SDL_KEYDOWN, SDLK_LEFT): LEFT_DOWN,
    (SDL_KEYUP, SDLK_RIGHT): RIGHT_UP,
    (SDL_KEYUP, SDLK_LEFT): LEFT_UP,

    (SDL_KEYDOWN, SDLK_LSHIFT): SHIFT_DOWN,
    (SDL_KEYDOWN, SDLK_RSHIFT): SHIFT_DOWN,
    (SDL_KEYUP, SDLK_LSHIFT): SHIFT_UP,
    (SDL_KEYUP, SDLK_RSHIFT): SHIFT_UP,
    (SDL_KEYDOWN, SDLK_SPACE): SPACE

}


class DashState:

    def enter(Mario, event):
        print('ENTER DASH')
        Mario.dir = Mario.velocity

    def exit(Mario, event):
        print('EXIT DASH')
        pass

    def do(Mario):
        Mario.frame = (Mario.frame + 1) % 8
        Mario.x += Mario.velocity * 2.5
        Mario.x = clamp(25, Mario.x, 1600 - 25)

    def draw(Mario):
        if Mario.velocity == 1:
            Mario.rimage.clip_draw(Mario.frame * 100, 100, 100, 100, Mario.x, Mario.y)
        else:
            Mario.limage.clip_draw(Mario.frame * 100, 0, 100, 100, Mario.x, Mario.y)

class IdleState:

    def enter(Mario, event):
        if event == RIGHT_DOWN:
            Mario.velocity += RUN_SPEED_PPS
        elif event == LEFT_DOWN:
            Mario.velocity -= RUN_SPEED_PPS
        elif event == RIGHT_UP:
            Mario.velocity -= RUN_SPEED_PPS
        elif event == LEFT_UP:
            Mario.velocity += RUN_SPEED_PPS
        Mario.timer = 1000

    def exit(Mario, event):
        if event == SPACE:
            Mario.fire_ball()
        pass

    def do(Mario):
       # Mario.frame = (Mario.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        Mario.timer -= 1
        if Mario.timer == 0:
            Mario.add_event(SLEEP_TIMER)

    def draw(Mario):
        if Mario.dir == 1:
            Mario.rimage.clip_draw(2, 319, 20, 35, Mario.x, Mario.y)
        else:
            Mario.limage.clip_draw(678, 319, 20, 35, Mario.x, Mario.y)


class RunState:

    def enter(Mario, event):
        if event == RIGHT_DOWN:
            Mario.velocity += RUN_SPEED_PPS
        elif event == LEFT_DOWN:
            Mario.velocity -= RUN_SPEED_PPS
        elif event == RIGHT_UP:
            Mario.velocity -= RUN_SPEED_PPS
        elif event == LEFT_UP:
            Mario.velocity += RUN_SPEED_PPS
        Mario.dir = clamp(-1, Mario.velocity, 1)
        pass

    def exit(Mario, event):
        if event == SPACE:
            Mario.fire_ball()

    def do(Mario):
        Mario.frame = (Mario.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 5
        Mario.x += Mario.velocity * game_framework.frame_time
        Mario.x = clamp(25, Mario.x, 1600 - 25)

    def draw(Mario):
        if Mario.dir == 1:
            Mario.rimage.clip_draw(int(Mario.frame) * 20 + 3, 319, 20, 35, Mario.x, Mario.y)
        else:
            Mario.limage.clip_draw(int(Mario.frame) * 20 + 597, 319, 20, 35, Mario.x, Mario.y)

class SleepState:

    def enter(Mario, event):
        Mario.frame = 0

    def exit(Mario, event):
        pass

    def do(Mario):
        Mario.frame = (Mario.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8

    def draw(Mario):
        if Mario.dir == 1:
            Mario.rimage.clip_composite_draw(int(Mario.frame) * 20 + 3, 300, 100, 100, 3.141592 / 2, '', Mario.x - 25, Mario.y - 25, 100, 100)
        else:
            Mario.limage.clip_composite_draw(int(Mario.frame) * 100, 200, 100, 100, -3.141592 / 2, '', Mario.x + 25, Mario.y - 25, 100, 100)






next_state_table = {
    DashState: {LEFT_DOWN: IdleState, RIGHT_DOWN: IdleState, LEFT_UP: IdleState, RIGHT_UP: IdleState,
                SHIFT_UP: RunState},
    IdleState: {RIGHT_UP: RunState, LEFT_UP: RunState, RIGHT_DOWN: RunState, LEFT_DOWN: RunState, SLEEP_TIMER: SleepState,
                SHIFT_DOWN: IdleState, SHIFT_UP: IdleState, SPACE: IdleState},
    RunState: {RIGHT_UP: IdleState, LEFT_UP: IdleState, LEFT_DOWN: IdleState, RIGHT_DOWN: IdleState,
               SHIFT_DOWN: DashState, SHIFT_UP: RunState, SPACE: RunState},
    SleepState: {LEFT_DOWN: RunState, RIGHT_DOWN: RunState, LEFT_UP: RunState, RIGHT_UP: RunState, SPACE: IdleState}
}

class Mario:

    def __init__(self):
        self.x, self.y = 0, 90
        # Boy is only once created, so instance image loading is fine
        self.rimage = load_image('right.png')
        self.limage = load_image('left.png')
        self.dir = 1
        self.velocity = 0
        self.frame = 0
        self.event_que = []
        self.cur_state = IdleState
        self.cur_state.enter(self, None)


    def fire_ball(self):
        f_ball = Fire_Ball(self.x, self.y, self.dir*3)
        game_world.add_object(f_ball, 1)


    def add_event(self, event):
        self.event_que.insert(0, event)

    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)

    def draw(self):
        self.cur_state.draw(self)

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)


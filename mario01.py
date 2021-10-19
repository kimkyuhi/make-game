from pico2d import *
import threading

def thread_run():
    global charge
    global dir
    run_timer = threading.Timer(0.5, thread_run)
    run_timer.start()
    if dir == 1 and charge < 6:
        charge += 1
    elif dir == -1 and charge > -6:
        charge -= 1

    if dir == 0:
        run_timer.cancel()




def handle_running_events():
    global running
    global dir
    global charge
    global stop
    global jump, jump_remy
    global x, y

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_RIGHT:
                stop = 0
                dir += 1
                thread_run()
            elif event.key == SDLK_LEFT:
                stop = 0
                dir -= 1
                thread_run()
            elif event.key == SDLK_UP:
                jump = 1
                jump_remy = y
            elif event.key == SDLK_ESCAPE:
                running = False

        elif event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                stop = 1
                dir = 0
                charge = 0

            elif event.key == SDLK_LEFT:
                stop = -1
                dir = 0
                charge = 0
            elif event.key == SDLK_UP:
                jump = 0
    pass

open_canvas()
grass = load_image('grass.png')
character_right = load_image('mario_right_walk.png')
character_left = load_image('mario_left_walk.png')
character_right_stop = load_image('mario_right_stop.png')
character_left_stop = load_image('mario_left_stop.png')
character_right_run = load_image('mario_right_run.png')
character_left_run = load_image('mario_left_run.png')
character_right_jump = load_image('mario_right_jump.png')

running = True
x = 0
y = 75
walk_frame = 0
run_frame = 0
dir = 0 # -1 left +1 right 0 stop
stop = 1 # -1 left +1 right 0 walk or run
charge = 0
jump = 0
jump_remy = 0.0

while running:
    clear_canvas()
    grass.draw(400, 30)
    # 정지모션
    if stop == 1:
        character_right_stop.clip_draw(0, 2, 20, 35, x, y)
    elif stop == -1:
        character_left_stop.clip_draw(0, 2, 20, 35, x, y)
    else:# walk or run and jump.
        if dir > 0:
            if charge == 6:
                if jump != 1:
                    character_right_run.clip_draw(run_frame * 19, 2, 19, 35, x, y)
                else:#jump
                    while jump == 1 and y <= (jump_remy + 50):
                        y += 3
                    character_right_jump.clip_draw(0, 2, 20, 35, x, y)
            else:
                character_right.clip_draw(walk_frame * 20, 2, 20, 35, x, y)

        elif dir < 0:
            if charge == -6:
                character_left_run.clip_draw(run_frame * 20, 2, 20, 35, x, y)
            else:
                character_left.clip_draw(walk_frame * 20, 2, 20, 35, x, y)

    update_canvas()
    handle_running_events()
    walk_frame = (walk_frame + 1) % 5
    run_frame = (run_frame + 1) % 3
    x += dir * 5 + charge
    delay(0.08)

close_canvas()
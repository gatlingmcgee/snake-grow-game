# --- direction controls ---

def on_up_pressed():
    global nextDx, nextDy, waiting_for_first_direction
    if dy == 0 or waiting_for_first_direction:
        nextDx = 0
        nextDy = -10
        waiting_for_first_direction = False
controller.up.on_event(ControllerButtonEvent.PRESSED, on_up_pressed)

# --- reset game function ---

def on_b_pressed():
    global dx, dy, nextDx, nextDy, waiting_for_first_direction, SnakeBody
    # reset direction
    dx = 0
    dy = 0
    nextDx = 0
    nextDy = 0
    # snake waits for first move
    waiting_for_first_direction = True
    # reset score
    info.set_score(0)
    # reset snake position
    SnakeHead.set_position(80, 60)
    # destroy tail
    for segment in SnakeBody:
        segment.destroy()
    SnakeBody = []
    # reposition food
    placeFood()
controller.B.on_event(ControllerButtonEvent.PRESSED, on_b_pressed)

def on_left_pressed():
    global nextDx, nextDy, waiting_for_first_direction
    if dx == 0 or waiting_for_first_direction:
        nextDx = -10
        nextDy = 0
        waiting_for_first_direction = False
controller.left.on_event(ControllerButtonEvent.PRESSED, on_left_pressed)

def placeFood():
    Chicken.set_position(randint(1, 15) * 10, randint(1, 11) * 10)

def on_right_pressed():
    global nextDx, nextDy, waiting_for_first_direction
    if dx == 0 or waiting_for_first_direction:
        nextDx = 10
        nextDy = 0
        waiting_for_first_direction = False
controller.right.on_event(ControllerButtonEvent.PRESSED, on_right_pressed)

def on_down_pressed():
    global nextDx, nextDy, waiting_for_first_direction
    if dy == 0 or waiting_for_first_direction:
        nextDx = 0
        nextDy = 10
        waiting_for_first_direction = False
controller.down.on_event(ControllerButtonEvent.PRESSED, on_down_pressed)

i = 0
oldHeadY = 0
oldHeadX = 0
SnakeBody: List[Sprite] = []
dx = 0
nextDy = 0
nextDx = 0
dy = 0
Chicken: Sprite = None
SnakeHead: Sprite = None
waiting_for_first_direction = False
waiting_for_first_direction = True
# --- create snake head sprite ---
SnakeHead = sprites.create(img("""
        . . . . 7 7 7 7 7 7 7 7 . . . .
        . . . . 7 7 7 7 7 7 7 7 . . . .
        . . . . 7 7 7 7 7 7 7 7 . . . .
        . . . . 7 7 7 7 7 7 7 7 . . . .
        """),
    SpriteKind.player)
SnakeHead.set_position(80, 60)
SnakeHead.set_stay_in_screen(False)
# --- create food item sprites ---
Chicken = sprites.create(img("""
        . . . . . . b 5 b . . . .
        . . . . b b b b b b . . .
        . . . b b 5 5 5 5 5 b . .
        . b b d d d 5 5 5 5 5 b .
        """),
    SpriteKind.food)
placeFood()
# --- game loop for each item collected ---
# speed control

def on_update_interval():
    global dx, dy, oldHeadX, oldHeadY, i
    # apply direction only if a direction is set
    dx = nextDx
    dy = nextDy
    # don't move until a direction is pressed
    if dx == 0 and dy == 0:
        return
    # save head position
    oldHeadX = SnakeHead.x
    oldHeadY = SnakeHead.y
    # save last tail position
    if len(SnakeBody) > 0:
        lastTailX = SnakeBody[len(SnakeBody) - 1].x
        lastTailY = SnakeBody[len(SnakeBody) - 1].y
    else:
        lastTailX = oldHeadX
        lastTailY = oldHeadY
    i = len(SnakeBody) - 1
    while i > 0:
        SnakeBody[i].set_position(SnakeBody[i - 1].x, SnakeBody[i - 1].y)
        i += -1
    if len(SnakeBody) > 0:
        SnakeBody[0].set_position(oldHeadX, oldHeadY)
    # move head
    SnakeHead.x += dx
    SnakeHead.y += dy
    # detect wall collision
    if SnakeHead.x < 0 or SnakeHead.x > 150 or SnakeHead.y < 0 or SnakeHead.y > 110:
        game.over(False)
    # detect self collision
    for segment2 in SnakeBody:
        if SnakeHead.overlaps_with(segment2):
            game.over(False)
    # detect food collision
    if SnakeHead.overlaps_with(Chicken):
        # food collection sound
        music.ba_ding.play()
        info.change_score_by(1)
        placeFood()
        newSegment = sprites.create(img("""
                . . 2 2 2 2 . .
                . 2 2 2 2 2 2 .
                . 2 2 2 2 2 2 .
                . . 2 2 2 2 . .
                """),
            SpriteKind.player)
        newSegment.set_position(lastTailX, lastTailY)
        SnakeBody.append(newSegment)
game.on_update_interval(400, on_update_interval)

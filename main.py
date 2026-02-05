# --- Direction variables ---
dx = 10
dy = 0
nextDx = 10
nextDy = 0

# --- Direction controls ---

def on_up_pressed():
    global nextDx, nextDy
    if dy == 0:
        nextDx = 0
        nextDy = -10
controller.up.on_event(ControllerButtonEvent.PRESSED, on_up_pressed)

def on_left_pressed():
    global nextDx, nextDy
    if dx == 0:
        nextDx = -10
        nextDy = 0
controller.left.on_event(ControllerButtonEvent.PRESSED, on_left_pressed)

def on_right_pressed():
    global nextDx, nextDy
    if dx == 0:
        nextDx = 10
        nextDy = 0
controller.right.on_event(ControllerButtonEvent.PRESSED, on_right_pressed)

def on_down_pressed():
    global nextDx, nextDy
    if dy == 0:
        nextDx = 0
        nextDy = 10
controller.down.on_event(ControllerButtonEvent.PRESSED, on_down_pressed)

# --- Create Food ---

def placeFood():
    Chicken.set_position(randint(1, 15) * 10, randint(1, 11) * 10)

# --- Variables ---

SnakeHead: Sprite = None
Chicken: Sprite = None
SnakeBody: List[Sprite] = []

info.set_score(0)

# --- Create Snake Head ---

SnakeHead = sprites.create(img("""
        . . . . 7 7 7 7 7 7 7 7 . . . .
        . . . . 7 7 7 7 7 7 7 7 . . . .
        . . . . 7 7 7 7 7 7 7 7 . . . .
        . . . . 7 7 7 7 7 7 7 7 . . . .
"""), SpriteKind.player)

SnakeHead.set_position(80, 60)
SnakeHead.set_stay_in_screen(False)

# --- Create Food ---

Chicken = sprites.create(img("""
        . . . . . . b 5 b . . . .
        . . . . b b b b b b . . .
        . . . b b 5 5 5 5 5 b . .
        . b b d d d 5 5 5 5 5 b .
"""), SpriteKind.food)

placeFood()

# --- Game loop ---

def on_update_interval():
    global dx, dy

    # Apply queued direction
    dx = nextDx
    dy = nextDy

    # Save head position
    oldHeadX = SnakeHead.x
    oldHeadY = SnakeHead.y

    # Save last tail position
    if len(SnakeBody) > 0:
        lastTailX = SnakeBody[len(SnakeBody) - 1].x
        lastTailY = SnakeBody[len(SnakeBody) - 1].y
    else:
        lastTailX = oldHeadX
        lastTailY = oldHeadY

    # Move body
    for i in range(len(SnakeBody) - 1, 0, -1):
        SnakeBody[i].set_position(
            SnakeBody[i - 1].x,
            SnakeBody[i - 1].y
        )

    if len(SnakeBody) > 0:
        SnakeBody[0].set_position(oldHeadX, oldHeadY)

    # Move head
    SnakeHead.x += dx
    SnakeHead.y += dy

    # Wall collision
    if SnakeHead.x < 0 or SnakeHead.x > 150 or SnakeHead.y < 0 or SnakeHead.y > 110:
        game.over(False)

    # Self collision
    for segment in SnakeBody:
        if SnakeHead.overlaps_with(segment):
            game.over(False)

    # Food collision (grow)
    if SnakeHead.overlaps_with(Chicken):
        info.change_score_by(1)
        placeFood()

        newSegment = sprites.create(img("""
                . . 2 2 2 2 . .
                . 2 2 2 2 2 2 .
                . 2 2 2 2 2 2 .
                . . 2 2 2 2 . .
        """), SpriteKind.player)

        newSegment.set_position(lastTailX, lastTailY)
        SnakeBody.append(newSegment)

game.on_update_interval(200, on_update_interval)

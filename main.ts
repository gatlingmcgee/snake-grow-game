//  --- Direction variables ---
let dx = 10
let dy = 0
let nextDx = 10
let nextDy = 0
//  --- Direction controls ---
controller.up.onEvent(ControllerButtonEvent.Pressed, function on_up_pressed() {
    
    if (dy == 0) {
        nextDx = 0
        nextDy = -10
    }
    
})
controller.left.onEvent(ControllerButtonEvent.Pressed, function on_left_pressed() {
    
    if (dx == 0) {
        nextDx = -10
        nextDy = 0
    }
    
})
controller.right.onEvent(ControllerButtonEvent.Pressed, function on_right_pressed() {
    
    if (dx == 0) {
        nextDx = 10
        nextDy = 0
    }
    
})
controller.down.onEvent(ControllerButtonEvent.Pressed, function on_down_pressed() {
    
    if (dy == 0) {
        nextDx = 0
        nextDy = 10
    }
    
})
//  --- Create Food ---
function placeFood() {
    Chicken.setPosition(randint(1, 15) * 10, randint(1, 11) * 10)
}

//  --- Variables ---
let SnakeHead : Sprite = null
let Chicken : Sprite = null
let SnakeBody : Sprite[] = []
info.setScore(0)
//  --- Create Snake Head ---
SnakeHead = sprites.create(img`
        . . . . 7 7 7 7 7 7 7 7 . . . .
        . . . . 7 7 7 7 7 7 7 7 . . . .
        . . . . 7 7 7 7 7 7 7 7 . . . .
        . . . . 7 7 7 7 7 7 7 7 . . . .
`, SpriteKind.Player)
SnakeHead.setPosition(80, 60)
SnakeHead.setStayInScreen(false)
//  --- Create Food ---
Chicken = sprites.create(img`
        . . . . . . b 5 b . . . .
        . . . . b b b b b b . . .
        . . . b b 5 5 5 5 5 b . .
        . b b d d d 5 5 5 5 5 b .
`, SpriteKind.Food)
placeFood()
//  --- Game loop ---
game.onUpdateInterval(200, function on_update_interval() {
    let lastTailX: number;
    let lastTailY: number;
    let newSegment: Sprite;
    
    //  Apply queued direction
    dx = nextDx
    dy = nextDy
    //  Save head position
    let oldHeadX = SnakeHead.x
    let oldHeadY = SnakeHead.y
    //  Save last tail position
    if (SnakeBody.length > 0) {
        lastTailX = SnakeBody[SnakeBody.length - 1].x
        lastTailY = SnakeBody[SnakeBody.length - 1].y
    } else {
        lastTailX = oldHeadX
        lastTailY = oldHeadY
    }
    
    //  Move body
    for (let i = SnakeBody.length - 1; i > 0; i += -1) {
        SnakeBody[i].setPosition(SnakeBody[i - 1].x, SnakeBody[i - 1].y)
    }
    if (SnakeBody.length > 0) {
        SnakeBody[0].setPosition(oldHeadX, oldHeadY)
    }
    
    //  Move head
    SnakeHead.x += dx
    SnakeHead.y += dy
    //  Wall collision
    if (SnakeHead.x < 0 || SnakeHead.x > 150 || SnakeHead.y < 0 || SnakeHead.y > 110) {
        game.over(false)
    }
    
    //  Self collision
    for (let segment of SnakeBody) {
        if (SnakeHead.overlapsWith(segment)) {
            game.over(false)
        }
        
    }
    //  Food collision (grow)
    if (SnakeHead.overlapsWith(Chicken)) {
        info.changeScoreBy(1)
        placeFood()
        newSegment = sprites.create(img`
                . . 2 2 2 2 . .
                . 2 2 2 2 2 2 .
                . 2 2 2 2 2 2 .
                . . 2 2 2 2 . .
        `, SpriteKind.Player)
        newSegment.setPosition(lastTailX, lastTailY)
        SnakeBody.push(newSegment)
    }
    
})

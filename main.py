# Libraries
import random
import sys
import pygame

# Global variables
screenWidth = 300
screenHeight = 500
screen = pygame.display.set_mode((screenWidth, screenHeight))
framePerSecond = 30
scrollSpeed = 4
game_images = {}

baseY = screenHeight * 0.75
pipeGap = screenHeight / 4
pipeHeight = 300
pipeWidth = 70
collision = False

title = 'gallery/images/front5.jpg'
background = 'gallery/images/background.png'
pipe = 'gallery/images/pipe.png'
player = 'gallery/images/bird.png'
base = 'gallery/images/base.png'
gameOver = 'gallery/images/gm1.png'


# Loading images
def load_images():
    game_images['title'] = pygame.transform.scale(pygame.image.load(title), (100, 200))

    game_images['base'] = pygame.transform.scale(pygame.image.load(base), (screenWidth * 2, 200))

    game_images['pipe'] = (

    pygame.transform.rotate(pygame.transform.scale(pygame.image.load(pipe), (pipeWidth, pipeHeight)), 180),

    pygame.transform.scale(pygame.image.load(pipe), (pipeWidth, pipeHeight))

     )

    game_images['background'] = pygame.transform.scale(pygame.image.load(background), (screenWidth, screenHeight))

    game_images['player'] = pygame.transform.scale(pygame.image.load(player), (50, 50))

    game_images['gameOver'] = pygame.transform.scale(pygame.image.load(gameOver), (200, 100))

    game_images['score'] = (
    pygame.transform.scale(pygame.image.load('gallery/images/0.png'), (50, 50)),
    pygame.transform.scale(pygame.image.load('gallery/images/1.png'), (50, 50)),
    pygame.transform.scale(pygame.image.load('gallery/images/2.png'), (50, 50)),
    pygame.transform.scale(pygame.image.load('gallery/images/3.png'), (50, 50)),
    pygame.transform.scale(pygame.image.load('gallery/images/4.png'), (50, 50)),
    pygame.transform.scale(pygame.image.load('gallery/images/5.png'), (50, 50)),
    pygame.transform.scale(pygame.image.load('gallery/images/6.png'), (50, 50)),
    pygame.transform.scale(pygame.image.load('gallery/images/7.png'), (50, 50)),
    pygame.transform.scale(pygame.image.load('gallery/images/8.png'), (50, 50)),
    pygame.transform.scale(pygame.image.load('gallery/images/9.png'), (50, 50))
    )


def startGame():
    playerX = int(screenWidth * 0.4)
    playerY = int((screenHeight - game_images['player'].get_height()) * 0.7)
    titleX = int((screenWidth - game_images['title'].get_width()) * 0.5)
    titleY = int(screenHeight * 0.2)
    baseX = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE or event.key == pygame.K_UP):
                play()

            else:
                screen.blit(game_images['background'], (0, 0))
                screen.blit(game_images['player'], (playerX, playerY))
                screen.blit(game_images['base'], (baseX, baseY))
                screen.blit(game_images['title'], (titleX, titleY))
                # refresh the screen
                pygame.display.update()
                # rate for frame per second
                fps_clock.tick(framePerSecond)

# Generate positions of two pipes top and bottom
def getRandomPipe():
    height = random.randrange(0, int(baseY * 0.8 - pipeGap))
    height += int(baseY * 0.2)
    pipeX = screenWidth + 60

    pipes = [
        {'x': pipeX, 'y': height - pipeHeight},  # upper pipe
        {'x': pipeX, 'y': height + pipeGap},  # lower pipe
    ]
    return pipes

# Testing for collisions
def crashTest(playerx, playery, upperPipes, lowerPipes):
    score = 0
    if playery <= 0 or playery >= 400:
        return True
    else:
        for upperpipe, lowerpipe in zip(upperPipes, lowerPipes):
            if abs(playerx  - upperpipe['x']) <= game_images['pipe'][0].get_width():
                if playery <= pipeHeight + upperpipe['y']:
                    return True
            if abs(playerx - lowerpipe['x']) <= game_images['pipe'][0].get_width():
                if playery + game_images['player'].get_height() >= lowerpipe['y']:
                    return True
        return False

# Game over screen
def endGame(score):
    gameOverX = int((screenWidth - game_images['gameOver'].get_width()) * 0.5)
    gameOverY = int(screenHeight*0.2)
    screen.blit(game_images['background'], (0, 0))
    screen.blit(game_images['gameOver'], (gameOverX, gameOverY))
    screen.blit(game_images['base'], (0, baseY))

# show final score
    scoreFont = pygame.font.SysFont('couriernew', 40, bold=True)
    display = scoreFont.render(f"Score: {score}", True, (255,127,0))
    screen.blit(display, (screenWidth*0.2, screenHeight*0.4))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE or event.key == pygame.K_UP):
                startGame()

        pygame.display.update()
        fps_clock.tick(framePerSecond)

def play():
    playerX = int(screenWidth * 0.4)
    playerY = int((screenHeight - game_images['player'].get_height()) * 0.5)
    baseX = 0
    vel = 0
    score = 0

    # create 2 pipes
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    # my list of upper pipes
    upperPipes = [
        {'x': screenWidth + 200, 'y': newPipe1[0]['y']},
        {'x': screenWidth + 200 + (screenWidth / 2), 'y': newPipe2[0]['y']}
    ]

    # my list of lower pipes
    lowerPipes = [
        {'x': screenWidth + 200, 'y': newPipe1[1]['y']},
        {'x': screenWidth + 200 + (screenWidth / 2), 'y': newPipe2[1]['y']}
    ]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                vel = -6
            if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                vel = 3

        playerY += vel

        # check if player crashed
        collision = crashTest(playerX, playerY, upperPipes, lowerPipes)
        if collision:
            endGame(score)

        # moves pipe to the left
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] -= scrollSpeed
            lowerPipe['x'] -= scrollSpeed

            # add a new pipe when the first is about to cross the leftmost part of the screen
            if 0 < upperPipe['x'] < 5:
                newPipe = getRandomPipe()
                upperPipes.append(newPipe[0])
                lowerPipes.append(newPipe[1])

        # if the pipe is out of the screen, remove it
        if upperPipes[0]['x'] < -game_images['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        # blit the sprites meaning draw the sprites
        screen.blit(game_images['background'], (0, 0))
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            screen.blit(game_images['pipe'][0], (upperPipe['x'], upperPipe['y']))
            screen.blit(game_images['pipe'][1], (lowerPipe['x'], lowerPipe['y']))

        screen.blit(game_images['base'], (baseX, baseY))
        screen.blit(game_images['player'], (playerX, playerY))
        baseX -= scrollSpeed
        if abs(baseX) > screenWidth:
            baseX = 0

        # display score
        playerMidPos = playerX + game_images['player'].get_width() / 2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + pipeWidth / 2
            if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                score += 1

        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += game_images['score'][digit].get_width()
        scoreX = (screenWidth - width) / 2
        scoreY = screenHeight * 0.12

        for digit in myDigits:
            screen.blit(game_images['score'][digit], (scoreX, scoreY))
            scoreX += game_images['score'][digit].get_width()

        pygame.display.update()
        fps_clock.tick(framePerSecond)


if __name__ == "__main__":
    # initialize pygame modules
    pygame.init()
    fps_clock = pygame.time.Clock() # control frame per second
    fps_clock.tick(framePerSecond)
    pygame.display.set_caption('Adventures of Flappy Bird')
    load_images()

    while True:
        startGame()

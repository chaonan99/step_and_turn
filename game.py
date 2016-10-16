# Step and Turn
# By chaonan99 (Haonan Chen) chenhaonan1995@gmail.com
# 2016/10/16

import pygame, sys, random, os, copy
from pygame.locals import *
import AI
from TwoPlayersGame import TwoPlayersGame

# Create the constants
TILESIZE = 80
WINWIDTH = 800 # width of the program's window, in pixels
WINHEIGHT = 600 # height in pixels
HALF_WINWIDTH = int(WINWIDTH / 2)
HALF_WINHEIGHT = int(WINHEIGHT / 2)
FPS = 30
CAM_MOVE_SPEED = 1

# The total width and height of each tile in pixels.
TILEWIDTH = 50
TILEHEIGHT = 85
TILEFLOORHEIGHT = 40

# The percentage of outdoor tiles that have additional
# decoration on them, such as a tree or rock.
OUTSIDE_DECORATION_PCT = 20

#              R    G    B
NAVYBLUE   = ( 60,  60, 100)
WHITE      = (255, 255, 255)
GREEN      = (  0, 255,   0)

BGCOLOR = NAVYBLUE
TILECOLOR = GREEN
TEXTCOLOR = WHITE
BASICFONTSIZE = 20

# Size of one character in the original resource
CHARACTERSIZE = 96

# direction of player
UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

# state of the game
STEP_PLAYER1 = 'step_1'
LIGHT_PLAYER1 = 'light_1'
TURN_PLAYER1 = 'turn_1'
READY_PLAYER1 = 'ready_1'
STEP_PLAYER2 = 'step_2'
LIGHT_PLAYER2 = 'light_2'
TURN_PLAYER2 = 'turn_2'
READY_PLAYER2 = 'ready_2'
AIPLAY1 = 'ai_play_1'
AIPLAY2 = 'ai_play_2'

# map symbols in level file to directions
DIRECTION1 = {'A':LEFT, 'S':DOWN, 'D':RIGHT, 'W':UP}
DIRECTION2 = {'J':LEFT, 'K':DOWN, 'L':RIGHT, 'I':UP}

# direction set
DIRECTIONSET = {'1':['W', 'D', 'S', 'A'], '2':['I', 'L', 'K', 'J']}


class StepTurnAI(TwoPlayersGame):
    def __init__(self, players, levelObj = None):
        # super(StepTurnAI, self).__init__()
        print(players)
        self.players = players
        self.levelObj = levelObj
        self.nplayer = 1  # player 1 starts.

    def possible_moves(self):
        print('call')
        if self.nplayer == 1:
            army = self.levelObj['army1']
            enemy = self.levelObj['army2']
        else:
            army = self.levelObj['army2']
            enemy = self.levelObj['army1']
        moves = []
        for soldier in army:
            if soldierCanMove(self.levelObj['mapObj'], soldier, army + enemy):
                move = {'from':list(soldier.getPosition()), 'turnPos':[], 'turn':None}
                for soldierTurn in army:
                    move['turnPos'] = list(soldierTurn.getPosition())
                    for turn in range(0, 1):  # 0 for left, 1 for right
                        move['turn'] = turn
                        moves.append(copy.deepcopy(move))
        print(moves)
        return moves

    def make_move(self, move):
        turn = move['turn']
        stepForwardAt(move['from'], self.levelObj['army1'] + self.levelObj['army2'])
        if turn == 0:
            turnLeftAt(move['turnPos'], self.levelObj['army1'] + self.levelObj['army2'])
        else:
            turnRightAt(move['turnPos'], self.levelObj['army1'] + self.levelObj['army2'])

    # def show(self):

    def lose(self):
        if self.nplayer == 1:
            army = self.levelObj['army1']
            enemy = self.levelObj['army2']
        else:
            army = self.levelObj['army2']
            enemy = self.levelObj['army1']
        return not canMove(self.levelObj['mapObj'], army, enemy)

    def scoring(self):
        score = 0
        if self.nplayer == 1:
            army = self.levelObj['army1']
            enemy = self.levelObj['army2']
        else:
            army = self.levelObj['army2']
            enemy = self.levelObj['army1']
        for soldier in army:
            if soldierCanMove(self.levelObj['mapObj'], soldier, army + enemy):
                score = score + 50
        return score

    def is_over(self):
        return self.lose()


class ImageProvider(object):
    """ImageProvider: Provide character image for two players"""
    __currentImageIdx = [0, 3]
    mapToPosition = (CHARACTERSIZE * 3, CHARACTERSIZE * 2, 0, CHARACTERSIZE)

    def __init__(self):
        super(ImageProvider, self).__init__()
        self.allImage = [pygame.image.load('resource/001_00.png'),
            pygame.image.load('resource/002_00.png'),
            pygame.image.load('resource/003_00.png'),
            pygame.image.load('resource/004_00.png'),
            pygame.image.load('resource/005_00.png'),
            pygame.image.load('resource/006_00.png'),
            pygame.image.load('resource/007_00.png'),
            pygame.image.load('resource/008_00.png'),
            pygame.image.load('resource/009_00.png'),
            pygame.image.load('resource/010_00.png'),
            pygame.image.load('resource/011_00.png'),
            pygame.image.load('resource/012_00.png'),
            pygame.image.load('resource/013_00.png'),
            pygame.image.load('resource/014_00.png'),
            pygame.image.load('resource/015_00.png'),
            pygame.image.load('resource/016_00.png'),
            pygame.image.load('resource/017_00.png'),
            pygame.image.load('resource/018_10.png'),
            pygame.image.load('resource/022_00.png'),
            pygame.image.load('resource/026_00.png'),
            pygame.image.load('resource/027_00.png'),
            pygame.image.load('resource/029_00.png'),
            pygame.image.load('resource/035_00.png'),
            pygame.image.load('resource/036_00.png'),
            pygame.image.load('resource/039_00.png'),
            pygame.image.load('resource/040_00.png'),
            pygame.image.load('resource/041_00.png'),
            pygame.image.load('resource/042_00.png'),
            pygame.image.load('resource/043_00.png'),
            pygame.image.load('resource/046_00.png'),
            pygame.image.load('resource/047_00.png'),
            pygame.image.load('resource/052_00.png'),
            pygame.image.load('resource/055_00.png'),
            pygame.image.load('resource/064_00.png'),
            pygame.image.load('resource/065_00.png'),
            pygame.image.load('resource/071_00.png'),
            pygame.image.load('resource/084_00.png'),
            pygame.image.load('resource/115_00.png'),
            pygame.image.load('resource/116_00.png'),
            pygame.image.load('resource/117_00.png'),
            pygame.image.load('resource/145_00.png'),
            ]
        self.__currentImageIdx[0] = random.randint(0, len(self.allImage))
        self.__currentImageIdx[1] = random.randint(0, len(self.allImage) - 1)
        if self.__currentImageIdx[1] == self.__currentImageIdx[0]:
            self.__currentImageIdx[1] = self.__currentImageIdx[1] + 1

    def getImage(self, direction, narmy):  # get image by direction and player number
        startx = self.mapToPosition[direction]
        oriImg = self.allImage[self.__currentImageIdx[narmy]]
        cropped = pygame.Surface((CHARACTERSIZE, CHARACTERSIZE), pygame.SRCALPHA, 32)
        cropped = cropped.convert_alpha()
        cropped.blit(oriImg, (0, 0), (0, startx, CHARACTERSIZE, CHARACTERSIZE))
        cropped = pygame.transform.scale(cropped, (TILEWIDTH, TILEWIDTH))
        return cropped

    def changeCharacter(self, narmy):  # change character of narmy player
        step = 1
        if (self.__currentImageIdx[narmy] + 1) % len(self.allImage) == self.__currentImageIdx[narmy - 1]:
            step = 2
        self.__currentImageIdx[narmy] = (self.__currentImageIdx[narmy] + step) % len(self.allImage)


class Soldier(object):
    """Soldier class"""
    def __init__(self, x, y, direction, narmy):
        super(Soldier, self).__init__()
        self.x = x                  # x coordinate on the map
        self.y = y                  # y coordinate on the map
        self.direction = direction  # current direction
        self.narmy = narmy          # belongs to which army

    def getPosition(self):
        return (self.x, self.y)

    def stepForward(self):
        if self.direction == UP:
            self.y = self.y - 1
        elif self.direction == DOWN:
            self.y = self.y + 1
        elif self.direction == LEFT:
            self.x = self.x - 1
        elif self.direction == RIGHT:
            self.x = self.x + 1

    def turnRight(self):
        self.direction = (self.direction + 1) % 4

    def turnLeft(self):
        self.direction = (self.direction - 1) % 4


def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT

    pygame.init()
    loadImage()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINWIDTH, WINHEIGHT))
    pygame.display.set_caption('Step and Turn')
    BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)

    startScreen()

    levels = readLevelsFile('stepturnLevel.txt')
    currentLevelIndex = 0

    while True:
        result = runGame(levels, currentLevelIndex)

        if result in ('solved', 'next'):
            # Go to the next level.
            currentLevelIndex += 1
            if currentLevelIndex >= len(levels):
                # If there are no more levels, go back to the first one.
                currentLevelIndex = 0
        elif result == 'back':
            # Go to the previous level.
            currentLevelIndex -= 1
            if currentLevelIndex < 0:
                # If there are no previous levels, go to the last one.
                currentLevelIndex = len(levels)-1
        elif result == 'reset':
            pass


def loadImage():
    """Load game resources"""
    # Gobal dict value that will contain all the Pygame
    # Surface objects returned by pygame.image.load().
    global IMAGESDICT, TILEMAPPING, OUTSIDEDECOMAPPING, PLAYERIMAGES, MOVEHINT
    IMAGESDICT = {'turn hint': pygame.image.load('resource/RedSelector.png'),
        'step hint': pygame.image.load('resource/Selector.png'),
        'corner': pygame.image.load('resource/Wall_Block_Tall.png'),
        'wall': pygame.image.load('resource/Wood_Block_Tall.png'),
        'inside floor': pygame.image.load('resource/Plain_Block.png'),
        'outside floor': pygame.image.load('resource/Grass_Block.png'),
        'title': pygame.image.load('resource/startscreen.png'),
        'win': pygame.image.load('resource/win.png'),
        'fail': pygame.image.load('resource/fail.png'),
        'rock': pygame.image.load('resource/Rock.png'),
        'short tree': pygame.image.load('resource/Tree_Short.png'),
        'tall tree': pygame.image.load('resource/Tree_Tall.png'),
        'ugly tree': pygame.image.load('resource/Tree_Ugly.png')}

    # These dict values are global, and map the character that appears
    # in the level file to the Surface object it represents.
    TILEMAPPING = {'x': IMAGESDICT['corner'],
        '#': IMAGESDICT['wall'],
        'o': IMAGESDICT['inside floor'],
        ' ': IMAGESDICT['outside floor']}
    OUTSIDEDECOMAPPING = {'1': IMAGESDICT['rock'],
        '2': IMAGESDICT['short tree'],
        '3': IMAGESDICT['tall tree'],
        '4': IMAGESDICT['ugly tree']}
    MOVEHINT = [ IMAGESDICT['step hint'],
        IMAGESDICT['turn hint'],  # North
        IMAGESDICT['turn hint'],  # West
        IMAGESDICT['turn hint'],  # South
        IMAGESDICT['turn hint']]  # East

    PLAYERIMAGES = ImageProvider()


def runGame(levels, levelNum):
    """Run a level of game"""
    global cameraOffsetX, cameraOffsetY, mapWidth, mapHeight
    from Player import Human_Player, AI_Player
    from AI import Negamax

    levelObj = copy.deepcopy(levels[levelNum])
    ai_algo = Negamax(5)
    game = StepTurnAI([Human_Player(), AI_Player(ai_algo)], levelObj)
    isAI1 = False
    isAI2 = True
    mapObj = decorateMap(levelObj['mapObj'], levelObj['army1'], levelObj['army2'])
    mapNeedsRedraw = True  # set to True to call drawMap()
    state = STEP_PLAYER1
    levelSurf = BASICFONT.render('Level %s of %s' % (levelNum + 1, len(levels)), 1, TEXTCOLOR)
    levelRect = levelSurf.get_rect()
    levelRect.bottomleft = (20, WINHEIGHT - 45)
    cameraOffsetX = 0
    cameraOffsetY = 0
    mapWidth = len(mapObj) * TILEWIDTH
    mapHeight = (len(mapObj[0]) - 1) * TILEFLOORHEIGHT + TILEHEIGHT
    MAX_CAM_X_PAN = abs(HALF_WINHEIGHT - int(mapHeight / 2)) + TILEWIDTH
    MAX_CAM_Y_PAN = abs(HALF_WINWIDTH - int(mapWidth / 2)) + TILEHEIGHT

    mousex = 0 # used to store x coordinate of mouse event
    mousey = 0 # used to store y coordinate of mouse event
    currentOn = [None, None]
    holdList = []
    # Track how much the camera has moved:
    # Track if the keys to move the camera are being held down:
    cameraUp = False
    cameraDown = False
    cameraLeft = False
    cameraRight = False
    mhint = [[None, None]] * 5
    winPlayer = 0

    while True:
        mouseClicked = False
        keyPressed = False

        # event handling loop
        for event in pygame.event.get():
            if event.type == QUIT:
                # Player clicked the "X" at the corner of the window.
                terminate()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True
            elif event.type == KEYDOWN:
                # Handle key presses
                keyPressed = True
                if event.key == K_p:
                    PLAYERIMAGES.changeCharacter(getArmyFromState(state)-1)
                    mapNeedsRedraw = True
                # Set the camera move mode.
                elif event.key == K_d:
                    cameraLeft = True
                elif event.key == K_a:
                    cameraRight = True
                elif event.key == K_s:
                    cameraUp = True
                elif event.key == K_w:
                    cameraDown = True

                elif event.key == K_n:
                    return 'next'
                elif event.key == K_b:
                    return 'back'
                elif event.key == K_ESCAPE:
                    terminate() # Esc key quits.
                elif event.key == K_BACKSPACE:
                    return 'reset' # Reset the level.

                elif event.key == K_i:
                    if state in [STEP_PLAYER1, LIGHT_PLAYER1]:
                        isAI1 = True
                        state = AIPLAY1
                    elif state in [STEP_PLAYER2, LIGHT_PLAYER2]:
                        isAI2 = True
                        state = AIPLAY2
                    else:
                        pass
                    pl1 = AI_Player(ai_algo) if isAI1 else Human_Player()
                    pl2 = AI_Player(ai_algo) if isAI2 else Human_Player()
                    game = StepTurnAI([pl1, pl2], levelObj)
                elif event.key == K_o:
                    isAI1 = False
                    isAI2 = False
                    if getArmyFromState(state) == 1:
                        state = STEP_PLAYER1
                    elif getArmyFromState(state) == 2:
                        state = STEP_PLAYER2
                    game = StepTurnAI([Human_Player(), Human_Player()], levelObj)

            elif event.type == KEYUP:
                # Unset the camera move mode.
                if event.key == K_d:
                    cameraLeft = False
                elif event.key == K_a:
                    cameraRight = False
                elif event.key == K_s:
                    cameraUp = False
                elif event.key == K_w:
                    cameraDown = False

        # state transfer, construct hints
        if winPlayer != 0:
            if keyPressed:
                if winPlayer == 2:
                    return 'reset'
                else:
                    return 'next'

        elif state == STEP_PLAYER1:
            assert canMove(levelObj['mapObj'], levelObj['army1'], levelObj['army2']), \
             'Invalid map!!!'
            holdList = getHighlight(mousex, mousey, levelObj['mapObj'],
                levelObj['army1'], levelObj['army2'])
            mhint[0] = holdList[1]
            currentOn = holdList[0]
            if mhint[0] != [None, None]:
                mapNeedsRedraw = True
                state = LIGHT_PLAYER1

        elif state == LIGHT_PLAYER1:
            temp = list(getTileAtPixel(mousex, mousey))
            if temp not in holdList:
                mhint[0] = [None, None]
                currentOn = [None, None]
                mapNeedsRedraw = True
                state = STEP_PLAYER1
            elif mouseClicked:
                stepForwardAt(currentOn, levelObj['army1'])
                mhint[0] = [None, None]
                currentOn = [None, None]
                mapNeedsRedraw = True
                state = TURN_PLAYER1

        elif state == TURN_PLAYER1:
            if not canMove(levelObj['mapObj'], levelObj['army2'], levelObj['army1']):
                winPlayer = 1
            holdList = getTurnHold(mousex, mousey, levelObj['army1'])
            currentOn = holdList[0]
            mhint[1:5] = getTurnlight(mousex, mousey, levelObj['army1'])
            if holdList[1] != [None, None]:
                mapNeedsRedraw = True
                state = READY_PLAYER1

        elif state == READY_PLAYER1:
            temp = list(getTileAtPixel(mousex, mousey))
            if temp not in holdList:
                mhint[1:5] = [None, None] * 4
                mapNeedsRedraw = True
                state = TURN_PLAYER1
            elif mouseClicked:
                if temp == holdList[1]:
                    turnRightAt(currentOn, levelObj['army1'])
                elif temp == holdList[2]:
                    turnLeftAt(currentOn, levelObj['army1'])
                else:
                    pass
                mapNeedsaRedraw = True
                state = AIPLAY2 if isAI2 else STEP_PLAYER2
                mhint[1:5] = [None, None] * 4
                currentOn = [None, None]
                game.switch_player()

        elif state == STEP_PLAYER2:
            assert canMove(levelObj['mapObj'], levelObj['army2'], levelObj['army1']), \
             'Program error. State transfer problem!'
            holdList = getHighlight(mousex, mousey, levelObj['mapObj'],
                levelObj['army2'], levelObj['army1'])
            mhint[0] = holdList[1]
            currentOn = holdList[0]
            if mhint[0] != [None, None]:
                mapNeedsRedraw = True
                state = LIGHT_PLAYER2

        elif state == LIGHT_PLAYER2:
            temp = list(getTileAtPixel(mousex, mousey))
            if temp not in holdList:
                mhint[0] = [None, None]
                currentOn = [None, None]
                mapNeedsRedraw = True
                state = STEP_PLAYER2
            elif mouseClicked:
                stepForwardAt(currentOn, levelObj['army2'])
                mapNeedsRedraw = True
                mhint[0] = [None, None]
                currentOn = [None, None]
                state = TURN_PLAYER2

        elif state == TURN_PLAYER2:
            if not canMove(levelObj['mapObj'], levelObj['army1'], levelObj['army2']):
                winPlayer = 2
            holdList = getTurnHold(mousex, mousey, levelObj['army2'])
            currentOn = holdList[0]
            mhint[1:5] = getTurnlight(mousex, mousey, levelObj['army2'])
            if holdList[1] != [None, None]:
                mapNeedsRedraw = True
                state = READY_PLAYER2

        elif state == READY_PLAYER2:
            temp = list(getTileAtPixel(mousex, mousey))
            if temp not in holdList:
                mhint[1:5] = [None, None] * 4
                mapNeedsRedraw = True
                state = TURN_PLAYER2
            elif mouseClicked:
                if temp == holdList[1]:
                    turnRightAt(currentOn, levelObj['army2'])
                elif temp == holdList[2]:
                    turnLeftAt(currentOn, levelObj['army2'])
                else:
                    pass
                mapNeedsRedraw = True
                state = AIPLAY1 if isAI1 else STEP_PLAYER1
                mhint[1:5] = [None, None] * 4
                currentOn = [None, None]
                game.switch_player()

        elif state == AIPLAY1:
            game.oneStep()
            mapNeedsRedraw = True
            if not canMove(levelObj['mapObj'], levelObj['army2'], levelObj['army1']):
                winPlayer = 1
            if isAI2:
                state = AIPLAY2
            else:
                state = STEP_PLAYER2

        elif state == AIPLAY2:
            game.oneStep()
            mapNeedsRedraw = True
            if not canMove(levelObj['mapObj'], levelObj['army1'], levelObj['army2']):
                winPlayer = 2
            if isAI1:
                state = AIPLAY1
            else:
                state = STEP_PLAYER1

        # game surf draw
        DISPLAYSURF.fill(BGCOLOR)

        if mapNeedsRedraw:
            mapSurf = drawMap(mapObj, levelObj['army1'], levelObj['army2'], mhint)
            mapNeedsRedraw = False

        if cameraUp and cameraOffsetY < MAX_CAM_X_PAN:
            cameraOffsetY += CAM_MOVE_SPEED
        elif cameraDown and cameraOffsetY > -MAX_CAM_X_PAN:
            cameraOffsetY -= CAM_MOVE_SPEED
        if cameraLeft and cameraOffsetX < MAX_CAM_Y_PAN:
            cameraOffsetX += CAM_MOVE_SPEED
        elif cameraRight and cameraOffsetX > -MAX_CAM_Y_PAN:
            cameraOffsetX -= CAM_MOVE_SPEED

        mapSurfRect = mapSurf.get_rect()
        mapSurfRect.center = (HALF_WINWIDTH + cameraOffsetX, HALF_WINHEIGHT + cameraOffsetY)
        DISPLAYSURF.blit(mapSurf, mapSurfRect)
        DISPLAYSURF.blit(levelSurf, levelRect)
        nplayerSurf = BASICFONT.render('Current: player %s ' % getArmyFromState(state), 1, TEXTCOLOR)
        stepRect = nplayerSurf.get_rect()
        stepRect.bottomleft = (20, WINHEIGHT - 10)
        DISPLAYSURF.blit(nplayerSurf, stepRect)
        currentPlayerImage = PLAYERIMAGES.getImage(DOWN, getArmyFromState(state) - 1)
        currentPlayerImageRect = currentPlayerImage.get_rect()
        currentPlayerImageRect.bottomleft = (180, WINHEIGHT - 5)
        DISPLAYSURF.blit(currentPlayerImage, currentPlayerImageRect)

        if winPlayer != 0:
            if winPlayer == 1:
                solvedImage = IMAGESDICT['win']
            elif winPlayer == 2:
                solvedImage = IMAGESDICT['fail']
            solvedRect = solvedImage.get_rect()
            solvedRect.center = (HALF_WINWIDTH, HALF_WINHEIGHT)
            DISPLAYSURF.blit(solvedImage, solvedRect)

        pygame.display.update()
        FPSCLOCK.tick()


def canMove(mapObj, army, enemy):
    """Judge if any soldier in army can move"""
    for soldier in army:
        if soldierCanMove(mapObj, soldier, army + enemy):
            return True

    return False


def soldierCanMove(mapObj, soldier, allarmy):
    direction = soldier.direction
    x, y = soldier.getPosition()
    if direction == UP:
        xOffset = 0
        yOffset = -1
    elif direction == RIGHT:
        xOffset = 1
        yOffset = 0
    elif direction == DOWN:
        xOffset = 0
        yOffset = 1
    elif direction == LEFT:
        xOffset = -1
        yOffset = 0

    if not isWall(mapObj, x + xOffset, y + yOffset) and not isSoldier(allarmy, x + xOffset, y + yOffset):
        return True
    else:
        return False

def getTileAtPixel(x, y):
    """Convert mouse point to coordinate on the map"""
    mapLeftMargin = HALF_WINWIDTH + cameraOffsetX - mapWidth/2
    mapTopMargin = HALF_WINHEIGHT + cameraOffsetY - mapHeight/2
    px = 0
    py = 0
    for tilexp in range(mapLeftMargin, mapLeftMargin + mapWidth, TILEWIDTH):
        py = 0
        for tileyp in range(mapTopMargin, mapTopMargin + mapHeight - TILEFLOORHEIGHT, TILEFLOORHEIGHT):
            tileRect = pygame.Rect(tilexp, tileyp - TILEFLOORHEIGHT, TILEWIDTH, TILEHEIGHT)
            if tileRect.collidepoint(x, y):
                return (px, py)
            py = py + 1
        px = px + 1
    return (None, None)


def getArmyFromState(state):
    """Convert state of game to army number"""
    return 1 if '1' in state else 2


def getTurnlight(mousex, mousey, army):
    """Get turn hint"""
    x, y = getTileAtPixel(mousex, mousey)
    if x != None and y != None:
        direction = getDirectionByPosition(x, y, army)
        if direction == UP or direction == DOWN:
            return [[None, None], [x - 1, y], [None, None], [x + 1, y]]
        elif direction == RIGHT or direction == LEFT:
            return [[x, y - 1], [None, None], [x, y + 1], [None, None]]
        else:
            return [[None, None]] * 4

    return [[None, None]] * 4


def getTurnHold(mousex, mousey, army):
    """Get hold on list of turn"""
    x, y = getTileAtPixel(mousex, mousey)
    if x != None and y != None:
        direction = getDirectionByPosition(x, y, army)
        if direction == UP:
            return [[x, y], [x + 1, y], [x - 1, y]]
        elif direction == DOWN:
            return [[x, y], [x - 1, y], [x + 1, y]]
        elif direction == LEFT:
            return [[x, y], [x, y - 1], [x, y + 1]]
        elif direction == RIGHT:
            return [[x, y], [x, y + 1], [x, y - 1]]
        else:
            return [[None, None]] * 3

    return [[None, None]] * 3


def getHighlight(mousex, mousey, mapObj, army, enemy):
    """Get step hint"""
    x, y = getTileAtPixel(mousex, mousey)
    if x != None and y != None:
        direction = getDirectionByPosition(x, y, army)
        if direction == UP:
            xOffset = 0
            yOffset = -1
        elif direction == RIGHT:
            xOffset = 1
            yOffset = 0
        elif direction == DOWN:
            xOffset = 0
            yOffset = 1
        elif direction == LEFT:
            xOffset = -1
            yOffset = 0
        else:
            return [[None, None]] * 2

        if isWall(mapObj, x + xOffset, y + yOffset) or isSoldier(enemy + army, x + xOffset, y + yOffset):
            return [[x, y], [None, None]]
        else:
            return [[x, y], [x + xOffset, y + yOffset]]

    return [[None, None]] * 2


def isSoldier(army, x, y):
    """Returns True if there is a soldier in the army
    on position (x, y)"""
    return getDirectionByPosition(x, y, army) != None


def isWall(mapObj, x, y):
    """Returns True if the (x, y) position on
    the map is a wall, otherwise return False."""
    if x < 0 or x >= len(mapObj) or y < 0 or y >= len(mapObj[x]):
        return False # x and y aren't actually on the map.
    elif mapObj[x][y] in ('#', 'x'):
        return True # wall is blocking
    return False


def decorateMap(mapObj, army1, army2):
    """Makes a copy of the given map object and modifies it.
    Here is what is done to it:
        * Walls that are corners are turned into corner pieces.
        * The outside/inside floor tile distinction is made.
        * Tree/rock decorations are randomly added to the outside tiles.

    Returns the decorated map object."""

    # Copy the map object so we don't modify the original passed
    mapObjCopy = copy.deepcopy(mapObj)

    # Remove the non-wall characters from the map data
    for x in range(len(mapObjCopy)):
        for y in range(len(mapObjCopy[0])):
            if mapObjCopy[x][y] in ('A', 'W', 'S', 'D', 'J', 'I', 'L', 'K'):
                mapObjCopy[x][y] = ' '

    # Flood fill to determine inside/outside floor tiles.
    for soldier in army1:
        floodFill(mapObjCopy, soldier.getPosition(), ' ', 'o')
    for soldier in army2:
        floodFill(mapObjCopy, soldier.getPosition(), ' ', 'o')

    # Convert the adjoined walls into corner tiles.
    for x in range(len(mapObjCopy)):
        for y in range(len(mapObjCopy[0])):

            if mapObjCopy[x][y] == '#':
                if (isWall(mapObjCopy, x, y-1) and isWall(mapObjCopy, x+1, y)) or \
                     (isWall(mapObjCopy, x+1, y) and isWall(mapObjCopy, x, y+1)) or \
                     (isWall(mapObjCopy, x, y+1) and isWall(mapObjCopy, x-1, y)) or \
                     (isWall(mapObjCopy, x-1, y) and isWall(mapObjCopy, x, y-1)):
                    mapObjCopy[x][y] = 'x'

            elif mapObjCopy[x][y] == ' ' and random.randint(0, 99) < OUTSIDE_DECORATION_PCT:
                mapObjCopy[x][y] = random.choice(list(OUTSIDEDECOMAPPING.keys()))

    return mapObjCopy


def floodFill(mapObj, position, oldCharacter, newCharacter):
    """Changes any values matching oldCharacter on the map object to
    newCharacter at the (x, y) position, and does the same for the
    positions to the left, right, down, and up of (x, y), recursively."""

    # In this game, the flood fill algorithm creates the inside/outside
    # floor distinction. This is a "recursive" function.
    # For more info on the Flood Fill algorithm, see:
    #   http://en.wikipedia.org/wiki/Flood_fill
    x, y = position
    if mapObj[x][y] == oldCharacter:
        mapObj[x][y] = newCharacter

    if x < len(mapObj) - 1 and mapObj[x+1][y] == oldCharacter:
        floodFill(mapObj, (x+1, y), oldCharacter, newCharacter) # call right
    if x > 0 and mapObj[x-1][y] == oldCharacter:
        floodFill(mapObj, (x-1, y), oldCharacter, newCharacter) # call left
    if y < len(mapObj[x]) - 1 and mapObj[x][y+1] == oldCharacter:
        floodFill(mapObj, (x, y+1), oldCharacter, newCharacter) # call down
    if y > 0 and mapObj[x][y-1] == oldCharacter:
        floodFill(mapObj, (x, y-1), oldCharacter, newCharacter) # call up


def readLevelsFile(filename):
    """Read map from txt file"""
    assert os.path.exists(filename), 'Cannot find the level file: %s' % (filename)
    mapFile = open(filename, 'r')
    # Each level must end with a blank line
    content = mapFile.readlines() + ['\r\n']
    mapFile.close()

    levels = [] # Will contain a list of level objects.
    levelNum = 0
    mapTextLines = [] # contains the lines for a single level's map.
    mapObj = [] # the map object made from the data in mapTextLines
    for lineNum in range(len(content)):
        # Process each line that was in the level file.
        line = content[lineNum].rstrip('\r\n')

        if ';' in line:
            # Ignore the ; lines, they're comments in the level file.
            line = line[:line.find(';')]

        if line != '':
            # This line is part of the map.
            mapTextLines.append(line)
        elif line == '' and len(mapTextLines) > 0:
            # A blank line indicates the end of a level's map in the file.
            # Convert the text in mapTextLines into a level object.

            # Find the longest row in the map.
            maxWidth = -1
            for i in range(len(mapTextLines)):
                if len(mapTextLines[i]) > maxWidth:
                    maxWidth = len(mapTextLines[i])
            # Add spaces to the ends of the shorter rows. This
            # ensures the map will be rectangular.
            for i in range(len(mapTextLines)):
                mapTextLines[i] += ' ' * (maxWidth - len(mapTextLines[i]))

            # Convert mapTextLines to a map object.
            for x in range(len(mapTextLines[0])):
                mapObj.append([])
            for y in range(len(mapTextLines)):
                for x in range(maxWidth):
                    mapObj[x].append(mapTextLines[y][x])

            # Loop through the spaces in the map and find the @, ., and $
            # characters for the starting game state.
            army1 = []  # The x and y for the player1's starting positions
            army2 = []  # The x and y for the player2's starting positions
            for x in range(maxWidth):
                for y in range(len(mapObj[x])):
                    if mapObj[x][y] in ('A', 'W', 'S', 'D'):
                        army1.append(Soldier(x, y, DIRECTION1[mapObj[x][y]], 1))
                    if mapObj[x][y] in ('J', 'I', 'L', 'K'):
                        army2.append(Soldier(x, y, DIRECTION2[mapObj[x][y]], 2))

            # Basic level design sanity checks:
            assert len(army1) > 0 and len(army2) > 0, 'Less than 2 players in level %s' % levelNum + 1

            # Create level object and starting game state object.
            levelObj = {'width': maxWidth,
                        'height': len(mapObj),
                        'mapObj': mapObj,
                        'army1': army1,
                        'army2': army2}

            levels.append(levelObj)

            # Reset the variables for reading the next map.
            mapTextLines = []
            mapObj = []
            levelNum += 1
    return levels


def drawMap(mapObj, army1, army2, mhint):
    """Draws the map to a Surface object, including the player and
    stars. This function does not call pygame.display.update(), nor
    does it draw the "Level" and "Steps" text in the corner."""

    # mapSurf will be the single Surface object that the tiles are drawn
    # on, so that it is easy to position the entire map on the DISPLAYSURF
    # Surface object. First, the width and height must be calculated.
    mapSurfWidth = len(mapObj) * TILEWIDTH
    mapSurfHeight = (len(mapObj[0]) - 1) * TILEFLOORHEIGHT + TILEHEIGHT
    mapSurf = pygame.Surface((mapSurfWidth, mapSurfHeight))
    mapSurf.fill(BGCOLOR) # start with a blank color on the surface.
    armyPosition1 = [soldier.getPosition() for soldier in army1]
    armyPosition2 = [soldier.getPosition() for soldier in army2]

    # Draw the tile sprites onto this surface.
    for x in range(len(mapObj)):
        for y in range(len(mapObj[x])):
            spaceRect = pygame.Rect((x * TILEWIDTH, y * TILEFLOORHEIGHT, TILEWIDTH, TILEHEIGHT))
            if mapObj[x][y] in TILEMAPPING:
                baseTile = TILEMAPPING[mapObj[x][y]]
            elif mapObj[x][y] in OUTSIDEDECOMAPPING:
                baseTile = TILEMAPPING[' ']
            elif mapObj[x][y] in DIRECTION1 or mapObj[x][y] in DIRECTION2:
                baseTile = TILEMAPPING['o']

            # First draw the base ground/wall tile.
            mapSurf.blit(baseTile, spaceRect)

            if mapObj[x][y] in OUTSIDEDECOMAPPING:
                # Draw any tree/rock decorations that are on this tile.
                mapSurf.blit(OUTSIDEDECOMAPPING[mapObj[x][y]], spaceRect)
            elif (x, y) in armyPosition1:
                mapSurf.blit(PLAYERIMAGES.getImage(getDirectionByPosition(x, y, army1), 0), spaceRect)
            elif (x, y) in armyPosition2:
                mapSurf.blit(PLAYERIMAGES.getImage(getDirectionByPosition(x, y, army2), 1), spaceRect)
            if [x, y] in mhint:
                mapSurf.blit(MOVEHINT[mhint.index([x, y])], spaceRect)
    return mapSurf


def getDirectionByPosition(x, y, army):
    """Return the direction of soldier on (x, y)
    Return None if no soldier in the army is on (x, y)"""
    for soldier in army:
        if (x, y) == soldier.getPosition():
            return soldier.direction
    return None


def stepForwardAt(pos, army):
    """Call step movement at pos = (x, y)"""
    [soldier.stepForward() for soldier in army if pos == list(soldier.getPosition())]


def turnRightAt(pos, army):
    """Call turn right movement at pos = (x, y)"""
    [soldier.turnRight() for soldier in army if pos == list(soldier.getPosition())]


def turnLeftAt(pos, army):
    """Call turn left movement at pos = (x, y)"""
    [soldier.turnLeft() for soldier in army if pos == list(soldier.getPosition())]


def startScreen():
    """Display the start screen (which has the title and instructions)
    until the player presses a key. Returns None."""

    # Position the title image.
    titleRect = IMAGESDICT['title'].get_rect()
    topCoord = 50 # topCoord tracks where to position the top of the text
    titleRect.top = topCoord
    titleRect.centerx = HALF_WINWIDTH
    topCoord += titleRect.height

    # Unfortunately, Pygame's font & text system only shows one line at
    # a time, so we can't use strings with \n newline characters in them.
    # So we will use a list with each line in it.
    instructionText = ['Step first and turn right or left next.',
                         'Hover your mouse to get hint, click mouse to move',
                         'WASD for camera control, P to change character.',
                         'Backspace to reset level, Esc to quit.',
                         'N for next level, B to go back a level.']

    # Start with drawing a blank color to the entire window:
    DISPLAYSURF.fill(BGCOLOR)

    # Draw the title image to the window:
    DISPLAYSURF.blit(IMAGESDICT['title'], titleRect)

    # Position and draw the text.
    for i in range(len(instructionText)):
        instSurf = BASICFONT.render(instructionText[i], 1, TEXTCOLOR)
        instRect = instSurf.get_rect()
        topCoord += 10 # 10 pixels will go in between each line of text.
        instRect.top = topCoord
        instRect.centerx = HALF_WINWIDTH
        topCoord += instRect.height # Adjust for the height of the line.
        DISPLAYSURF.blit(instSurf, instRect)

    while True: # Main loop for the start screen.
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                return # user has pressed a key, so return.

        # Display the DISPLAYSURF contents to the actual screen.
        pygame.display.update()
        FPSCLOCK.tick()


def terminate():
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
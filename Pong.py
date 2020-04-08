#!/usr/bin/python
# -*- coding: utf-8 -*-


#Now this project is available in github.


import pygame
import sys
from pygame.locals import *
from os.path import abspath

# ======================================== VARIABLES GLOBALES ==================================================

BOT_TIME_OF_REACTION = 0
DECREASE_REACTION_VALUE = 0
MULTIPLAYER = True

PAUSE = False

BAR_DIMENSIONS = (2, 2, 12, 96)  # Dimensions of the bar sprite
BALL_DIMENSIONS = (2, 2, 12, 12)  # Dimensions of the ball sprite
BARRIER_DIMENSIONS = (2, 1, 16, 31)

SPEED = 5  # Speed of the players

IMAGES_PATH = abspath('Images')  # Folder which contain the images of the game

(WIDTH, HEIGHT) = (1100, 600)  # Size values

(XBALL_DIR, YBALL_DIR) = (-2, 2)  # Ball direction to bounce
BALL_SPEED = 2

(PLAYER1_POINTS, PLAYER2_POINTS) = (0, 0)


# ===================================================================================================================================================================

class sprites(pygame.sprite.Sprite):

    def __init__(self):

        self.FONT = pygame.font.Font('freesansbold.ttf', 35)
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.PLAYER1_TEXT_POINTS = self.FONT.render('0', True,
                self.WHITE, self.BLACK)
        self.PLAYER2_TEXT_POINTS = self.FONT.render('0', True,
                self.WHITE, self.BLACK)

        self.PLAYER1_POINTS_POS = self.PLAYER1_TEXT_POINTS.get_rect()
        self.PLAYER1_POINTS_POS.center = (WIDTH // 2 - 80, 50)

        self.PLAYER2_POINTS_POS = self.PLAYER2_TEXT_POINTS.get_rect()
        self.PLAYER2_POINTS_POS.center = (WIDTH // 2 + 80, 50)

        self.WINNER = self.FONT.render('', True, self.WHITE, self.BLACK)
        self.PAUSE_TEXT = self.FONT.render('Paused', True, self.WHITE,
                self.BLACK)

# ===================================================================================================================================================================

    def new_image(self, path, transparence=False):
        try:
            self.character = pygame.image.load(path)
        except pygame.error as err:
            raise err

        self.character = self.character.convert()
        if transparence:
            self.colorOfTransparence = self.character.get_at((0, 0))
            self.character.set_colorkey(self.colorOfTransparence,
                    RLEACCEL)

        return self.character


# ===================================================================================================================================================================

class game(sprites):

    def __init__(self):
        pygame.init()

        super(game, self).__init__()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT),
                RESIZABLE)
        pygame.display.set_caption('Pong game')

        self.initScreen()

        self.start = pygame.time.get_ticks()

        # Sprites

        self.ball_Image = super().new_image(IMAGES_PATH + '\\ball.png',
                True)
        self.ball = self.ball_Image.get_rect()
        self.ball.left = WIDTH // 2
        self.ball.top = HEIGHT // 2

        self.pong_bar = super().new_image(IMAGES_PATH
                + '\\player_bar.png', True)
        self.player1 = self.pong_bar.get_rect()
        self.player2 = self.pong_bar.get_rect()

        self.player1.top = 40
        self.player2.top = 40
        self.player1.left = 30
        self.player2.left = WIDTH - 30

        self.barrier_image = super().new_image(IMAGES_PATH
                + '\\barrier.png', True)

        self.winner_text_pos = self.WINNER.get_rect()

        self.clock = pygame.time.Clock()

        self.process()

# ===================================================================================================================================================================

    def process(self):

        while 1:

            self.limits()
            self.time = self.clock.tick(60)
            self.screen.fill([0, 0, 0])
            self.movement()
            self.hitBall()

            for y in range(32, HEIGHT, 75):
                self.screen.blit(self.barrier_image, (WIDTH // 2
                                 - BARRIER_DIMENSIONS[2] // 2, y),
                                 BARRIER_DIMENSIONS)

            self.screen.blit(self.pong_bar, self.player1,
                             BAR_DIMENSIONS)  # Draw player1 bar
            self.screen.blit(self.pong_bar, self.player2,
                             BAR_DIMENSIONS)  # Draw player2 bar
            self.screen.blit(self.ball_Image, self.ball,
                             BALL_DIMENSIONS)  # Draw ball
            self.screen.blit(self.PLAYER1_TEXT_POINTS,
                             self.PLAYER1_POINTS_POS)  # Draw player1 points
            self.screen.blit(self.PLAYER2_TEXT_POINTS,
                             self.PLAYER2_POINTS_POS)  # Draw player2 points

            # Salir del programa

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.VIDEORESIZE:
                	self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
					self.player1.left = 30
					self.player2.left = WIDTH - 30
	        		self.winner_text_pos.center = (WIDTH // 2 - 150, HEIGHT // 2)


            pygame.display.flip()


        return

# ===================================================================================================================================================================

    def initScreen(self):
        global MULTIPLAYER

        initFont = pygame.font.Font('freesansbold.ttf', 100)

        # Variables del 1st loop

        screenText1 = initFont.render('Pong', True, self.WHITE,
                self.BLACK)
        screenText2 = initFont.render('Game', True, self.WHITE,
                self.BLACK)

        start = pygame.time.get_ticks()

        # Variables of the 2nd loop

        CHOICE = 0
        player1Choice = initFont.render('One player [1]', True,
                self.WHITE, self.BLACK)
        player2Choice = initFont.render('Two players [2]', True,
                self.WHITE, self.BLACK)
        controlsChoice = initFont.render('Controls [3]', True,
                self.WHITE, self.BLACK)

        while 1:

            now = pygame.time.get_ticks()
            if now - start >= 1500:
                self.screen.fill(self.BLACK)
                break

            self.screen.fill(self.BLACK)
            self.screen.blit(screenText1, (WIDTH // 2 - 150, HEIGHT
                             // 2 - 100))
            self.screen.blit(screenText2, (WIDTH // 2 - 150, HEIGHT
                             // 2))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

        while not CHOICE:

            self.screen.fill(self.BLACK)
            self.screen.blit(player1Choice, (WIDTH // 2 - 300, HEIGHT
                             // 2 - 200))
            self.screen.blit(player2Choice, (WIDTH // 2 - 300, HEIGHT
                             // 2 - 100))
            self.screen.blit(controlsChoice, (WIDTH // 2 - 300, HEIGHT
                             // 2))

            # Codigo

            key = pygame.key.get_pressed()
            if key[K_1]:
                CHOICE = 1
                MULTIPLAYER = False
                break
            elif key[K_2]:
                CHOICE = 2
                break
            elif key[K_3]:

                CHOICE = 3
                self.seeControls(False)
                break

            self.elec = CHOICE
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

        CHOICE = 0

# ===================================================================================================================================================================

    def Bot(self):
        steps = (self.player2.left - self.ball.left) // BALL_SPEED
        if YBALL_DIR > 0:
            ballPredictedPos = (self.player2.left + steps,
                                self.player2.top + steps)

            if ballPredictedPos[1] < HEIGHT and ballPredictedPos[0] \
                >= self.player2.left and ballPredictedPos[1] \
                not in range(self.player2.top, self.player2.top
                             + BAR_DIMENSIONS[3]):
                if self.player2.top < ballPredictedPos[1]:
                    self.player2.top += SPEED
                elif self.player2.top > ballPredictedPos[1]:

                    self.player2.top -= SPEED
        else:

            ballPredictedPos = (self.player2.left + steps,
                                self.player2.top - steps)

            if ballPredictedPos[1] > 0 and ballPredictedPos[0] \
                >= self.player2.left and ballPredictedPos[1] \
                not in range(self.player2.top, self.player2.top
                             + BAR_DIMENSIONS[3]):
                if self.player2.top > ballPredictedPos[1] \
                    or ballPredictedPos[1] \
                    not in range(self.player2.top, self.player2.top
                                 + BAR_DIMENSIONS[3]):
                    self.player2.top -= SPEED
                elif self.player2.top < ballPredictedPos[1]:

                    self.player2.top += SPEED

        self.start = pygame.time.get_ticks()

# ===================================================================================================================================================================

    def PauseGame(self):
        global PAUSE

        while PAUSE:

            self.screen.fill(self.BLACK)
            self.screen.blit(self.PAUSE_TEXT, (WIDTH // 2 - 80, HEIGHT
                             // 2))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:

                    if event.key == K_RETURN:
                        PAUSE = False
                        self.screen.fill(self.BLACK)
                        self.process()
        return

# ===================================================================================================================================================================

    def movement(self):
        global SPEED, PAUSE

        self.key = pygame.key.get_pressed()

        if self.key[K_w]:
            self.player1.top -= SPEED
        elif self.key[K_s]:
            self.player1.top += SPEED

        if self.key[K_ESCAPE]:
            PAUSE = True
            self.PauseGame()
        elif self.key[K_F2]:

            self.seeControls(True)

        if MULTIPLAYER:
            if self.key[K_UP]:
                self.player2.top -= SPEED
            elif self.key[K_DOWN]:
                self.player2.top += SPEED
        elif pygame.time.get_ticks() - self.start \
            >= BOT_TIME_OF_REACTION:

            self.Bot()

# ===================================================================================================================================================================

    def seeControls(self, playing):
        firstOp = self.FONT.render('[ARROWS] To move the player bar',
                                   True, self.WHITE, self.BLACK)
        secondOp = self.FONT.render('[ESC] To pause the game', True,
                                    self.WHITE, self.BLACK)
        thirdOp = self.FONT.render('[ENTER] To quit pause', True,
                                   self.WHITE, self.BLACK)
        fourthOp = self.FONT.render('[C] To exit this menu', True,
                                    self.WHITE, self.BLACK)
        fifthOP = self.FONT.render('[F2] Return to this menu', True,
                                   self.WHITE, self.BLACK)

        thisKey = pygame.key.get_pressed()
        while not thisKey[K_c]:

            thisKey = pygame.key.get_pressed()

            self.screen.fill(self.BLACK)
            self.screen.blit(firstOp, (WIDTH // 2 - 350, HEIGHT // 2
                             - 150))
            self.screen.blit(secondOp, (WIDTH // 2 - 350, HEIGHT // 2
                             - 100))
            self.screen.blit(thirdOp, (WIDTH // 2 - 350, HEIGHT // 2
                             - 50))
            self.screen.blit(fourthOp, (WIDTH // 2 - 350, HEIGHT // 2))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

        if not playing:
            self.initScreen()

# ===================================================================================================================================================================

    def limits(self):

        if self.player1.top <= 10:
            self.player1.top += SPEED * 2
        elif self.player1.top >= HEIGHT - BAR_DIMENSIONS[3] - 10:

            self.player1.top -= SPEED * 2

        if self.player2.top <= 10:
            self.player2.top += SPEED * 2
        elif self.player2.top >= HEIGHT - BAR_DIMENSIONS[3] - 10:

            self.player2.top -= SPEED * 2

# ===================================================================================================================================================================

    def hitBall(self):
        global XBALL_DIR, YBALL_DIR, BALL_SPEED, PLAYER1_POINTS, \
            PLAYER2_POINTS, BOT_TIME_OF_REACTION

        if self.ball.left in range(self.player1.left, self.player1.left
                                   + BAR_DIMENSIONS[2]) \
            and self.ball.top in range(self.player1.top,
                self.player1.top + BAR_DIMENSIONS[3]):  # If the ball collides with the player1 bar
            (XBALL_DIR, YBALL_DIR) = (BALL_SPEED, BALL_SPEED)  # The ball will go right and down
        elif self.ball.left in range(self.player2.left
                - BAR_DIMENSIONS[2], self.player2.left) \
            and self.ball.top in range(self.player2.top,
                self.player2.top + BAR_DIMENSIONS[3]):

            # If the ball collides with the player2 bar

            (XBALL_DIR, YBALL_DIR) = (-BALL_SPEED, -BALL_SPEED)  # The ball will go left and up
        elif self.ball.top >= HEIGHT - BALL_DIMENSIONS[3]:

            YBALL_DIR = -BALL_SPEED
        elif self.ball.top <= 0:

            YBALL_DIR = BALL_SPEED
        elif self.ball.left <= 0:

        # GET POINTS

            PLAYER2_POINTS += 1
            self.PLAYER2_TEXT_POINTS = \
                self.FONT.render(str(PLAYER2_POINTS), True, self.WHITE,
                                 self.BLACK)
            self.ball.left = WIDTH // 2
            self.ball.top = HEIGHT // 2
            BALL_SPEED += 1
            BOT_TIME_OF_REACTION -= DECREASE_REACTION_VALUE
            XBALL_DIR *= -1

            if PLAYER2_POINTS >= 15:
                self.WINNER = self.FONT.render('Player 2 won the game!!'
                        , True, self.WHITE, self.BLACK)
                self.gameOver()
        elif self.ball.left >= WIDTH - BALL_DIMENSIONS[2]:

            PLAYER1_POINTS += 1
            self.PLAYER1_TEXT_POINTS = \
                self.FONT.render(str(PLAYER1_POINTS), True, self.WHITE,
                                 self.BLACK)
            self.ball.left = WIDTH // 2
            self.ball.top = HEIGHT // 2
            BALL_SPEED += 1
            BOT_TIME_OF_REACTION -= DECREASE_REACTION_VALUE
            XBALL_DIR *= -1

            if PLAYER1_POINTS >= 15:
                self.WINNER = self.FONT.render('Player 1 won the game!!'
                        , True, self.WHITE, self.BLACK)
                self.gameOver()

        self.ball.top += YBALL_DIR
        self.ball.left += XBALL_DIR

# ===================================================================================================================================================================

    def gameOver(self):
        global PLAYER1_POINTS, PLAYER2_POINTS, BOT_TIME_OF_REACTION, \
            BALL_SPEED, XBALL_DIR, YBALL_DIR

        self.screen.fill(self.BLACK)
        self.screen.blit(self.WINNER, self.winner_text_pos)
        pygame.display.flip()
        pygame.time.delay(1500)
        self.initScreen()

        (PLAYER1_POINTS, PLAYER2_POINTS, BALL_SPEED) = (0, 0, 2)
        BOT_TIME_OF_REACTION = 1.0
        (XBALL_DIR, YBALL_DIR) = (-2, 2)


# ===================================================================================================================================================================

if __name__ == '__main__':
    pong = game()

# Gomoku Test Environment
# (by Marius Versteegen)

# FIRST, RUN THIS AT THE ANACONDA PROMPT (to download the pygame library)
# python -m pip install -U pygame --user
# or, in pycharm, click on the "Terminal" tab at the bottom to open a terminal.
# in the terminal, you can type the same as above to install the pygame libary.

# Let op!  Als je de game runt, lijkt er niets te gebeurren.
# De game start immers geminimaliseerd op, en zal knipperen op je task-bar.
# Klik op de game icon in de task-bar (een bijtje) om de game te maximaliseren.

# Tips + potentiele instinkers bij Gomoku
'''
    Deze voorbeeldcode heeft een aantal handige test-faciliteiten:
    - Via de klasse GmGameRules kun je de board afmetingen en het aantal stenen op een rij dat wint instellen.
    - Via een gui kun je zelf meespelen, als je een (of meerdere) human player toevoegt.
    - Je kunt de bordgrootte en het aantal stenen op een rij dat wint, vrij instellen, zolang het bord maar vierkant is.

    * Begin met het implementeren van de pseusdocode voor een zuivere MontecarloPlayer.
    * Test die met een klein board (2x2) om de basis-algoritmen te debuggen
    * Gebruik de debugger, met breakpoints en de mogelijkheid om dingen tijdens zo'n breakpoint 
        aan te roepen, zoals self.printTree(node)
    * Gebruik ook de profiler (in plaats van timeit) om een goed overzicht te krijgen van waar de 
      rekentijd zit.
    * Maak het bord 3x3 en test het 3 op een rij spel.
    * Je kunt een enkele move onderzoeken door je board vooraf een bepaalde waarde te geven, zoals
      [[1,2,0],[2,0,0],[1,0,0]] # 0=empty, 1=zwart, 2=wit
    * Let op bij FindSpotToExpand: een winning node is meteen ook een terminal node!
    * Maak een printNode en printTree functie, waardoor je snel een overzicht kunt krijgen van 
      een enkele node en haar kinderen of in het geval van printTree: de hele boom die er onder hangt.
      Print van elke node positie, N, Q en uct
    * Houd je Montecarlo-player klasse klein. Verhuis 2e orde utility functies naar een andere klasse
      met @staticmethod functies.
    * De beste move die je uiteindelijk selecteert is niet de move met de hoogste Q, maar de move met de hoogste Q/N
      (NB: de findspot to expand gebruikt daarentegen de uitkomst van de uct formule als criterium)
    * Je zult merken dat 5 op een rij op een 8x8 board met zuiver MontecarloPlayer als tegenstander nog goed
      werkt als die tegenstander zo'n 2 seconden de tijd heeft.
    * Om de effectiviteit van je heuristiek te testen zou je voorlopig op dat bord kunnen blijven testen,
      en kijken of je dankzij die heuristiek je rekentijd met een bepaalde factor kunt verkleinen-zonder dat het
      tegenspel slecht wordt.
      
    v1.1 update: het werkt nu ook als het boad een numpy array is.
    v1.4 update: gebruik overal (row,col) om moves te representeren. Geen (x,y) meer.
'''

# TODO: start with Move Center

import random, sys, pygame, time, math, copy
import numpy as np
from pygame.locals import KEYUP,QUIT,MOUSEBUTTONUP,K_ESCAPE
from gomoku import Board, Move, GameState, valid_moves, pretty_board
from GmUtils import GmUtils
from GmGameRules import GmGameRules
from gomoku_ai_marius1_webclient import gomoku_ai_marius1_webclient
from gomoku_ai_random_webclient import gomoku_ai_random_webclient
from basePlayer import basePlayer
from GmGame import GmGame
from GmQuickTests import GmQuickTests

# player gives an implementation the basePlayer cl
class randomPlayer(basePlayer):
    def __init__(self, black_=True):
        self.black = black_
    
        self.max_move_time_ns   = 0
        self.start_time_ns      = 0

    def new_game(self, black_: bool):
        """At the start of each new game you will be notified by the competition.
        this method has a boolean parameter that informs your agent whether you
        will play black or white.
        """
        self.black = black_

    def move(self, state: GameState, last_move: Move, max_time_to_move: int = 1000) -> Move:
        board = state[0]
        ply = state[1]
        
        validMoves = GmUtils.getValidMoves(board,ply)
                    
        return random.choice(validMoves)

    def id(self) -> str:
        """Please return a string here that uniquely identifies your submission e.g., "name (student_id)" """
        return "random_player"

class humanPlayer(basePlayer):
    def __init__(self, black_=True):
        self.black = black_
        
    def new_game(self, black_):
        self.black = black_

    def move(self, gamestate, last_move, max_time_to_move=1000):   
        board = gamestate[0]
        tokenx, tokeny = None, None
        while True:
            for event in pygame.event.get(): # event handling loop
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEBUTTONUP:
                    tokenx, tokeny = event.pos
                    if GmGame.YMARGIN < tokeny < GmGame.WINDOWHEIGHT-GmGame.YMARGIN and GmGame.XMARGIN < tokenx < GmGame.WINDOWWIDTH - GmGame.XMARGIN:
                        # place it
                        col = int((tokenx - GmGame.XMARGIN) / GmGame.SPACESIZE)
                        row = int((tokeny - GmGame.YMARGIN) / GmGame.SPACESIZE)
                        #print("row:{},col:{}".format(row,column))
                        if GmUtils.isValidMove(board, row, col):
                            return (row,col)
                    tokenx, tokeny = None, None
    
            if last_move!=None:
                GmGame.drawBoardWithExtraTokens(board,last_move[0],last_move[1],GmGame.MARKER)
            else:
                GmGame.drawBoard(board)
          
            pygame.display.update()
            GmGame.FPSCLOCK.tick()

    def id(self):
        return "Marius"

random.seed(0) # voor reproduceerbare debugging

humanPlayer1 = humanPlayer()
humanPlayer2 = humanPlayer()

aiPlayer1 = randomPlayer()
aiPlayer2 = gomoku_ai_marius1_webclient(True,GmGameRules.winningSeries,GmGameRules.BOARDWIDTH)
aiPlayer3 = gomoku_ai_random_webclient(True,GmGameRules.winningSeries,GmGameRules.BOARDWIDTH)

# uncomment the line below to test again yourself as human (player1 is black and starts the game)
# GmGame.start(player1=aiPlayer2,player2=humanPlayer2,max_time_to_move=1000,showIntermediateMoves=True) # don't speciry an aiPlayer for Human vs Human games

# uncomment the line below to run some simple tests for quick analysis and debugging.
GmQuickTests.doAllTests(aiPlayer2)


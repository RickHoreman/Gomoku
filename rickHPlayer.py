import random
from gomoku import Move, GameState, pretty_board as printBoard
from GmUtils import GmUtils, basePlayer
from time import time
from node import Node

# This default base player does a randomn move
class rickHPlayer(basePlayer):
    """This class specifies a player that just does random moves.
    The use of this class is two-fold: 1) You can use it as a base random roll-out policy.
    2) it specifies the required methods that will be used by the competition to run
    your player
    """
    def __init__(self, black_: bool = True):
        """Constructor for the player."""
        self.black = black_
        self.nRoot = None

    def new_game(self, black_: bool):
        """At the start of each new game you will be notified by the competition.
        this method has a boolean parameter that informs your agent whether you
        will play black or white.
        """
        self.black = black_
        self.nRoot = None

    # O(1) want duurt altijd more or less max_time_to_move
    def move(self, state: GameState, last_move: Move, max_time_to_move: int = 1000) -> Move:
        """This is the most important method: the agent will get:
        1) the current state of the game
        2) the last move by the opponent
        3) the available moves you can play (this is a special service we provide ;-) )
        4) the maximum time until the agent is required to make a move in milliseconds [diverging from this will lead to disqualification].
        """
        startTimeMS = time()*1000
        if(last_move == () and self.black):
            return (len(state[0])//2,len(state[0])//2)
        if(self.nRoot == None):
            self.nRoot = Node(state, last_move)
        else:
            self.nRoot = self.nRoot.childWithMove(last_move)
            if(self.nRoot == None):
                self.nRoot = Node(state, last_move)
            self.nRoot.parent = None
        while time()*1000-startTimeMS < max_time_to_move * 0.90:
            nLeaf = self.nRoot.findSpotToExpand()
            val = nLeaf.rollout(self.black)
            nLeaf.backupValue(val)
        bestChild = self.nRoot.bestChild()
        self.nRoot = bestChild
        self.nRoot.parent = None
        return bestChild.lastMove

    def id(self) -> str:
        """Please return a string here that uniquely identifies your submission e.g., "name (student_id)" """
        return "Rick's Mega Pog Ultra Gamer Agent (ggez)"
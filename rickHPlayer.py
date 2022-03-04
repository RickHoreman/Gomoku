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

    def move(self, state: GameState, last_move: Move, max_time_to_move: int = 1000) -> Move:
        """This is the most important method: the agent will get:
        1) the current state of the game
        2) the last move by the opponent
        3) the available moves you can play (this is a special service we provide ;-) )
        4) the maximum time until the agent is required to make a move in milliseconds [diverging from this will lead to disqualification].
        """
        if(self.black):
            colour = "black/o"
        else:
            colour = "white/x"
        print(f"move! {colour} ply: {state[1]}")
        print(f"root: {self.nRoot}")
        startTimeMS = time()*1000
        if(last_move == () and self.black):
            return (len(state[0])//2,len(state[0])//2)
        print(f"last_move: {last_move}")
        printBoard(state[0])
        if(self.nRoot == None):
            debug = [0,0,0,0,0]
            self.nRoot = Node(state, last_move, debug=debug)
        else:
            self.nRoot = self.nRoot.childWithMove(last_move)
            if(self.nRoot == None):
                debug = [0,0,0,0,0]
                self.nRoot = Node(state, last_move, debug=debug)
            self.nRoot.parent = None
        count=0
        while time()*1000-startTimeMS < max_time_to_move * 0.90:
            count+=1
            #print(f"count: {count}")
            nLeaf = self.nRoot.findSpotToExpand()
            #print(nLeaf)
            #print(f"nLeaf.Q: {nLeaf.Q}")
            val = nLeaf.rollout(self.black)
            nLeaf.backupValue(val)
        print(f"count: {count}")
        bestChild = self.nRoot.bestChild()
        print(f"best child's move: {bestChild.lastMove}")
        print(f"best child: {bestChild}")
        self.nRoot = bestChild
        self.nRoot.parent = None
        return bestChild.lastMove

    def id(self) -> str:
        """Please return a string here that uniquely identifies your submission e.g., "name (student_id)" """
        return "Rick's Mega Pog Ultra Gamer Agent (ggez)"
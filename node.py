from GmUtils import GmUtils
from gomoku import move as play, Move, GameState, check_win, pretty_board as printBoard, valid_moves as getValidMoves
import random
import numpy as np
import matplotlib.pyplot as plt
import math
from copy import deepcopy
random.seed(0)
c = 1 / math.sqrt(2)

class Node:
    # O(1)
    def __init__(self, state: GameState, lastMove: Move, parent=None):
        self.state = deepcopy(state)
        self.children = []
        self.parent = parent
        self.N = 0
        self.Q = 0
        self.lastMove = deepcopy(lastMove)
        self.movesToExplore = getValidMoves(self.state)

    def printNode(self):
        printBoard(self.state[0])
        print(f"nChildren: {len(self.children)}\nQ: {self.Q}\nN: {self.N}\nlastMove: {self.lastMove}\nnMovesToExplore: {len(self.movesToExplore)}")

    # O(?) check_win onbekend, maar zal vermoedelijk iets in de richting van O(n^2) zijn, omdat het bord n*n is als het goed is.
    def isTerminal(self):
        return check_win(self.state[0], self.lastMove)

    # O(n^2) in het geval dat we door blijven gaan tot een vol bord.
    def findSpotToExpand(self):
        if(self.isTerminal()):
            return self
        if(len(self.movesToExplore) > 0):
            moveIndex = random.randrange(0, len(self.movesToExplore))
            ok, win, state = play(deepcopy(self.state), self.movesToExplore[moveIndex])
            self.children.append(Node(state, self.movesToExplore[moveIndex], parent=self))
            self.movesToExplore = self.movesToExplore[:moveIndex] + self.movesToExplore[moveIndex+1:]
            return self.children[-1]
        return self.highestUCTChild().findSpotToExpand()

    # O(n), je gaat altijd één keer door de hele lijst van child nodes.
    def highestUCTChild(self):
        highest = (-float('inf'), None)
        for child in self.children:
            value = child.getUCT()
            if value > highest[0]:
                highest = (value, child)
        return highest[1]

    # O(1)
    def getUCT(self):
        return (self.Q / self.N) + (c * math.sqrt((2 * math.log2(self.parent.N)) / self.N))
        
    # O(n^2), als je begint vanaf een (bijna) helemaal leeg bord
    def rollout(self, black: bool):
        state = deepcopy(self.state)
        win = check_win(self.state[0], self.lastMove)
        moves = getValidMoves(state)
        while(not win):
            if(len(moves)==0):
                return 0
            move = random.choice(moves)
            moves.remove(move)
            ok, win, state = play(state, move)
        if(state[1]%2 != black):
            return 1
        else:
            return -1

    # O(n^2), als de value van één van de laatste moves helemaal naar boven ge-backupped moet worden
    def backupValue(self, val: float):
        self.N += 1
        self.Q += val
        if self.parent is not None:
            self.parent.backupValue(val)
    
    # O(n), je gaat altijd één keer door de lijst van child nodes
    def bestChild(self):
        best = (-float('inf'), None, 0)
        vals = []
        for child in self.children:
            val = child.Q / child.N
            vals.append(val)
            if((val > best[0])):
                best = (val, child)
        return best[1]
    
    # O(n), je gaat altijd één keer door de lijst van child nodes
    def childWithMove(self, move):
        for child in self.children:
            if(child.lastMove == move):
                return child
        return None
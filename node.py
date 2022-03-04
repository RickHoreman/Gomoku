from GmUtils import GmUtils
from gomoku import move as play, Move, GameState, check_win, pretty_board as printBoard, valid_moves as getValidMoves
import random
import numpy as np
from copy import deepcopy
random.seed(0)
c = 1 / np.sqrt(2)

class Node:
    def __init__(self, state: GameState, lastMove: Move, parent=None, debug=None):
        #print("Node!")
        self.state = deepcopy(state)
        self.children = []
        self.parent = parent
        self.N = 0
        self.Q = 0
        self.lastMove = deepcopy(lastMove)
        self.movesToExplore = getValidMoves(self.state)
        self.debug = debug

    def isTerminal(self):
        #print(self.lastMove)
        #print(self.movesToExplore)
        return check_win(self.state[0], self.lastMove)

    def findSpotToExpand(self):
        #print("findSpotToExpand")
        #printBoard(self.state[0])
        #moves = getValidMoves(self.state)
        if(self.isTerminal()):
            #print("isTerminal")
            self.debug[0] += 1
            return self
        #print(len(self.movesToExplore))
        #print(len(self.children))
        if(len(self.movesToExplore) > len(self.children)):
            #print("que")
            self.debug[1] += 1
            moveIndex = random.randrange(0, len(self.movesToExplore))
            ok, win, state = play(self.state, self.movesToExplore[moveIndex])
            if(not ok):
                print("This should absolutely never be possible 1 :/")
                printBoard(self.state[0])
                print("~~~")
                printBoard(state[0])
                print(self.movesToExplore[moveIndex])
                print(len(self.movesToExplore))
                exit(1)
            self.children.append(Node(state, self.movesToExplore[moveIndex], parent=self, debug=self.debug))
            #print(len(self.movesToExplore))
            #print(self.movesToExplore)
            self.movesToExplore = self.movesToExplore[:moveIndex] + self.movesToExplore[moveIndex+1:]
            #print(self.movesToExplore)
            #print(len(self.movesToExplore))
            return self.children[-1]
        if(len(self.movesToExplore) == 0):
            print("Leaf node!")
            self.debug[2] += 1
            return self
        return self.highestUCTChild().findSpotToExpand()

    def highestUCTChild(self):
        highest = (-1, None)
        for child in self.children:
            value = child.getUCT()
            if value > highest[0]:
                highest = (value, child)
        #print(f"highest: {highest[0]}")
        return highest[1]

    def getUCT(self):
        return (self.Q / self.N) + (c * np.sqrt((2 * np.log(self.parent.N)) / self.N))
        
    def rollout(self, black: bool):
        state = deepcopy(self.state)
        win = False
        while(not win):
            moves = getValidMoves(state)
            if(len(moves)==0):
                if(state[1]%2 == black):
                    return 0.5
                else:
                    return -0.5
            move = random.choice(moves)
            ok, win, state = play(state, move)
            if(not ok):
                print("This should absolutely never be possible 2 :/")
                printBoard(state[0])
                print(move)
                exit(1)
        if(state[1]%2 != black):
            return 1
        else:
            return -1

    def backupValue(self, val: float):
        self.N += 1
        self.Q += val
        if self.parent is not None:
            self.parent.backupValue(val)
    
    def bestChild(self):
        if(len(self.children) == 0):
            print("fuck")
            print(self.lastMove)
            print(self.N)
            print(self.Q)
            print(self.movesToExplore)
        best = (-1, None)
        #print("children's values:")
        for child in self.children:
            val = child.Q / child.N
            #print(val)
            if((val > best[0]) and len(child.children) > 0):
                best = (val, child)
            print(child.lastMove, end=', ')
        # print(f"best child's children: {best[1].children}")
        print(f"\n{self.debug[0]} terminal, {self.debug[1]} que, {self.debug[2]} leaf, {self.debug[3]} not yabe, {self.debug[4]} yabe")
        return best[1]
    
    def childWithMove(self, move):
        for child in self.children:
            if(child.lastMove == move):
                self.debug[3] += 1
                return child
        print(f"yabe: {move}")
        self.debug[4] += 1
        return None
"""
The Brandeis Quant Club ML/AI Competition (November 2023)

Author: @Ephraim Zimmerman
Email: quants@brandeis.edu
Website: brandeisquantclub.com; quants.devpost.com

Description:

For any technical issues or questions please feel free to reach out to
the "on-call" hackathon support member via email at quants@brandeis.edu

Website/GitHub Repository:
You can find the latest updates, documentation, and additional resources for this project on the
official website or GitHub repository: https://github.com/EphraimJZimmerman/chess_hackathon_23

License:
This code is open-source and released under the MIT License. See the LICENSE file for details.
"""

import numpy as np
import chess
import requests
import logging
import random
# DO NOT MODIFY



# First, get board state
# 

# Create empty node
# Simulate game
# change weights and n
# back prop

# select child by ucb

class Node:
    def __init__(self, parent=None, action=None, c = 2, w = 0, n = 0, fen = None):
        self.action = action
        self.w = w
        self.n = n
        self.c = c
        
        self.board = chess.Board(fen if fen else "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        self.color = self.board.turn
        self.legal_moves = list(self.board.legal_moves)

        self.parent = parent
        self.children = []
        self.max_children = self.board.legal_moves.count()
        # print(self.max_children)

    def addChild(self, action, fen):
        node = Node(parent=self, action=action, fen=fen)
        self.children.append(node)
        return node

    def simulate(self, color):
        board_copy = chess.Board(self.board.fen())
        # print(board_copy)

        #do random moves til game ends
        while board_copy.outcome() == None:
            move = random.choice(list(board_copy.legal_moves))
            board_copy.push(move)
            # print(board_copy)     
        # print(board_copy.outcome())

        result = (0, 0)

        if board_copy.outcome().winner == None:
            result = (1/2, 1)
        elif board_copy.outcome().winner == color:
            result = (1, 1)
        else:
            result = (0, 1)

        self.w = result[0]
        self.n = result[1]
        return result

    # if there are no children
    #   create new child node and use it for rest
    # if there is one child
    #   ubc goes through, there is only one choice, so use that choice
    # if there are 2 >= children
    #   loop through and ubc and choose highest

    #recursion returns iterations
    #or maybe not
    #root has no children so it returns itself
    #runs simulation
    def selectNextLeafNode(self):
        if len(self.children) < self.max_children:
            return self
        
        max_child = self.children[0]
        max = 0
        for child in self.children:
            child_w = getattr(child, "w")
            child_n = getattr(child, "n")
            ubc = (child_w / child_n) + (self.c * (np.log(self.n)/child_n)**0.5)
            print(child)
            print(ubc)
            print()
            if max < ubc:
                max = ubc
                max_child = child
            # print(getattr(child, "w"))
        
        return max_child.selectNextLeafNode()
    
    def backPropagateWN(self, w, n):
        if self.parent != None:
            self.parent.addWins(w)
            self.parent.addVisits(n)
            self.parent.backPropagateWN(w, n)

    def getNextLegalMove(self):
        #could make this random
        return self.legal_moves.pop(0)
    
    def getWins(self):
        return self.w
    
    def getVisits(self):
        return self.n

    def addWins(self, w):
        self.w += w

    def addVisits(self, n):
        self.n += n

    def printTreeFromNode(self):
        for child in self.children:
            print(str(child))

    def __str__(self):
        return "parent: " + str(getattr(self, "parent")) + " | move: " + str(getattr(self, "action"))

# Node has zero children
# Create one child
# OR Node chooses child
# Go to child node
# simulate thing
# back propogation
# return back to root node repeat above


# Node.s
def MCGameTree(board, iterations, color):
    print("start")
    #figure out board to fen
    root = Node(fen=board.fen())

    #for each iteration
    for i in range(iterations):
        #Selection
        leaf = root.selectNextLeafNode()

        #Expansion
        #Need to create a child storing an action and the board after the action in fen notation
        action = leaf.getNextLegalMove()
        leaf_board_copy = chess.Board(getattr(leaf, "board").fen())
        leaf_board_copy.push(action)

        leaf_child = leaf.addChild(action, leaf_board_copy.fen())
        # print(leaf_child)
        #Simulation
        results = leaf_child.simulate(color=color)

        #Backpropagation
        leaf_child.backPropagateWN(results[0], results[1])

    max_child = getattr(root, "children")[0]
    max = 0
    for child in getattr(root, "children"):
        child_w = child.getWins()
        child_n = child.getVisits()
        ubc = (child_w / child_n) + (getattr(root, "c") * (np.log(root.getVisits())/child_n)**0.5)
        if max < ubc:
            max = ubc
            max_child = child
        # print(getattr(child, "w"))
    
    return getattr(max_child, "action")

board = chess.Board("rnb5/8/1p1B2p1/2pQPk1p/p1P5/2N2NP1/PP3PP1/3R1RK1 w a - 0 1")
# print("print" + str(board.legal_moves.count()))
# move = MCGameTree(board, 500)
# board.push(move)
# print(board)

#do random moves til game ends
response = input("who starts first")
if response == "1":
    move = input("enter move: ")
    board.push_san(move)
print(board)
while board.outcome() == None:
    move = MCGameTree(board, 500, response!="1")
    board.push(move)
    print(board)
    move = input("enter move: ")
    # move = random.choice(list(board.legal_moves))
    board.push_san(move)
    print(board)

    # print(board_copy)     
# print(board_copy.outcome())

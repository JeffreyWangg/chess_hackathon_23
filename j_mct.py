import chess
import random
import numpy as np
import math
from eval import eval
class ChessGame:
    def __init__(self):
        self.board = chess.Board()

    def get_initial_state(self):
        return self.board

    def get_valid_moves(self, board):
        return list(board.legal_moves)

    def get_next_state(self, board, move):
        new_board = board.copy()
        new_board.push(move)
        return new_board

    def check_win(self, board):
        return board.is_checkmate()

    def get_value_and_terminated(self, board, player):
        if self.check_win(board):
            return 1 if board.turn == player else -1, True
        if board.is_game_over():
            return 0, True
        return 0, False

    def change_perspective(self, board, player):
        # In chess, the perspective change is handled by the board.turn attribute
        return board


class Node:
    def __init__(self, game, state, parent=None, action_taken=None, player=chess.WHITE):
        self.game = game
        self.state = state
        self.parent = parent
        self.action_taken = action_taken
        self.player = player

        self.children = []
        self.expandable_moves = game.get_valid_moves(state)

        self.visit_count = 0
        self.value_sum = 0

    def is_fully_expanded(self):
        return len(self.expandable_moves) == 0 and len(self.children) > 0

    def select(self):
        best_child = None
        best_ucb = -np.inf

        for child in self.children:
            ucb = self.get_ucb(child)
            if ucb > best_ucb:
                best_child = child
                best_ucb = ucb

        return best_child

    def get_ucb(self, child):
        q_value = (child.value_sum / child.visit_count)
        e_val = (eval(child.state.fen())  + 100)/100
        return q_value + 1.4 * math.sqrt(math.log(self.visit_count) / child.visit_count) + 5*e_val

    def expand(self):
        move = self.expandable_moves.pop()
        new_state = self.game.get_next_state(self.state, move)
        child = Node(self.game, new_state, self, move, not self.player)
        self.children.append(child)
        return child

    def simulate(self):
        # A more sophisticated simulation approach can be implemented here
        current_state = self.state.copy()
        while not current_state.is_game_over():
            move = random.choice(list(current_state.legal_moves))
            current_state.push(move)
        value, _ = self.game.get_value_and_terminated(current_state, self.player)
        return value

    def backpropagate(self, value):
        self.value_sum += value
        self.visit_count += 1
        if self.parent is not None:
            self.parent.backpropagate(-value)  # Flip the value for the opponent


class MCTS:
    def __init__(self, game, args):
        self.game = game
        self.args = args

    def search(self, state, player):
        root = Node(self.game, state, player=player)

        for _ in range(self.args['num_searches']):
            node = root

            while node.is_fully_expanded():
                node = node.select()

            if not node.state.is_game_over():
                node = node.expand()
                value = node.simulate()

            node.backpropagate(value)

        action_probs = np.zeros(len(root.children))
        for i, child in enumerate(root.children):
            action_probs[i] = child.visit_count
        action_probs /= np.sum(action_probs)

        return action_probs
    


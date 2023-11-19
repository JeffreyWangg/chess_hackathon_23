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

import random
import chess
import time
import numpy as np
from collections.abc import Iterator
from contextlib import contextmanager
from j_mct import MCTS, ChessGame


@contextmanager
def game_manager():
    """Creates context for game."""

    print("===== GAME STARTED =====")
    ping: float = time.perf_counter()
    try:
        # DO NOT EDIT. This will be replaced w/ judging context manager.
        yield
    finally:
        pong: float = time.perf_counter()
        total = pong - ping
        print(f"Total game time = {total:.3f} seconds")
    print("===== GAME ENDED =====")

# Add promotion stuff

if __name__ == "__main__":
    with game_manager():

        """
        
        Feel free to make any adjustments as you see fit. The desired outcome 
        is to generate the next best move, regardless of whether the bot 
        is controlling the white or black pieces. The code snippet below 
        serves as a useful testing framework from which you can begin 
        developing your strategy.

        """

        # Initialize the game and MCTS parameters
        chess_game = ChessGame()
        args = {
            'C': 1.41,          # Exploration parameter
            'num_searches': 1000  # Number of searches (iterations) for MCTS
        }
        mcts = MCTS(chess_game, args)

        side = input("Enter 1 for White or 0 for Black")
        side = chess.BLACK if side == 0 else chess.WHITE

        # Main game loop
        while not chess_game.board.is_game_over():
            print('\n')
            print(chess_game.board)
            if chess_game.board.turn == side:
                # MCTS player (White)
                neutral_state = chess_game.change_perspective(chess_game.board, side)
                mcts_probs = mcts.search(neutral_state, side)
                action = chess_game.get_valid_moves(neutral_state)[np.argmax(mcts_probs)]
            else:
                # Random player (Black)
                valid_moves = list(chess_game.board.legal_moves)
                action = random.choice(valid_moves)

            chess_game.board.push(action)

        # Print the final board and the game result
        print(chess_game.board)
        print("Game result:", chess_game.board.result())

     
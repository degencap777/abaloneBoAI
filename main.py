#!/usr/bin/env python3

import game
import random

def initGame():
    """Set the game to its inital state and print the board.
    """

    game.fillBoard()
    game.printBoard()

    if random.random() < 0.5:
        game.togglePlayer()

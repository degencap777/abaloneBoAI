#!/usr/bin/env python3

# Copyright (c) 2018 Scriptim
# This code is licensed under the MIT License, see LICENSE.md


import abalone
import random
import sys

game = sys.modules['__main__'].game


def turn(board, opponent_move):
    """Perform a random move.
    :param board: the current state of the board
    :type board: dict
    :param opponent_move: the opponent's last move
    :type opponent_move: tuple(list[str], int) | None
    :return: the move to be performed
    :rtype: tuple(list[str], int)
    """

    straight_lines = []
    for space in abalone.spaces:
        if board[space] == 1:
            straight_lines.append([space])
            for direction in [1, 2, 6]:
                neighbor1 = abalone.neighbor(space, direction)
                if neighbor1 in abalone.spaces and board[neighbor1] == 1:
                    straight_lines.append([space, neighbor1])
                    neighbor2 = abalone.neighbor(neighbor1, direction)
                    if neighbor2 in abalone.spaces and board[neighbor2] == 1:
                        straight_lines.append([space, neighbor1, neighbor2])

    moves = []
    for line in straight_lines:
        for direction in range(1, 7):
            off_board = False
            for marble in line:
                if abalone.neighbor(marble, direction) == 0:
                    off_board = True
                    break
            if off_board:
                continue
            try:
                game.copy().move(line, direction)
                moves.append((line, direction))
            except Exception:
                pass

    return random.choice(moves)

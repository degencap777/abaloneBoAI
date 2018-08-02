#!/usr/bin/env python3

# Copyright (c) 2018 Scriptim
# This code is licensed under the MIT License, see LICENSE.md


import game
import random


def turn(board, opponent_move):
    """Perform a random move.

    :param board: the current state of the board
    :type board: dict
    :param opponent_move: the opponent's last move
    :type opponent_move: tuple(list[str], int) | None
    :return: the move to be performed
    :rtype: tuple(list[str], int)
    """

    spaces = [
        'A1', 'A2', 'A3', 'A4', 'A5',
        'B1', 'B2', 'B3', 'B4', 'B5', 'B6',
        'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7',
        'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8',
        'E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9',
        'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9',
        'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9',
        'H4', 'H5', 'H6', 'H7', 'H8', 'H9',
        'I5', 'I6', 'I7', 'I8', 'I9'
    ]

    straight_lines = []
    for space in spaces:
        if board[space] == 1:
            straight_lines.append([space])
            for direction in [1, 2, 6]:
                neighbor1 = game.neighbor(space, direction)
                if neighbor1 in spaces and board[neighbor1] == 1:
                    straight_lines.append([space, neighbor1])
                    neighbor2 = game.neighbor(neighbor1, direction)
                    if neighbor2 in spaces and board[neighbor2] == 1:
                        straight_lines.append([space, neighbor1, neighbor2])

    moves = []
    for line in straight_lines:
        for direction in range(1, 7):
            off_board = False
            for marble in line:
                if game.neighbor(marble, direction) == 0:
                    off_board = True
                    break
            if off_board:
                continue
            try:
                board_copy = {}
                for space in game.global_board:
                    board_copy[space] = game.global_board[space]
                game.move(line, direction, board_copy)
                moves.append((line, direction))
            except Exception:
                pass

    return random.choice(moves)

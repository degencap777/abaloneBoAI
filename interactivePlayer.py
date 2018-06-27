#!/usr/bin/env python3

# Copyright (c) 2018 Scriptim
# This code is licensed under the MIT License, see LICENSE.md


def turn(board, opponentMove):
    """Receive input from the user to make a move.

    :param board: the current state of the board
    :type board: dict
    :param opponentMove: the opponent's last move
    :type opponentMove: tuple(list[str], int) | None
    :return: the move to be performed
    :rtype: tuple(list[str], int)
    """

    while True:
        try:
            marbles = input('marbles (space separated): ')
            marbles = [marble for marble in marbles.split(' ') if marble != '']
            direction = input('direction [1-9]: ')
            direction = int(direction)
            return (marbles, direction)
        except KeyboardInterrupt as e:
            raise e
        except Exception as e:
            print('Input exception: ' + str(e))

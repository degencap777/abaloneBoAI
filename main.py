#!/usr/bin/env python3

# Copyright (c) 2018 Scriptim
# This code is licensed under the MIT License, see LICENSE.md

import argparse
import game
import importlib
import os
import random
import sys
import traceback


def parseArgs():
    """Parse the command line arguments.

    :return: parsed arguments
    :rtype: dict
    """

    parser = argparse.ArgumentParser(description='Abalone Battle of AIs',
                                     epilog='Documentation: https://scriptim' +
                                     '.github.io/Abalone-BoAI')
    parser.add_argument('--version', action='version', version='1.0.0rc')
    parser.add_argument('-1', dest='player1', default='interactivePlayer',
                        help='python module for player 1 (black)')
    parser.add_argument('-2', dest='player2', default='interactivePlayer',
                        help='python module for player 2 (white)')
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true',
                        help='verbose output')
    parser.add_argument('-r', '--random', dest='random', action='store_true',
                        help='start with random player')

    sys.argv = vars(parser.parse_args())


def initGame():
    """Set the game to its initial state and print the board.
    """

    game.fillBoard()
    game.printBoard()

    if sys.argv['random'] and random.random() < 0.5:
        game.togglePlayer()


def runGame(player1, player2):
    """The main game loop.

    :param player1: an AI that plays as player 1 (black)
    :type player1: module
    :param player2: an AI that plays as player 2 (white)
    :type player2: module
    """

    lastMove = None

    while True:
        print()

        if game.score['p1'] == 0:
            print('Player 2 won the game!')
            sys.exit(0)
        if game.score['p2'] == 0:
            print('Player 1 won the game!')
            sys.exit(0)

        print('Player ' + str(game.currentPlayer) + ' is next')
        print('Score: ' + str(game.score['p1']) + ' : ' +
              str(game.score['p2']))
        game.printBoard()

        # A modified board is given to the player, in which 1 stands for the
        # player and -1 for the opponent.
        playerBoard = {}
        for space in game.board:
            player = game.board[space]
            if player == 0:
                playerBoard[space] = 0
            else:
                playerBoard[space] = 1 if player == game.currentPlayer else -1

        try:
            if game.currentPlayer == 1:
                lastMove = player1.turn(playerBoard, lastMove)
            else:
                lastMove = player2.turn(playerBoard, lastMove)

            print('Moving \'' + ', '.join(lastMove[0]) + '\' in direction ' +
                  str(lastMove[1]))

            for marble in lastMove[0]:
                if game.isOpponent(marble):
                    raise game.IllegalMoveException(
                        'Moving opponent\'s marble')
                if game.neighbor(marble, lastMove[1]) == 0:
                    raise game.IllegalMoveException(
                        'Moving marble off the board')

            game.move(lastMove[0], lastMove[1])
            game.togglePlayer()

        except game.IllegalMoveException as e:
            print('Player ' + str(game.currentPlayer) +
                  ' made an illegal move')
            print(e)
            print('Player ' + str(2 if game.currentPlayer == 1 else 1) +
                  ' won the game!')
            sys.exit(1)

        except Exception:
            print('Player ' + str(game.currentPlayer) +
                  '\'s move caused an exception')
            if sys.argv['verbose']:
                traceback.print_exc()
            print('Player ' + str(2 if game.currentPlayer == 1 else 1) +
                  ' won the game!')
            sys.exit(1)


if __name__ == "__main__":
    parseArgs()

    # Add ./ais directory to path for importing ai modules
    directory = os.path.abspath(os.path.dirname(__file__))
    sys.path.append(os.path.join(directory, 'ais'))

    player1 = importlib.import_module(sys.argv['player1'])
    player2 = importlib.import_module(sys.argv['player2'])

    initGame()

    try:
        runGame(player1, player2)
    except KeyboardInterrupt:
        if sys.argv['verbose']:
            print('Interrupted')
        sys.exit(137)

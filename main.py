#!/usr/bin/env python3

# Copyright (c) 2018 Scriptim
# This code is licensed under the MIT License, see LICENSE.md

import game
import random
import sys
import traceback


def initGame():
    """Set the game to its inital state and print the board.
    """

    game.fillBoard()
    game.printBoard()

    if random.random() < 0.5:
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
            traceback.print_exc()
            print('Player ' + str(2 if game.currentPlayer == 1 else 1) +
                  ' won the game!')
            sys.exit(1)


if __name__ == "__main__":
    initGame()

    player1 = None
    player2 = None

    if player1 == None:
        player1 = game.interactivePlayer
    if player2 == None:
        player2 = game.interactivePlayer

    try:
        runGame(player1, player2)
    except KeyboardInterrupt:
        sys.exit(137)

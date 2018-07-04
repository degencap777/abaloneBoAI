#!/usr/bin/env python3

# Copyright (c) 2018 Scriptim
# This code is licensed under the MIT License, see LICENSE.md

import argparse
import game
import importlib
import json
import os
import random
import sys
import traceback
import urllib.parse


def parseArgs():
    """Parse the command line arguments.

    :return: parsed arguments
    :rtype: dict
    """

    parser = argparse.ArgumentParser(description='Abalone Battle of AIs',
                                     epilog='Documentation: https://scriptim' +
                                     '.github.io/Abalone-BoAI')
    parser.add_argument('--version', action='version', version='1.2.0rc')
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

    courseOfTheGame = {
        'boardHistory': [],
        'moveHistory': [],
        'scoreHistory': [],
        'startPlayer': None,
        'winner': None,
        'exitReason': None
    }

    courseOfTheGame['startPlayer'] = game.currentPlayer

    lastMove = None

    while True:
        print()

        courseOfTheGame['scoreHistory'].append((game.score['p1'],
                                                game.score['p2']))
        courseOfTheGame['boardHistory'].append(game.board.copy())

        if game.score['p1'] == 0 or game.score['p2'] == 0:
            if game.score['p1'] == 0:
                winner = 2
            if game.score['p2'] == 0:
                winner = 1
            print(f'Player {winner} won the game!')
            courseOfTheGame['winner'] = winner
            saveCourseOfTheGameToFile(courseOfTheGame)
            sys.exit(0)

        print(f'Player {game.currentPlayer} is next')
        print(f'Score: {game.score["p1"]} : {game.score["p2"]}')

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

            courseOfTheGame['moveHistory'].append(lastMove)

            print(f'Moving \'{", ".join(lastMove[0])}\' in direction '
                  f'{lastMove[1]}')

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
            exitReason = f'Player {game.currentPlayer} made an illegal move'
            print(e)
            courseOfTheGame['exitReason'] = exitReason
            winner = 2 if game.currentPlayer == 1 else 1
            print(f'Player {winner} won the game!')
            courseOfTheGame['winner'] = winner
            saveCourseOfTheGameToFile(courseOfTheGame)
            sys.exit(1)

        except Exception:
            exitReason = (f'Player {game.currentPlayer}\'s move caused an '
                          'exception')
            print(exitReason)
            courseOfTheGame['exitReason'] = exitReason
            if sys.argv['verbose']:
                traceback.print_exc()
            winner = 2 if game.currentPlayer == 1 else 1
            print(f'Player {winner} won the game!')
            courseOfTheGame['winner'] = winner
            saveCourseOfTheGameToFile(courseOfTheGame)
            sys.exit(1)

    saveCourseOfTheGameToFile(courseOfTheGame)


def saveCourseOfTheGameToFile(courseOfTheGame):
    """Save the course of the game to a JSON file (``course_of_the_game.json``)
    in the project directory.

    :param courseOfTheGame: The course of the game to be saved

    keys:

    - ``boardHistory``: a list containing all states of the board during the
      game in chronological order
    - ``moveHistory``: a list of all moves, i. e. the return values of the
      players' ``turn`` functions, during the game in chronological order
    - ``scoreHistory``: a list of tuples of two integer values representing the
      players' scores during the game in chronological order
    - ``startPlayer``: the player (``1`` or ``2``) that started the game
    - ``winner``: The player (``1`` or ``2``) that won the game
    - ``exitReason``: the error message if an error has occurred

    :type courseOfTheGame: dict
    """

    player1 = 'interactivePlayer'
    player2 = 'interactivePlayer'
    if 'player1' in sys.argv:
        player1 = sys.argv['player1'].split(".")[0]
    if 'player2' in sys.argv:
        player2 = sys.argv['player2'].split(".")[0]

    filename = f'{player1} -- {player2}.js'
    directory = os.path.abspath(os.path.dirname(__file__))
    filepath = os.path.join(directory, 'results', filename)

    with open(filepath, 'w', encoding='utf-8') as file:
        file.write('const courseOfTheGame = ')
        file.write(json.dumps(courseOfTheGame))
        file.write('\nupdate.all()')
        filename = urllib.parse.quote(filename)
        htmlFile = os.path.join(directory, 'html', 'index.html')
        htmlFile = urllib.parse.quote(htmlFile)
        print(f'\nOpen file://{htmlFile}?game={filename} in a web browser')


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

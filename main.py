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


def parse_args():
    """Parse the command line arguments.

    :return: parsed arguments
    :rtype: dict
    """

    parser = argparse.ArgumentParser(description='Abalone Battle of AIs',
                                     epilog='Documentation: https://scriptim' +
                                     '.github.io/Abalone-BoAI')
    parser.add_argument('--version', action='version', version='1.2.0rc')
    parser.add_argument('-1', dest='p1', default='interactive_player.main',
                        help='python module for player 1 (black)')
    parser.add_argument('-2', dest='p2', default='interactive_player.main',
                        help='python module for player 2 (white)')
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true',
                        help='verbose output')
    parser.add_argument('-r', '--random', dest='random', action='store_true',
                        help='start with random player')

    sys.argv = vars(parser.parse_args())


def init_game():
    """Set the game to its initial state and print the board.
    """

    game.fill_board()
    game.print_board()

    if sys.argv['random'] and random.random() < 0.5:
        game.toggle_player()


def run_game(p1, p2):
    """The main game loop.

    :param p1: an AI that plays as player 1 (black)
    :type p1: module
    :param p2: an AI that plays as player 2 (white)
    :type p2: module
    """

    course_of_the_game = {
        'boardHistory': [],
        'moveHistory': [],
        'scoreHistory': [],
        'startPlayer': None,
        'winner': None,
        'exitReason': None
    }

    course_of_the_game['startPlayer'] = game.current_player

    last_move = None

    while True:
        print()

        course_of_the_game['scoreHistory'].append((game.score['p1'],
                                                    game.score['p2']))
        course_of_the_game['boardHistory'].append(game.global_board.copy())

        if game.score['p1'] == 0 or game.score['p2'] == 0:
            if game.score['p1'] == 0:
                winner = 2
            if game.score['p2'] == 0:
                winner = 1
            print(f'Player {winner} won the game!')
            course_of_the_game['winner'] = winner
            save_course_of_the_game_to_file(course_of_the_game)
            sys.exit(0)

        print(f'Player {game.current_player} is next')
        print(f'Score: {game.score["p1"]} : {game.score["p2"]}')

        game.print_board()

        # A modified board is given to the player, in which 1 stands for the
        # player and -1 for the opponent.
        player_board = {}
        for space in game.global_board:
            player = game.global_board[space]
            if player == 0:
                player_board[space] = 0
            else:
                player_board[space] = (1 if player == game.current_player else
                                       -1)

        try:
            if game.current_player == 1:
                last_move = p1.turn(player_board, last_move)
            else:
                last_move = p2.turn(player_board, last_move)

            course_of_the_game['moveHistory'].append(last_move)

            print(f'Moving \'{", ".join(last_move[0])}\' in direction '
                  f'{last_move[1]}')

            for marble in last_move[0]:
                if game.is_opponent(marble):
                    raise game.IllegalMoveException(
                        'Moving opponent\'s marble')
                if game.neighbor(marble, last_move[1]) == 0:
                    raise game.IllegalMoveException(
                        'Moving marble off the board')

            game.move(last_move[0], last_move[1])
            game.toggle_player()

        except game.IllegalMoveException as e:
            exit_reason = f'Player {game.current_player} made an illegal move'
            print(e)
            course_of_the_game['exitReason'] = exit_reason
            winner = 2 if game.current_player == 1 else 1
            print(f'Player {winner} won the game!')
            course_of_the_game['winner'] = winner
            save_course_of_the_game_to_file(course_of_the_game)
            sys.exit(1)

        except Exception:
            exit_reason = (f'Player {game.current_player}\'s move caused an '
                           'exception')
            print(exit_reason)
            course_of_the_game['exitReason'] = exit_reason
            if sys.argv['verbose']:
                traceback.print_exc()
            winner = 2 if game.current_player == 1 else 1
            print(f'Player {winner} won the game!')
            course_of_the_game['winner'] = winner
            save_course_of_the_game_to_file(course_of_the_game)
            sys.exit(1)

    save_course_of_the_game_to_file(course_of_the_game)


def save_course_of_the_game_to_file(course_of_the_game):
    """Save the course of the game to a JSON file in the results directory.

    :param course_of_the_game: The course of the game to be saved

    keys:

    - ``boardHistory``: a list containing all states of the board during the
      game in chronological order
    - ``moveHistory``: a list of all moves, i. e. the return values of the
      players' ``turn`` functions, during the game in chronological order
    - ``scoreHistory``: a list of tuples of two integer values representing
      the players' scores during the game in chronological order
    - ``startPlayer``: the player (``1`` or ``2``) that started the game
    - ``winner``: The player (``1`` or ``2``) that won the game
    - ``exitReason``: the error message if an error has occurred

    :type course_of_the_game: dict
    """

    p1 = sys.argv['p1'].split(".")[0]
    p2 = sys.argv['p2'].split(".")[0]

    filename = f'{p1} -- {p2}.js'
    directory = os.path.abspath(os.path.dirname(__file__))
    filepath = os.path.join(directory, 'results', filename)

    with open(filepath, 'w', encoding='utf-8') as file:
        file.write('const courseOfTheGame = ')
        file.write(json.dumps(course_of_the_game))
        file.write('\nupdate.all()')
        filename = urllib.parse.quote(filename)
        html_file = os.path.join(directory, 'html', 'index.html')
        html_file = urllib.parse.quote(html_file)
        print(f'\nOpen file://{html_file}?game={filename} in a web browser')


if __name__ == "__main__":
    parse_args()

    p1 = importlib.import_module(f'ais.{sys.argv["p1"]}')
    p2 = importlib.import_module(f'ais.{sys.argv["p2"]}')

    init_game()

    try:
        run_game(p1, p2)
    except KeyboardInterrupt:
        if sys.argv['verbose']:
            print('Interrupted')
        sys.exit(137)

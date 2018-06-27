#!/usr/bin/env python3

# black (X) = 1, white (O) = 2
# Note that the AI is passed a modified board with its own marbles represented
# by 1 and the opponent's marbles by -1.
currentPlayer = 1

# Maps a space of the board to the player (1/2) to own it or 0 if the space is
# empty. See the documentation for information on how the spaces are denoted.
board = {}

# The score of a player decrements whenever a marble is pushed off the board by
# the opponent.
score = {'p1': 6, 'p2': 6}

rows = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
diagonals = ['1', '2', '3', '4', '5', '6', '7', '8', '9']


def fillBoard():
    """Fill the ``board`` dict with the `default initial position
    <https://en.wikipedia.org/wiki/File:Abalone_standard.svg>`_.
    """

    global board
    global rows
    global diagonals

    for row in rows:
        rowIndex = rows.index(row)

        diagonalsForRow = (diagonals[0:5 + rowIndex] if rowIndex <= 4 else
                           diagonals[rowIndex - 4:])

        for diagonal in diagonalsForRow:
            board[row + diagonal] = 0  # empty
            if (row in ['A', 'B'] or
                    (row == 'C' and diagonal in ['3', '4', '5'])):
                board[row + diagonal] = 1  # black
            elif (row in ['H', 'I'] or
                  (row == 'G' and diagonal in ['5', '6', '7'])):
                board[row + diagonal] = 2  # white


def isCurrentPlayer(space):
    """Check if a space is owned by the current player.

    :param space: the space to be checked
    :type space: str
    :return: whether the space is owned by the current player
    :rtype: bool
    """

    global currentPlayer
    global board

    if space == 0:
        return False
    return board[parseSpace(space)] == currentPlayer


def isEmpty(space):
    """Check if a space is empty.

    :param space: the space to be checked
    :type space: str
    :return: whether the space is empty
    :rtype: bool
    """

    global board

    if space == 0:
        return False
    return board[parseSpace(space)] == 0


def isOpponent(space):
    """Check if a space is owned by the opponent player.

    :param space: the space to be checked
    :type space: str
    :return: whether the space is owned by the opponent player
    :rtype: bool
    """

    global currentPlayer
    global board

    if space == 0:
        return False
    return (board[parseSpace(space)] == 2 if currentPlayer == 1 else
            board[parseSpace(space)] == 1)


def parseSpace(space):
    """Convert any space valid notation to the standard notation.

    A valid string that denotes a space consists of a row letter (from ``A`` to
    ``I``) and a diagonal number (from ``1`` to ``9``). The notation is
    case-insensitive and does not require a specific order.

    The standard notation starts with a capital row letter followed by a
    diagonal number. It is used for the keys in the ``board`` dict, among
    other things.

    :param space: a space in any valid notation
    :type space: str
    :raises TypeError: Invalid type (str expected)
    :raises Error: Invalid string length (2 expected)
    :raises Error: Invalid string notation
    :return: the standard notation for the given space
    :rtype: str
    """

    global rows
    global diagonals

    if (space == 0):
        return 0  # off the board

    if not isinstance(space, str):
        raise TypeError('Invalid type \'' + type(space).__name__ +
                        '\' (str expected)')
    if len(space) != 2:
        raise Error('Invalid string length ' + str(len(space)) +
                    ' (2 expected)')

    space = space.upper()

    if space[0] in rows and space[1] in diagonals:
        return space
    elif space[0] in diagonals and space[1] in rows:
        return space[::-1]

    raise Error('Invalid string notation ' + space)


def printBoard():
    """Print the board to stdout.

    Player 1 (black) is represented by ``X``, player 2 (white) by ``O``, empty
    spaces by ``·``, e. g.

    ::

            I O O O O O
           H O O O O O O
          G · · O O O · ·
         F · · · · · · · ·
        E · · · · · · · · ·
         D · · · · · · · · 9
          C · · X X X · · 8
           B X X X X X X 7
            A X X X X X 6
               1 2 3 4 5
    """

    global board

    # black = X, white = O, empty = ·
    loggableBoard = {}
    for space in board:
        loggableBoard[space] = ('X' if board[space] == 1 else
                                ('O' if board[space] == 2 else '·'))

    boardStr = ''
    boardStr += '    I ' + ' '.join([str(loggableBoard['I' + str(d)])
                                     for d in range(5, 10)]) + '\n'
    boardStr += '   H ' + ' '.join([str(loggableBoard['H' + str(d)])
                                    for d in range(4, 10)]) + '\n'
    boardStr += '  G ' + ' '.join([str(loggableBoard['G' + str(d)])
                                   for d in range(3, 10)]) + '\n'
    boardStr += ' F ' + ' '.join([str(loggableBoard['F' + str(d)])
                                  for d in range(2, 10)]) + '\n'
    boardStr += 'E ' + ' '.join([str(loggableBoard['E' + str(d)])
                                 for d in range(1, 10)]) + '\n'
    boardStr += ' D ' + ' '.join([str(loggableBoard['D' + str(d)])
                                  for d in range(1, 9)]) + ' 9\n'
    boardStr += '  C ' + ' '.join([str(loggableBoard['C' + str(d)])
                                   for d in range(1, 8)]) + ' 8\n'
    boardStr += '   B ' + ' '.join([str(loggableBoard['B' + str(d)])
                                    for d in range(1, 7)]) + ' 7\n'
    boardStr += '    A ' + ' '.join([str(loggableBoard['A' + str(d)])
                                     for d in range(1, 6)]) + ' 6\n'
    boardStr += '       1 2 3 4 5'

    print(boardStr)


def togglePlayer():
    """Switch ``currentPlayer`` between ``1`` and ``2``.
    """

    global currentPlayer

    currentPlayer = 2 if currentPlayer == 1 else 1

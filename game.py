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


class IllegalMoveException(Exception):
    """Custom Exception to be raised whenever a player performs an illegal
    move.
    """

    pass


def areStraightLine(spaces):
    """Check if the given spaces form a straight line.

    This is a required for a valid move.

    :param spaces: a list of spaces
    :type spaces: list[str]
    :return: whether the spaces form a straight line
    :rtype: bool
    """

    global rows
    global diagonals

    spaces = [parseSpace(space) for space in spaces]

    if len(spaces) <= 1:
        return True

    # Check for duplicates.
    if len(set(spaces)) != len(spaces):
        return False

    same = sameRowAndDiagonal(spaces)
    if not same['row'] and not same['diagonal'] and not same['diagonalR']:
        return False

    # The lexicographical sorting ensures that successive spaces in the list
    # are closest to each other on the board.
    spaces.sort()
    for space in range(1, len(spaces)):
        prevRow = spaces[space - 1][0]
        row = spaces[space][0]
        deltaRow = abs(rows.index(prevRow) - rows.index(row))

        prevDiagonal = spaces[space - 1][1]
        diagonal = spaces[space][1]
        deltaDiagonal = (abs(diagonals.index(prevDiagonal) -
                             diagonals.index(diagonal)))

        # The distance (delta) to the previous space is exactly 1 if they are
        # adjacent.
        if (same['row'] and deltaDiagonal != 1 or
            same['diagonal'] and deltaRow != 1 or
                same['diagonalR'] and (deltaDiagonal != 1 or deltaRow != 1)):
            return False

    return True


def broadside(marbles, direction):
    """Perform a broadside move.

    .. warning:: This function should not be called directly, as it does not
                 perform input validation, which could lead to unpredictable
                 behavior. It is only intended as a help function for
                 :func:`move`.

    :param marbles: the marbles to be moved
    :type marbles: list[str]
    :param direction: the direction of movement

    .. seealso:: :func:`move` for information on the direction parameter

    :type direction: int
    """

    for marble in marbles:
        move([marble], direction)


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


def fromHeadToTail(spaces, direction):
    """Sort a straight line of spaces by a certain direction so that the head
    comes first.

    :param spaces: a straight line of spaces
    :type spaces: list[str]
    :param direction: the direction in which the spaces are oriented

    .. seealso:: :func:`move` for information on the direction parameter

    :type direction: int
    :raises Exception: Marbles are not in a straight line
    :raises Exception: Moving *marbles* in direction is not an in-line move
    :return: a sorted list of spaces
    :rtype: list[str]
    """

    if not areStraightLine(spaces):
        raise Exception('Marbles ' + ', '.join(spaces) +
                        ' are not in a straight line')
    same = sameRowAndDiagonal(spaces)
    if (same['row'] and direction in [1, 3, 4, 6] or
        same['diagonal'] and direction in [1, 2, 4, 5] or
            same['diagonalR'] and direction in [2, 3, 5, 6]):
        raise Exception('Moving ' + ', '.join(spaces) + ' in direction ' +
                        str(direction) + ' is not an in-line move')
    spaces.sort()
    if direction in [1, 2, 6]:
        spaces.reverse()
    return spaces


def inLine(marbles, direction):
    """Perform an in-line move, sumito if applicable.

    .. warning:: This function should not be called directly, as it does not
                 perform input validation, which could lead to unpredictable
                 behavior. It is only intended as a help function for
                 :func:`move`.

    :param marbles: the marbles to be moved
    :type marbles: list[str]
    :param direction: the direction of movement

    .. seealso:: :func:`move` for information on the direction parameter

    :type direction: int
    :raises IllegalMoveException: *space* is not empty

    if the destination space is already occupied

    :raises IllegalMoveException: Moving *n* marbles with *m* own marble(s)

    if the move cannot be made due to too few marbles
    """

    head = fromHeadToTail(marbles, direction)[0]

    # destination: opponent -> sumito
    opponentMarbles = []
    if isOpponent(neighbor(head, direction)):
        opponentHead = neighbor(head, direction)
        opponentMarbles = [opponentHead]
        while True:
            nextMarble = neighbor(opponentHead, direction)
            if isOpponent(nextMarble):
                opponentHead = nextMarble
                opponentMarbles.append(nextMarble)
            elif isCurrentPlayer(nextMarble):
                # The space after the opponent's line of marbles is already
                # owned by the player, hence not empty.
                raise IllegalMoveException(nextMarble + ' is not empty')
            else:
                break

        # Valid sumito moves are 2 -> 1, 3 -> 1, 3 -> 2
        if len(opponentMarbles) >= len(marbles):
            raise IllegalMoveException('Moving ' + str(len(opponentMarbles)) +
                                       ' marbles with ' + str(len(marbles)) +
                                       'own marble(s)')

    # The list starts with the marble closest to the current player's marbles
    # which must be moved last.
    opponentMarbles.reverse()
    for opponentMarble in opponentMarbles:
        move([opponentMarble], direction)

    # destination: current player
    if isCurrentPlayer(neighbor(head, direction)):
        raise IllegalMoveException(neighbor(head, direction) + ' is not empty')

    # destination: empty
    for marble in fromHeadToTail(marbles, direction):
        move([marble], direction)


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


def move(marbles, direction):
    """Perform a move in a specific direction.

    :param marbles: the marbles to be moved
    :type marbles: list[str]
    :param direction: the direction of movement

    ::

         6 1
        5 · 2
         4 3

    1. northeast
    2. east
    3. southeast
    4. southwest
    5. west
    6. northwest

    :type direction: int
    :raises IllegalMoveException: Moving *n* marbles

    if the number of marbles is not between ``1`` and ``3`` (inclusive)

    :raises IllegalMoveException: Marbles are not in a straight line
    :raises IllegalMoveException: *space* is not empty
    """

    global currentPlayer
    global board

    marbles = [parseSpace(marble) for marble in marbles]

    if len(marbles) < 1 or len(marbles) > 3:
        raise IllegalMoveException('Moving ' + str(len(marbles)) + ' marbles')
    if not areStraightLine(marbles):
        raise IllegalMoveException('Marbles ' + ', '.join(marbles) +
                                   ' are not in a straight line')

    # single
    if len(marbles) == 1:
        destination = neighbor(marbles[0], direction)
        if destination == 0:
            pass  # player moves opponent's marble off the board
        elif not isEmpty(destination):
            raise IllegalMoveException(str(destination) + ' is not empty')
        else:
            board[destination] = board[marbles[0]]
        board[marbles[0]] = 0
        return

    same = sameRowAndDiagonal(marbles)
    if (same['row'] and direction in [1, 3, 4, 6] or
        same['diagonal'] and direction in [1, 2, 4, 5] or
            same['diagonalR'] and direction in [2, 3, 5, 6]):
        broadside(marbles, direction)
    else:
        inLine(marbles, direction)


def neighbor(space, direction):
    """Get the adjacent space in a certain direction.

    :param space: the space from which the neighbour is determined
    :type space: str
    :param direction: the direction

    .. seealso:: :func:`move` for information on the direction parameter

    :type direction: int
    :raises Exception: Invalid direction

    if the direction is not between ``1`` and ``6`` (inclusive)

    :return: the neighbor space in standard notation | ``0`` if there is no
             neighbor in the given direction

    :rtype: str | int
    """

    global rows
    global diagonals

    space = parseSpace(space)

    row = rows.index(space[0])
    diagonal = diagonals.index(space[1])

    if direction == 1:
        row = row + 1
        diagonal = diagonal + 1
    elif direction == 2:
        diagonal = diagonal + 1
    elif direction == 3:
        row = row - 1
    elif direction == 4:
        row = row - 1
        diagonal = diagonal - 1
    elif direction == 5:
        diagonal = diagonal - 1
    elif direction == 6:
        row = row + 1
    else:
        raise Exception('Invalid direction ' + str(direction))

    if (row < 0 or row >= len(rows) or diagonal < 0 or
            diagonal >= len(diagonals)):
        return 0  # off the board

    return rows[row] + diagonals[diagonal]


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


def sameRowAndDiagonal(spaces):
    """Indicate if the given spaces are in the same row and/or diagonal.

    :param spaces: a list of spaces
    :type spaces: list[str]
    :return: a dict with three keys ``row``, ``diagonal`` and ``diagonalR``

    - ``row`` is ``True`` if the spaces are in the same row (``A`` to ``I``).
    - ``diagonal`` is ``True`` if the spaces are in the same diagonal (``1`` to
      ``9``). This includes only the diagonals from northwest to southeast.
    - ``diagonalR`` is ``True`` if the spaces are in the same diagonal. This
      includes only the diagonals from northeast to southwest.

    :rtype: dict[str, bool]
    """

    global rows
    global diagonals

    spaces = [parseSpace(space) for space in spaces]
    sameRow = True
    sameDiagonal = True
    sameDiagonalR = True
    for space in range(1, len(spaces)):
        deltaRow = (abs(rows.index(spaces[0][0]) -
                        rows.index(spaces[space][0])))
        deltaDiagonal = (abs(diagonals.index(spaces[0][1]) -
                             diagonals.index(spaces[space][1])))

        if deltaRow != 0:
            sameRow = False

        if deltaDiagonal != 0:
            sameDiagonal = False

        if deltaRow != deltaDiagonal:
            sameDiagonalR = False

    return {
        'row': sameRow,
        'diagonal': sameDiagonal,
        'diagonalR': sameDiagonalR
    }


def togglePlayer():
    """Switch ``currentPlayer`` between ``1`` and ``2``.
    """

    global currentPlayer

    currentPlayer = 2 if currentPlayer == 1 else 1

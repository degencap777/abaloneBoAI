#!/usr/bin/env python3

# Copyright (c) 2018 Scriptim
# This code is licensed under the MIT License, see LICENSE.md


# black (X) = 1, white (O) = 2
# Note that the AI is passed a modified board with its own marbles represented
# by 1 and the opponent's marbles by -1.
current_player = 1

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


def are_straight_line(spaces):
    """Check if the given spaces form a straight line.

    This is a required for a valid move.

    :param spaces: a list of spaces
    :type spaces: list[str]
    :return: whether the spaces form a straight line
    :rtype: bool
    """

    global rows
    global diagonals

    spaces = [parse_space(space) for space in spaces]

    if len(spaces) <= 1:
        return True

    # Check for duplicates.
    if len(set(spaces)) != len(spaces):
        return False

    same = same_row_and_diagonal(spaces)
    if not same['row'] and not same['diagonal'] and not same['diagonal_r']:
        return False

    # The lexicographical sorting ensures that successive spaces in the list
    # are closest to each other on the board.
    spaces.sort()
    for space in range(1, len(spaces)):
        prev_row = spaces[space - 1][0]
        row = spaces[space][0]
        delta_row = abs(rows.index(prev_row) - rows.index(row))

        prev_diagonal = spaces[space - 1][1]
        diagonal = spaces[space][1]
        delta_diagonal = (abs(diagonals.index(prev_diagonal) -
                              diagonals.index(diagonal)))

        # The distance (delta) to the previous space is exactly 1 if they are
        # adjacent.
        if (same['row'] and delta_diagonal != 1 or
            same['diagonal'] and delta_row != 1 or
                same['diagonal_r'] and (delta_diagonal != 1 or
                                        delta_row != 1)):
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


def fill_board():
    """Fill the ``board`` dict with the `default initial position
    <https://en.wikipedia.org/wiki/File:Abalone_standard.svg>`_.
    """

    global board
    global rows
    global diagonals

    for row in rows:
        row_index = rows.index(row)

        diagonals_for_row = (diagonals[0:5 + row_index] if row_index <= 4 else
                             diagonals[row_index - 4:])

        for diagonal in diagonals_for_row:
            board[row + diagonal] = 0  # empty
            if (row in ['A', 'B'] or
                    (row == 'C' and diagonal in ['3', '4', '5'])):
                board[row + diagonal] = 1  # black
            elif (row in ['H', 'I'] or
                  (row == 'G' and diagonal in ['5', '6', '7'])):
                board[row + diagonal] = 2  # white


def from_head_to_tail(spaces, direction):
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

    if not are_straight_line(spaces):
        raise Exception(f'Marbles {", ".join(spaces)} '
                        'are not in a straight line')
    same = same_row_and_diagonal(spaces)
    if (same['row'] and direction in [1, 3, 4, 6] or
        same['diagonal'] and direction in [1, 2, 4, 5] or
            same['diagonal_r'] and direction in [2, 3, 5, 6]):
        raise Exception(f'Moving {", ".join(spaces)} in direction {direction} '
                        'is not an in-line move')
    spaces.sort()
    if direction in [1, 2, 6]:
        spaces.reverse()
    return spaces


def in_line(marbles, direction):
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

    head = from_head_to_tail(marbles, direction)[0]

    # destination: opponent -> sumito
    opponent_marbles = []
    if is_opponent(neighbor(head, direction)):
        opponent_head = neighbor(head, direction)
        opponent_marbles = [opponent_head]
        while True:
            next_marble = neighbor(opponent_head, direction)
            if is_opponent(next_marble):
                opponent_head = next_marble
                opponent_marbles.append(next_marble)
            elif is_current_player(next_marble):
                # The space after the opponent's line of marbles is already
                # owned by the player, hence not empty.
                raise IllegalMoveException(f'{next_marble} is not empty')
            else:
                break

        # Valid sumito moves are 2 -> 1, 3 -> 1, 3 -> 2
        if len(opponent_marbles) >= len(marbles):
            raise IllegalMoveException(f'Moving {len(opponent_marbles)} '
                                       f'marbles with {len(marbles)} '
                                       'own marble(s)')

    # The list starts with the marble closest to the current player's marbles
    # which must be moved last.
    opponent_marbles.reverse()
    for opponent_marble in opponent_marbles:
        move([opponent_marble], direction)

    # destination: current player
    if is_current_player(neighbor(head, direction)):
        raise IllegalMoveException(f'{neighbor(head, direction)} is not empty')

    # destination: empty
    for marble in from_head_to_tail(marbles, direction):
        move([marble], direction)


def is_current_player(space):
    """Check if a space is owned by the current player.

    :param space: the space to be checked
    :type space: str
    :return: whether the space is owned by the current player
    :rtype: bool
    """

    global current_player
    global board

    if space == 0:
        return False
    return board[parse_space(space)] == current_player


def is_empty(space):
    """Check if a space is empty.

    :param space: the space to be checked
    :type space: str
    :return: whether the space is empty
    :rtype: bool
    """

    global board

    if space == 0:
        return False
    return board[parse_space(space)] == 0


def is_opponent(space):
    """Check if a space is owned by the opponent player.

    :param space: the space to be checked
    :type space: str
    :return: whether the space is owned by the opponent player
    :rtype: bool
    """

    global current_player
    global board

    if space == 0:
        return False
    return (board[parse_space(space)] == 2 if current_player == 1 else
            board[parse_space(space)] == 1)


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

    global current_player
    global board

    marbles = [parse_space(marble) for marble in marbles]

    if len(marbles) < 1 or len(marbles) > 3:
        raise IllegalMoveException(f'Moving {len(marbles)} marbles')
    if not are_straight_line(marbles):
        raise IllegalMoveException(
            f'Marbles {", ".join(marbles)} are not in a straight line')

    # single
    if len(marbles) == 1:
        destination = neighbor(marbles[0], direction)
        if destination == 0:
            on_off_board(board[marbles[0]])
        elif not is_empty(destination):
            raise IllegalMoveException(f'{destination} is not empty')
        else:
            board[destination] = board[marbles[0]]
        board[marbles[0]] = 0
        return

    same = same_row_and_diagonal(marbles)
    if (same['row'] and direction in [1, 3, 4, 6] or
        same['diagonal'] and direction in [1, 2, 4, 5] or
            same['diagonal_r'] and direction in [2, 3, 5, 6]):
        broadside(marbles, direction)
    else:
        in_line(marbles, direction)


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

    space = parse_space(space)

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
        raise Exception(f'Invalid direction {direction}')

    if (row < 0 or row >= len(rows) or
        diagonal < 0 or diagonal >= len(diagonals) or
            not f'{rows[row]}{diagonals[diagonal]}' in board):
        return 0  # off the board

    return rows[row] + diagonals[diagonal]


def on_off_board(player):
    """Reduce the score of a player whose marble has been pushed off the board.

    :param player: the player (``1`` or ``2``) that
    :type player: int
    """

    global board
    global score

    index = f'p{player}'
    score[index] = score[index] - 1


def parse_space(space):
    """Convert any valid space notation to the standard notation.

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
        raise TypeError(f'Invalid type \'{type(space).__name__}\' '
                        '(str expected)')
    if len(space) != 2:
        raise Error(f'Invalid string length {len(space)} (2 expected)')

    space = space.upper()

    if space[0] in rows and space[1] in diagonals:
        return space
    elif space[0] in diagonals and space[1] in rows:
        return space[::-1]

    raise Error(f'Invalid string notation {space}')


def print_board():
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
    log_board = {}
    for space in board:
        log_board[space] = ('X' if board[space] == 1 else
                            ('O' if board[space] == 2 else '·'))

    row_str = {}
    row_str['A'] = " ".join([str(log_board[f"A{d}"]) for d in range(1, 6)])
    row_str['B'] = " ".join([str(log_board[f"B{d}"]) for d in range(1, 7)])
    row_str['C'] = " ".join([str(log_board[f"C{d}"]) for d in range(1, 8)])
    row_str['D'] = " ".join([str(log_board[f"D{d}"]) for d in range(1, 9)])
    row_str['E'] = " ".join([str(log_board[f"E{d}"]) for d in range(1, 10)])
    row_str['F'] = " ".join([str(log_board[f"F{d}"]) for d in range(2, 10)])
    row_str['G'] = " ".join([str(log_board[f"G{d}"]) for d in range(3, 10)])
    row_str['H'] = " ".join([str(log_board[f"H{d}"]) for d in range(4, 10)])
    row_str['I'] = " ".join([str(log_board[f"I{d}"]) for d in range(5, 10)])

    board_str = (f'    I {row_str["I"]}\n'
                 f'   H {row_str["H"]}\n'
                 f'  G {row_str["G"]}\n'
                 f' F {row_str["F"]}\n'
                 f'E {row_str["E"]}\n'
                 f' D {row_str["D"]} 9\n'
                 f'  C {row_str["C"]} 8\n'
                 f'   B {row_str["B"]} 7\n'
                 f'    A {row_str["A"]} 6\n'
                 f'       1 2 3 4 5')

    print(board_str)


def same_row_and_diagonal(spaces):
    """Indicate if the given spaces are in the same row and/or diagonal.

    :param spaces: a list of spaces
    :type spaces: list[str]
    :return: a dict with three keys ``row``, ``diagonal`` and ``diagonal_r``

    - ``row`` is ``True`` if the spaces are in the same row (``A`` to ``I``).
    - ``diagonal`` is ``True`` if the spaces are in the same diagonal (``1`` to
      ``9``). This includes only the diagonals from northwest to southeast.
    - ``diagonal_r`` is ``True`` if the spaces are in the same diagonal. This
      includes only the diagonals from northeast to southwest.

    :rtype: dict[str, bool]
    """

    global rows
    global diagonals

    spaces = [parse_space(space) for space in spaces]
    same_row = True
    same_diagonal = True
    same_diagonal_r = True
    for space in range(1, len(spaces)):
        delta_row = (abs(rows.index(spaces[0][0]) -
                         rows.index(spaces[space][0])))
        delta_diagonal = (abs(diagonals.index(spaces[0][1]) -
                              diagonals.index(spaces[space][1])))

        if delta_row != 0:
            same_row = False

        if delta_diagonal != 0:
            same_diagonal = False

        if delta_row != delta_diagonal:
            same_diagonal_r = False

    return {
        'row': same_row,
        'diagonal': same_diagonal,
        'diagonal_r': same_diagonal_r
    }


def toggle_player():
    """Switch ``current_player`` between ``1`` and ``2``.
    """

    global current_player

    current_player = 2 if current_player == 1 else 1

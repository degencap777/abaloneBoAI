How to create your own
======================

To create your own ai follow these steps:

1. Fork the `GitHub repository <https://github.com/Scriptim/Abalone-BoAI>`_ and
   clone it.
2. Create a new branch and check it out.
3. Create a new subdirectory in the ``ais`` directory with the name of your AI.
4. Create a Python file (``.py``) in that directory that implements
   ``turn(board, opponent_move)``.

   ::

       def turn(board, opponent_move):
          """My AI.

          :param board: the current state of the board
          :type board: dict
          :param opponent_move: the opponent's last move
          :type opponent_move: tuple(list[str], int) | None
          :return: the move to be performed
          :rtype: tuple(list[str], int)
          """

          pass  # TODO: implement

5. Create a ``requirements.txt`` file in which you specify the required Python
   modules.
6. Push your changes.
7. Create a pull request.

----

Assuming your subdirectory is called ``my-ai`` and the main file in it is
called ``ai.py``, then you can load this module using the CLI as follows:

::

    python3 main.py -1 my-ai.ai


``turn(board, opponent_move)``
------------------------------

This function shall return a tuple with a list and an integer value.

The first value is a list of the marbles to be moved. A marble is represented
by a string denoting the space it rests in.

Each space on the board is denoted by a string that consist of a row letter
(from A to I) and a diagonal number (from 1 to 9). The notation is
case-insensitive and does not require a specific order.

::

      I · · · · ·
     H · · · · · ·
    G · · · · · · ·
   F · · · · · · · ·
  E · · · · · · · · ·
   D · · · · · · · · 9
    C · · · · · · · 8
     B · · · · · · 7
      A · · · · · 6
         1 2 3 4 5

The second value in the tuple is an integer between ``1`` and ``6`` (inclusive)
that represents the direction of movement.

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

The ``board`` parameter contains a dict that represents the current state of
the board. It maps strings denoting the spaces in standard notation to
integers where ``0`` stands for empty spaces, ``1`` for the player's own
spaces and ``-1`` for the opponent's spaces.

The standard notation, which is used for the keys in the board dict, starts
with a capital row letter followed by a diagonal number.

The ``opponent_move`` parameter contains the opponent's most recent move, i. e.
the returned value of the opponent's ``turn`` function.

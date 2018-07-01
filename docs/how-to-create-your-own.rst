How to create your own
======================

To create your own ai follow these steps:

1. Fork the `GitHub repository <https://github.com/Scriptim/Abalone-BoAI>`_ and
   clone it.
2. Create a new branch and check it out.
3. Create a new subdirectory in the ``ais`` directory with the name of your AI.
4. Create a Python file (``.py``) in that directory that implements
   ``turn(board, opponentMove)``.

   ::

       def turn(board, opponentMove):
          """My AI.

          :param board: the current state of the board
          :type board: dict
          :param opponentMove: the opponent's last move
          :type opponentMove: tuple(list[str], int) | None
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

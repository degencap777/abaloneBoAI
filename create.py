#!/usr/bin/env python3

# Copyright (c) 2018 Scriptim
# This code is licensed under the MIT License, see LICENSE.md

import git
import os
import re
import sys

if __name__ == '__main__':
    directory = os.path.dirname(os.path.realpath(__file__))

    repo = git.Repo(directory)

    if repo.bare:
        print("Could not load git repository.")
        sys.exit(1)

    origin = repo.remotes.origin
    if origin.exists():
        original_urls = [
            'git@github.com:Scriptim/Abalone-BoAI',
            'git@github.com:Scriptim/Abalone-BoAI.git',
            'https://github.com/Scriptim/Abalone-BoAI',
            'https://github.com/Scriptim/Abalone-BoAI.git'
        ]
        origin_urls = list(origin.urls)

        if len(set(original_urls).intersection(origin_urls)) > 0:
            print('Fork the GitHub repository and clone it:')
            print('https://github.com/Scriptim/Abalone-BoAI')
            print('Then rerun this script there.')
            sys.exit(1)

    if repo.is_dirty():
        print('Your repository is dirty.')
        sys.exit(1)

    if (not 'master' in repo.branches):
        print('Missing branch "master".')

    author = None
    try:
        author = repo.config_reader().get_value('user', 'name')
    except:
        print('Could not get author information.')
        print('Set user.name with git config.')
        sys.exit(1)

    name = input('Give your AI a name: ')
    if re.compile('^[A-Za-z0-9\-]+$').match(name) == None:
        print('Invalid input.')
        print('The name may only contain letters, numbers and hyphens.')
        sys.exit(1)

    if name in repo.branches:
        print('A branch with that name already exists.')
        sys.exit(1)

    ai_directory = os.path.join(directory, 'ais', name)
    if os.path.exists(ai_directory):
        print(f'ais/{name} already exists.')
        sys.exit(1)

    repo.git.checkout('master', b=name)

    os.makedirs(ai_directory)

    with open(os.path.join(ai_directory, 'README.md'), 'w') as file:
        file.write('# ')
        file.write(name)
        file.write(' by ')
        file.write(author)
        file.write('\n\n')
        file.write('(description)\n')

    repo.git.add(ai_directory)
    repo.index.commit(f'Create ai "{name}"')

    with open(os.path.join(ai_directory, 'main.py'), 'w') as file:
        file.write('def turn(board, opponent_move):\n')
        file.write('    """')
        file.write(name)
        file.write('\n\n')
        file.write('    :param board: the current state of the board\n')
        file.write('    :type board: dict\n')
        file.write('    :param opponent_move: the opponent\'s last move\n')
        file.write('    :type opponent_move: tuple(list[str], int) | None\n')
        file.write('    :return: the move to be performed\n')
        file.write('    :rtype: tuple(list[str], int)\n')
        file.write('    """\n')
        file.write('\n')
        file.write('    pass  # TODO: implement\n')

    repo.git.add(ai_directory)
    repo.index.commit(f'Add "main.py"')

    with open(os.path.join(ai_directory, 'requirements.txt'), 'w') as file:
        file.write('\n')

    repo.git.add(ai_directory)
    repo.index.commit(f'Add "requirements.txt"')

    print(f'Your ai was created in "ais/{name}"')
    print('All you have to do now is implement the "turn" function in the '
          '"main.py" file inside your ai directory.')
    print('See https://scriptim.github.io/Abalone-BoAI/how-to-create-your-own.'
          'html#turn-board-opponent-move for more information.')
    print('If you are using third party Python libraries, they are specified '
          'in "requirements.txt"')
    print('Creating a "LICENSE.md" file is recommended.')
    print('Commit all your changes and push them if you like.')

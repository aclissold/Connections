#!/usr/bin/env python3
#
# A simple command-line Connect Four clone.
#
# To-do:
#   Colorize winning pieces on Windows
#   Refactor:
#       Add comments/docstrings
#       Split up has_four_in_a_row()
#       Make classe(s)
#   Create online version

import os, sys
from random import randint

# Initialize board to empty cells
board = [[[] for index in range(7)] for index in range(7)]
winning_rows = []
winning_columns = []
turn = randint(1, 2)
last_row = 0
last_column = 0

# Set each board cell to a space
def reset_board():
    """Initialize (or reset) the board to a clean slate.
    
    Clear all board cells (i.e., set all indices of the board variable to a
    single space character), and pop any indices off of winning_rows and
    winning_columns.
    """
    for i in range(7):
        for j in range(7):
            board[i][j] = ' '
    for i in range(len(winning_rows)):
        winning_rows.pop()
        winning_columns.pop()

# Display the current board state to the user,
# in a pretty format.
def draw_board():
    """Display the board on the screen.

    Use a nested for-loops to iterated through the elements of board
    and display them properly in a grid resembling a Connect Four game.

    """
    print('   _____________')
    for i in reversed(range(7)):
        print('  |', end='')
        for j in range(6):
            print(str(board[i][j]), end=' ')
        print(str(board[i][6] + '|'))
    print(' /===============\\')
    print('   1 2 3 4 5 6 7')
    print()

def prompt_column(is_full=False):
    """Ask the player what column to drop a piece in and return it.

    Also, exit if the player types "q".

    """
    if is_full:
        message = 'Column is full, please choose another: '
    else:
        message = 'Choose a column (or type q to quit): '
    column = -1
    while column < 0 or column > 6:
        inputted_string = input(message)
        modified_input = str(inputted_string).lower().split()
        if modified_input:
            if modified_input[0] == 'q' or modified_input[0] == 'quit':
                sys.exit(0)
        try:
            column = int(inputted_string) - 1
        except ValueError:
            pass
        if column < 0 or column > 6:
            print('Please enter a number from 1 - 7 or \"q\".')
    return column

def drop_piece(column):
    """Drop a game piece in the given column."""
    global last_row, last_column
    for row in range(7):
        if board[row][column] == ' ':
            if turn == 1:
                board[row][column] = 'x'
                last_row, last_column = row, column
                break
            else:
                board[row][column] = 'o'
                last_row, last_column = row, column
                break
    else:
        # Column is full
        new_column = prompt_column(is_full=True)
        drop_piece(new_column)

def change_turn():
    """Turn 1 becomes 2 and vice versa; clear the screen; display turn info."""
    global turn
    if turn == 1:
        turn = 2
    else:
        turn = 1
    if sys.platform == 'win32':
        os.system('cls')
    else:
        os.system('clear')
    print()
    print(' ~Player {0}\'s Turn~'.format(turn))

def top_row_full():
    """Determine if the top row is full.

    If it IS full, display a "Draw" message and return True. Else return False.

    """
    pieces_in_row = 0
    for i in range(7):
        if board[6][i] == ' ':
            break
        else:
            pieces_in_row += 1
    if pieces_in_row == 7:
        print('IT\'S A DRAW?!? Nobody wins! Sad day.')
        return True
    else:
        return False

def has_four_in_a_row():
    """Check if the previously dropped piece led to four+ in a row.

    Return True if that was the case; False otherwise.

    """
    dropped_piece = board[last_row][last_column]
    has_four_in_a_row = False
    winning_rows.append(last_row)
    winning_columns.append(last_column)
    in_a_row = 1
    # Check if there's four-in-a-row horizontally
    for i in range(1, 7):
        # Right to left
        if last_column - i >= 0:
            if board[last_row][last_column - i] == dropped_piece:
                in_a_row += 1
                winning_rows.append(last_row)
                winning_columns.append(last_column - i)
            else:
                break
        else:
            break
    for i in range(1, 7):
        # Left to right
        if last_column + i <= 6:
            if board[last_row][last_column + i] == dropped_piece:
                in_a_row += 1
                winning_rows.append(last_row)
                winning_columns.append(last_column + i)
            else:
                break
        else:
            break
    if in_a_row >= 4:
        has_four_in_a_row = True
    else:
        if in_a_row > 1:
            for i in range(in_a_row - 1):
                winning_rows.pop()
                winning_columns.pop()
    in_a_row = 1
    # Check if there's four-in-a-row vertically
    for i in range(1, 5):
        # Bottom to top
        if last_row + i <= 6:
            if board[last_row + i][last_column] == dropped_piece:
                in_a_row += 1
                winning_rows.append(last_row + i)
                winning_columns.append(last_column)
            else:
                break
        else:
            break
    for i in range(1, 5):
        # Top to bottom
        if last_row - i >= 0:
            if board[last_row - i][last_column] == dropped_piece:
                in_a_row += 1
                winning_rows.append(last_row - i)
                winning_columns.append(last_column)
            else:
                break
        else:
            break
    if in_a_row >= 4:
        has_four_in_a_row = True
    else:
        if in_a_row > 1:
            for i in range(in_a_row - 1):
                winning_rows.pop()
                winning_columns.pop()
    in_a_row = 1
    # Check if there's four-in-a-row diagonally (/)
    for i in range(1, 7):
        # Lower-left to upper-right
        if last_row + i <= 6 and last_column + i <= 6:
            if board[last_row + i][last_column + i] == dropped_piece:
                in_a_row += 1
                winning_rows.append(last_row + i)
                winning_columns.append(last_column + i)
            else:
                break
        else:
            break
    for i in range(1, 7):
        # Upper-right to lower-left
        if last_row - i >= 0 and last_column - i >= 0:
            if board[last_row - i][last_column - i] == dropped_piece:
                in_a_row += 1
                winning_rows.append(last_row - i)
                winning_columns.append(last_column - i)
            else:
                break
        else:
            break
    if in_a_row >= 4:
        has_four_in_a_row = True
    else:
        if in_a_row > 1:
            for i in range(in_a_row - 1):
                winning_rows.pop()
                winning_columns.pop()
    in_a_row = 1
    # Check if there's four-in-a-row diagonally (\)
    for i in range(1, 7):
        if last_row - i >= 0 and last_column + i <= 6:
            if board[last_row - i][last_column + i] == dropped_piece:
                in_a_row += 1
                winning_rows.append(last_row - i)
                winning_columns.append(last_column + i)
            else:
                break
        else:
            break
    for i in range(1, 7):
        if last_row + i <= 6 and last_column - i >= 0:
            if board[last_row + i][last_column - i] == dropped_piece:
                in_a_row += 1
                winning_rows.append(last_row + i)
                winning_columns.append(last_column - i)
            else:
                break
        else:
            break
    if in_a_row >= 4:
        has_four_in_a_row = True
    else:
        if in_a_row > 1:
            for i in range(in_a_row - 1):
                winning_rows.pop()
                winning_columns.pop()
    if not has_four_in_a_row:
        # Also remove initial piece
        winning_rows.pop()
        winning_columns.pop()
    return has_four_in_a_row

def win():
    if sys.platform == 'win32':
        os.system('cls')
    else:
        os.system('clear')
    # Change colors of the winning pieces
    piece = 'x' if turn == 2 else 'o'
    if not sys.platform == 'win32':
    	piece = '\033[38;5;118m' + piece + '\033[0m'
    for i in range(len(winning_rows)):
        board[winning_rows[i]][winning_columns[i]] = piece
    print()
    print(' ~DING DING DING!~'.format(turn))
    draw_board()
    winner = 2 if turn == 1 else 2
    print('Four in a row!!! Player {0} wins!!! ' \
          'Party time.'.format(winner))
    print()

def again():
    """Ask the player if they want to play again and respond accordingly."""
    while True:
        choice = str(input('Play again? (Y/n): ').lower().split())
        if len(choice) == 2:
            play()
        else:
            if choice[2] == 'y':
                play()
            elif choice[2] == 'n':
                print('Thanks for playing!')
                print()
                sys.exit(0)
            else:
                print('Please type a \"y\" (or hit enter) for yes, ' \
                      'or an \"n\" for no.')

# Calls the other functions
def play():
    """Call all the functions that make up this program."""
    reset_board()
    change_turn()
    draw_board()
    has_four = False
    full = False
    while(not has_four and not full):
        column = prompt_column()
        drop_piece(column)
        change_turn()
        full = top_row_full()
        has_four = has_four_in_a_row()
        if has_four:
            win()
        else:
            draw_board()
    again()

if __name__ == '__main__':
    req_version = (3,0)
    cur_version = sys.version_info

    if cur_version >= req_version:
        play()
    else:
        print('Connections requires Python 3 to run.')

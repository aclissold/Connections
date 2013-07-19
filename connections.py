#!/usr/bin/env python3
#
# A simple command-line Connect Four clone.
#
# To-do:
#   Change board to by 7 x 6
#   Colorize winning pieces on Windows
#   Refactor:
#       Add comments/docstrings
#       Split up has_four_in_a_row()
#       Make classe(s)
#   Create online version

import os
import sys
from random import randint

# Initialize board to 7 x 7 empty cells
board = [[[] for index in range(7)] for index in range(7)]
# Holds the player's turn info (initialized randomly)
turn = randint(1, 2)
# Lists to hold indices of in-a-row pieces
winning_rows = []
winning_columns = []
# Holds the indices of the last-dropped piece
last_row = 0
last_column = 0

# Set each board cell to a space
def reset_board():
    """Reset (or initialize) the board to a clean slate."""
    
    # Clear all board cells by setting each index to a single space character
    for i in range(7):
        for j in range(7):
            board[i][j] = ' '
    # Pop any winning indices off of winning_rows and winning_columns
    for i in range(len(winning_rows)):
        winning_rows.pop()
        winning_columns.pop()

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

    Also, exit if the player types "q". True should be passed to this
    function if prompt_column was called previously and found to be
    a full column by drop_piece(). This causes a different prompt
    message to be displayed.

    """
    if is_full:
        message = 'Column is full, please choose another: '
    else:
        message = 'Choose a column (or type q to quit): '
    # Initialize column to an invalid number
    column = -1
    # "while column is invalid"
    while column < 0 or column > 6:
        inputted_string = input(message)
        modified_input = str(inputted_string).lower().split()
        if modified_input:
            if modified_input[0] == 'q' or modified_input[0] == 'quit':
                print('Thanks for playing!')
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
    # Iterate through the board from bottom to top
    for row in range(7):
        # Skip nonempty cells
        if board[row][column] == ' ':
            if turn == 1:
                # Drop piece
                board[row][column] = 'x'
                # Store these indices for later
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
    """Set turn 1 to 2 or vice versa; clear the screen; display turn info."""
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
    # Count the pieces in the top row
    for column in range(7):
        if board[6][column] == ' ':
            break
        else:
            pieces_in_row += 1
    if pieces_in_row == 7:
        if sys.platform == 'win32':
            os.system('cls')
        else:
            os.system('clear')
        print()
        print(' IT\'S A DRAW?!? Nobody wins! Sad day.')
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
    """Clear the screen; make winning pieces green; print winning message."""
    # Clear the screen
    if sys.platform == 'win32':
        os.system('cls')
    else:
        os.system('clear')
    # Change colors of the winning pieces (only on Mac/Linux)
    piece = 'x' if turn == 2 else 'o'
    if not sys.platform == 'win32':
    	piece = '\033[38;5;118m' + piece + '\033[0m'
    for i in range(len(winning_rows)):
        board[winning_rows[i]][winning_columns[i]] = piece
    # Draw the board with a unique winning message above and below
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
        # Accept no input (which results in '') as a default action
        if len(choice) == 2:
            play()
        else:
            # Accept any word starting with "y"
            if choice[2] == 'y':
                play()
            # Accept any word starting with "n"
            elif choice[2] == 'n':
                print('Thanks for playing!')
                print()
                sys.exit(0)
            else:
                print('Please type a "y" (or hit enter) for yes, ' \
                      'or an "n" for no.')

# Calls the other functions
def play():
    """Call all the functions that make up this program."""
    reset_board()
    change_turn()
    draw_board()
    # while-loop conditional initialization
    has_four = False
    full = False
    while(not has_four and not full):
        # Ask the player for a column and save it
        column = prompt_column()
        drop_piece(column)
        # Check if the top row is full and save the boolean result
        full = top_row_full()
        if not full:
            change_turn()
        # Check if the last piece resulted in four+ in a row and save the
        # boolean result
        has_four = has_four_in_a_row()
        if has_four:
            win() # DING DING DING!
        else:
            draw_board()
    # Ask if the player wants to play again
    again()

if __name__ == '__main__':
    # print('whatever') looks silly on Python 2.
    req_version = (3,0)
    cur_version = sys.version_info

    if cur_version >= req_version:
        play() # Start the game!!!
    else:
        print('Connections requires Python 3 to run.')
        # (implicit exit)

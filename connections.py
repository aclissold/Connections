#!/usr/bin/env python3
#
# Required methods:
#
# play()
# reset_board()
# draw_board()
# prompt_column()
# drop_piece()
# has_four_in_a_row()
# change_turn()
# again()
#
# To-do:
#   Allow winning diagonally
#   Restart when the board is filled
#   Don't show turn info on win
#
# Sample:
#
# ~Player 1's Turn~
#   _____________
#  |             |
#  |        x o  |
#  |    x   o x  |
#  |o   o x o o  |
#  |x x o x x x o|
#  |o o x o x x o|
# /===============\
#   1 2 3 4 5 6 7
#
# Choose a column: 4
import os, sys
from random import randint

# Initialize board to empty cells
board = [[[] for index in range(7)] for index in range(7)]
turn = randint(1, 2)
last_row = 0
last_column = 0

# Set each board cell to a space
def reset_board():
    for i in range(7):
        for j in range(7):
            board[i][j] = ' '

# Display the current board state to the user,
# in a pretty format.
def draw_board():
    os.system('clear')
    print()
    print(' ~Player {0}\'s Turn~'.format(turn))
    print('   _____________')
    print('  |' + str(board[6][0]), board[6][1], board[6][2], board[6][3], board[6][4], board[6][5], str(board[6][6]) + '|')
    print('  |' + str(board[5][0]), board[5][1], board[5][2], board[5][3], board[5][4], board[5][5], str(board[5][6]) + '|')
    print('  |' + str(board[4][0]), board[4][1], board[4][2], board[4][3], board[4][4], board[4][5], str(board[4][6]) + '|')
    print('  |' + str(board[3][0]), board[3][1], board[3][2], board[3][3], board[3][4], board[3][5], str(board[3][6]) + '|')
    print('  |' + str(board[2][0]), board[2][1], board[2][2], board[2][3], board[2][4], board[2][5], str(board[2][6]) + '|')
    print('  |' + str(board[1][0]), board[1][1], board[1][2], board[1][3], board[1][4], board[1][5], str(board[1][6]) + '|')
    print('  |' + str(board[0][0]), board[0][1], board[0][2], board[0][3], board[0][4], board[0][5], str(board[0][6]) + '|')
    print(' /===============\\')
    print('   1 2 3 4 5 6 7')
    print()

def prompt_column(is_full=False):
    if is_full:
        message = "Column is full, please choose another: "
    else:
        message = "Choose a column: "
    column = -1
    while column < 0 or column > 6:
        try:
            column = int(input(message)) - 1
        except ValueError:
            pass
        if column < 0 or column > 6:
            print("Please enter a number from 1 - 7 (inclusive).")
    return column

def drop_piece(column):
    global last_row, last_column
    for row in range(7):
        if board[row][column] == ' ':
            if turn == 1:
                board[row][column] = 'x'
                last_row, last_column = row, column
                break
            elif turn == 2:
                board[row][column] = 'o'
                last_row, last_column = row, column
                break
            else:
                raise Exception("You somehow managed to make it neither X " \
                                "nor O's turn.")
        elif board[row][column] == 'x' or board[row][column] == 'o':
            # Check the next row up
            pass
        else:
            raise Exception("Attempted to set a nonempty row/column combination")
    else:
        # Column is full
        new_column = prompt_column(is_full=True)
        drop_piece(new_column)

def change_turn():
    global turn
    if turn == 1:
        turn = 2
    else:
        turn = 1

def has_four_in_a_row():
    dropped_piece = board[last_row][last_column]
    has_four_in_a_row = False
    if dropped_piece == 'x' or dropped_piece == 'o':
        # Check if there's four-in-a-row horizontally
        in_a_row = 1
        for i in range(1, 5):
            if last_column - i >= 0:
                if board[last_row][last_column - i] == dropped_piece:
                    in_a_row += 1
                else:
                    break
            else:
                break
        for i in range(1, 5):
            if last_column + i <= 6:
                if board[last_row][last_column + i] == dropped_piece:
                    in_a_row += 1
                else:
                    break
            else:
                break
        if in_a_row == 4:
            print("Four in a row!!! Player {0} wins!!! " \
                  "Party time.".format(turn))
            print()
            has_four_in_a_row = True
        # Check if there's four-in-a-row vertically
        in_a_row = 1
        for i in range(1, 5):
            if last_row + i <= 6:
                if board[last_row + i][last_column] == dropped_piece:
                    in_a_row += 1
                else:
                    break
            else:
                break
        for i in range(1, 5):
            if last_row - i >= 0:
                if board[last_row - i][last_column] == dropped_piece:
                    in_a_row += 1
                else:
                    break
            else:
                break
        if in_a_row == 4:
            winner = 2 if turn == 1 else 2
            print("Four in a row!!! Player {0} wins!!! " \
                  "Party time.".format(winner))
            print()
            has_four_in_a_row = True
        # Check if there's four-in-a-row diagonally (/)
        in_a_row = 1
        for i in range(1, 5):
            if last_row + i <= 6 and last_column + i <= 6:
                if board[last_row + i][last_column + i] == dropped_piece:
                    in_a_row += 1
                else:
                    break
            else:
                break
        for i in range(1, 5):
            if last_row - i >= 0 and last_column - i >= 0:
                if board[last_row - i][last_column - i] == dropped_piece:
                    in_a_row += 1
                else:
                    break
            else:
                break
        if in_a_row == 4:
            winner = 2 if turn == 1 else 2
            print("Four in a row!!! Player {0} wins!!! " \
                  "Party time.".format(winner))
            print()
            has_four_in_a_row = True
        # Check if there's four-in-a-row diagonally (\)
        in_a_row = 1
        for i in range(1, 5):
            if last_row - i >= 0 and last_column + i <= 6:
                if board[last_row - i][last_column + i] == dropped_piece:
                    in_a_row += 1
                else:
                    break
            else:
                break
        for i in range(1, 5):
            if last_row + i <= 6 and last_column - i >= 0:
                if board[last_row + i][last_column - i] == dropped_piece:
                    in_a_row += 1
                else:
                    break
            else:
                break
        if in_a_row == 4:
            winner = 2 if turn == 1 else 2
            print("Four in a row!!! Player {0} wins!!! " \
                  "Party time.".format(winner))
            print()
            has_four_in_a_row = True
    return has_four_in_a_row

def again():
    while True:
        choice = str(input("Play again? (Y/n): ").lower().split())
        if len(choice) == 2:
            play()
        else:
            if choice[2] == 'y':
                play()
            elif choice[2] == 'n':
                print("Thanks for playing!")
                print()
                sys.exit(0)
            else:
                print("Please type a \"y\" (or hit enter) for yes, " \
                      "or an \"n\" for no.")

# Calls the other functions
def play():
    reset_board()
    draw_board()
    while(not has_four_in_a_row()):
        column = prompt_column()
        drop_piece(column)
        change_turn()
        draw_board()
    again()

if __name__ == '__main__':
    req_version = (3,0)
    cur_version = sys.version_info

    if cur_version >= req_version:
        play()
    else:
        print("Connections requires Python 3 to run.")


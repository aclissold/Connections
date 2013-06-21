#!/usr/bin/python3
#
# Required methods:
#
# play()
# reset_board()
# draw_board()
# prompt_column()
# drop_piece()
# check_drop()
# change_turn()
# again()
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
from random import randint

# Initialize board to empty cells
board = [[[] for i in range(7)] for i in range(7)]
turn = randint(1, 2)

# Set each board cell to a space
def reset_board():
    for i in range(7):
        for j in range(7):
            board[i][j] = ' '

# Display the current board state to the user,
# in a pretty format.
def draw_board():
    print()
    print('   _____________')
    print('  |' + str(board[6][0]), board[6][1], board[6][2], board[6][3], board[6][4], board[6][5], str(board[5][6]) + '|')
    print('  |' + str(board[5][0]), board[5][1], board[5][2], board[5][3], board[5][4], board[5][5], str(board[5][6]) + '|')
    print('  |' + str(board[4][0]), board[4][1], board[4][2], board[4][3], board[4][4], board[4][5], str(board[4][6]) + '|')
    print('  |' + str(board[3][0]), board[3][1], board[3][2], board[3][3], board[3][4], board[3][5], str(board[3][6]) + '|')
    print('  |' + str(board[2][0]), board[2][1], board[2][2], board[2][3], board[2][4], board[2][5], str(board[2][6]) + '|')
    print('  |' + str(board[1][0]), board[1][1], board[1][2], board[1][3], board[1][4], board[1][5], str(board[1][6]) + '|')
    print('  |' + str(board[0][0]), board[0][1], board[0][2], board[0][3], board[0][4], board[0][5], str(board[0][6]) + '|')
    print(' /===============\\')
    print('   1 2 3 4 5 6 7')
    print()

def prompt_column():
    column = int(input("Choose a column: ")) - 1
    return column

def drop_piece(column):
    for row in range(7):
        if board[row][column] == ' ':
            if turn == 1:
                board[row][column] = 'x'
            elif turn == 2:
                board[row][column] = 'o'
            else:
                print('Error dropping piece (turn not 1 or 2)')
            break
        else:
            print('Row is full and I didn\'t implement this case yet.')

def check_drop():
    draw_board()

# Calls the other functions
def play():
    reset_board()
    draw_board()
    column = prompt_column()
    drop_piece(column)
    check_drop()

if __name__ == '__main__':
    play()


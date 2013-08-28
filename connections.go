// A simple command-line Connect Four clone.
//
// To-do:
//     Consider changing "x" to 'x' and using runes
//     Change var declarations to var()
//     Research int vs. uint8
//     Look up correct comment documentation format
//     Change board to by 7 x 6
//     Colorize winning pieces on Windows
//     Refactor:
//         Add comments/docstrings
//         Split up hasFourInARow()
//         Make classe(s)
//     Create online version
//
package main

import (
	"bufio"
	"fmt"
	"log"
	"math/rand"
	"os"
	"os/exec"
	"regexp"
	"runtime"
	"strconv"
	"strings"
	"time"
)

// Will be initialized to 7 x 7 empty cells to hold game pieces
var board [][]string

// Holds the player's turn info (initialized randomly)
var r *rand.Rand
var turn uint8

// Slices to hold indices of in-a-row pieces
var winningRows = make([]int, 0, 7)
var winningColumns = make([]int, 0, 7)

// Holds the indices of the last-dropped piece
var lastRow int
var lastColumn int

func main() {
    // Init
	board = make([][]string, 7)
	for i := range board {
		board[i] = make([]string, 7)
	}
    r = rand.New(rand.NewSource(time.Now().UnixNano()))
    turn = uint8(r.Intn(2)) + 1
	play() // Start the game!!!
}

// Call all the functions that make up Connections.
func play() {
	resetBoard()
	changeTurn()
	drawBoard()
	// while-loop conditions
	hasFour := false
	full := false
	for !hasFour && !full {
		// Ask the player for a column and save it
		column := promptColumn(false)
		dropPiece(column)
		// Check if the top row is full and save the boolean result
		full = topRowFull()
		if !full {
			changeTurn()
		}
		// Check if the last piece resulted in four+ in a row and save the
		// boolean result
		hasFour = hasFourInARow()
		if hasFour {
			win() // DING DING DING!
		} else {
			drawBoard()
		}
	}
	// Ask if the player wants to play again
	again()
}

// Reset (or initialize) the board to a clean slate.
func resetBoard() {
	// Clear all board cells by setting each index to a single space character
	for i := 0; i < 7; i++ {
		for j := 0; j < 7; j++ {
			board[i][j] = " "
		}
	}
	// Remove any winning indices from winningRows and winningColumns
	winningRows = winningRows[:-len(winningRows)]
	winningColumns = winningColumns[:-len(winningRows)]
}

func drawBoard() {
	/* Display the board on the screen.

	   Use a nested for-loops to iterated through the elements of board
	   and display them properly in a grid resembling a Connect Four game.
	*/
	fmt.Println("   _____________")
	for i := 6; i > -1; i-- {
		fmt.Print("  |")
		for j := 0; j < 6; j++ {
			fmt.Print(string(board[i][j]) + " ")
		}
		fmt.Println(string(board[i][6] + "|"))
	}
	fmt.Println(" /===============\\")
	fmt.Println("   1 2 3 4 5 6 7")
	fmt.Println()
}

func promptColumn(isFull bool) int {
	/* Ask the player what column to drop a piece in and return it.

	   Also, exit if the player types "q". true should be passed to this
	   function if promptColumn was called previously and found to be
	   a full column by dropPiece(). This causes a different prompt
	   message to be displayed.
	*/
	scanner := bufio.NewScanner(os.Stdin)
	var message string

	if isFull {
		message = "Column is full, please choose another: "
	} else {
		message = "Choose a column (or type q to quit): "
	}
	// Initialize column to an invalid number
	column := -1
	// "while column is invalid"
	for column < 0 || column > 6 {
		fmt.Print(message)
		scanner.Scan()
		choice := scanner.Text()
		if err := scanner.Err(); err != nil {
			log.Fatal("reading standard input:", err)
		}
		choice = strings.Trim(choice, " ")
		choice = strings.ToLower(choice)
        if len(choice) > 0 {
            if string(choice[0]) == "q" {
                fmt.Println("Thanks for playing!")
                fmt.Println()
                os.Exit(0)
            }
        }
		for column < 0 || column > 6 {
			// column, err := strconv.Atoi(choice) would create a new "column"
			var err error
            column, err = strconv.Atoi(choice)
			column -= 1
			if err != nil || column < 0 || column > 6 {
				fmt.Println("Please enter a number from 1 - 7 or \"q\".")
                break
			}
		}
	}
	return column
}

// Drop a game piece in the given column.
func dropPiece(column int) {
	// Iterate through the board from bottom to top
	for row := 0; row < 7; row++ {
		// Skip non-empty cells
		if board[row][column] == " " {
			if turn == 1 {
				// Drop piece
				board[row][column] = "x"
				// Store these indices for later
				lastRow, lastColumn = row, column
				return
			} else {
				board[row][column] = "o"
				lastRow, lastColumn = row, column
				return
			}
		}
	}
	// Column is full; did not return yet
	newColumn := promptColumn(true)
	dropPiece(newColumn)
}

// Set turn 1 to 2 or vice versa, clear the screen, and display turn info.
func changeTurn() {
	if turn == 1 {
		turn = 2
	} else {
		turn = 1
	}
	// XXX
	clear()
	fmt.Println()
	fmt.Printf(" ~Player %d's Turn~\n", turn)
}

// Clear the screen in preparation to redraw the board
func clear() {
	var cmd *exec.Cmd
	if runtime.GOOS == "windows" {
		cmd = exec.Command("cls")
	} else {
		cmd = exec.Command("clear")
	}
	cmd.Stdout = os.Stdout
	err := cmd.Run()
	if err != nil {
		log.Fatal(err)
	}
}

// Determine if the top row is full, and display "Draw" if returning true.
func topRowFull() bool {
	piecesInRow := 0
	// Count the pieces in the top row
	for column := 0; column < 7; column++ {
		if board[6][column] == " " {
			break
		} else {
			piecesInRow++
		}
	}
	if piecesInRow == 7 {
		clear()
		fmt.Println()
		fmt.Println(" IT'S A DRAW?!? Nobody wins! Sad day.")
		return true
	}
	return false
}

func hasFourInARow() bool {

    // psuedoBoard is a string representation of a row, column or diagonal of the
    // pieces on the board which can then be checked for four+ in a row via regexp.
    var psuedoBoard string

    // hasFourHelper simply holds the code that would be written four times otherwise
    hasFourHelper := func(psuedoBoard string) bool {
        hasFour, err := regexp.MatchString("xxxx.*|oooo.*", psuedoBoard)
        if err != nil {
            fmt.Fprintln(os.Stderr, err)
            os.Exit(1)
        }
        return hasFour
    }

    // Check for four+ in a row horizontally
    for i := 0; i < 7; i++ {
        psuedoBoard = ""
        for j := 0; j < 7; j++ {
            psuedoBoard += board[i][j]
        }
        hasFour := hasFourHelper(psuedoBoard)
        if hasFour {
            return true
        }
    }

    // Check for four+ in a row vertically
    for i := 0; i < 7; i++ {
        psuedoBoard = ""
        for j := 0; j < 7; j++ {
            psuedoBoard += board[j][i]
        }
        hasFour := hasFourHelper(psuedoBoard)
        if hasFour {
            return true
        }
    }
/*
    // Check for four+ in a row diagonally (/)
    for i := 0; i < 7; i++ {
        psuedoBoard = ""
        for j := 0; j < 7; j++ {
            psuedoBoard += board[i][j]
        }
        hasFour, err := regexp.MatchString("xxxx.*|oooo.*", psuedoBoard)
        if err != nil {
            fmt.Fprintln(os.Stderr, err)
            os.Exit(1)
        }
        if hasFour {
            return true
        }
    }

    // Check for four+ in a row diagonally (\)
    for i := 0; i < 7; i++ {
        psuedoBoard = ""
        for j := 0; j < 7; j++ {
            psuedoBoard += board[i][j]
        }
        hasFour, err := regexp.MatchString("xxxx.*|oooo.*", psuedoBoard)
        if err != nil {
            fmt.Fprintln(os.Stderr, err)
            os.Exit(1)
        }
        if hasFour {
            return true
        }
    }
*/

    // Never found a match
	return false
}

// func hasFourInARow() {
//     """Check if the previously dropped piece led to four+ in a row.
//
//     Return true if that was the case; false otherwise.
//
//     """
//     droppedPiece = board[lastRow][lastColumn]
//     hasFourInARow = false
//     winningRows.append(lastRow)
//     winningColumns.append(lastColumn)
//     in_a_row = 1

//     // Check if there's four-in-a-row horizontally
//     for i in range(1, 7):
//         // Right to left
//         if lastColumn - i >= 0:
//             if board[lastRow][lastColumn - i] == droppedPiece:
//                 in_a_row += 1
//                 winningRows.append(lastRow)
//                 winningColumns.append(lastColumn - i)
//             else:
//                 break
//         else:
//             break
//     for i in range(1, 7):
//         // Left to right
//         if lastColumn + i <= 6:
//             if board[lastRow][lastColumn + i] == droppedPiece:
//                 in_a_row += 1
//                 winningRows.append(lastRow)
//                 winningColumns.append(lastColumn + i)
//             else:
//                 break
//         else:
//             break
//     if in_a_row >= 4:
//         hasFourInARow = true
//     else:
//         if in_a_row > 1:
//             for i in range(in_a_row - 1):
//                 winningRows.pop()
//                 winningColumns.pop()
//     in_a_row = 1

//     // Check if there's four-in-a-row vertically
//     for i in range(1, 5):
//         // Bottom to top
//         if lastRow + i <= 6:
//             if board[lastRow + i][lastColumn] == droppedPiece:
//                 in_a_row += 1
//                 winningRows.append(lastRow + i)
//                 winningColumns.append(lastColumn)
//             else:
//                 break
//         else:
//             break
//     for i in range(1, 5):
//         // Top to bottom
//         if lastRow - i >= 0:
//             if board[lastRow - i][lastColumn] == droppedPiece:
//                 in_a_row += 1
//                 winningRows.append(lastRow - i)
//                 winningColumns.append(lastColumn)
//             else:
//                 break
//         else:
//             break
//     if in_a_row >= 4:
//         hasFourInARow = true
//     else:
//         if in_a_row > 1:
//             for i in range(in_a_row - 1):
//                 winningRows.pop()
//                 winningColumns.pop()
//     in_a_row = 1
//     // Check if there's four-in-a-row diagonally (/)
//     for i in range(1, 7):
//         // Lower-left to upper-right
//         if lastRow + i <= 6 and lastColumn + i <= 6:
//             if board[lastRow + i][lastColumn + i] == droppedPiece:
//                 in_a_row += 1
//                 winningRows.append(lastRow + i)
//                 winningColumns.append(lastColumn + i)
//             else:
//                 break
//         else:
//             break
//     for i in range(1, 7):
//         // Upper-right to lower-left
//         if lastRow - i >= 0 and lastColumn - i >= 0:
//             if board[lastRow - i][lastColumn - i] == droppedPiece:
//                 in_a_row += 1
//                 winningRows.append(lastRow - i)
//                 winningColumns.append(lastColumn - i)
//             else:
//                 break
//         else:
//             break
//     if in_a_row >= 4:
//         hasFourInARow = true
//     else:
//         if in_a_row > 1:
//             for i in range(in_a_row - 1):
//                 winningRows.pop()
//                 winningColumns.pop()
//     in_a_row = 1
//     // Check if there's four-in-a-row diagonally (\)
//     for i in range(1, 7):
//         if lastRow - i >= 0 and lastColumn + i <= 6:
//             if board[lastRow - i][lastColumn + i] == droppedPiece:
//                 in_a_row += 1
//                 winningRows.append(lastRow - i)
//                 winningColumns.append(lastColumn + i)
//             else:
//                 break
//         else:
//             break
//     for i in range(1, 7):
//         if lastRow + i <= 6 and lastColumn - i >= 0:
//             if board[lastRow + i][lastColumn - i] == droppedPiece:
//                 in_a_row += 1
//                 winningRows.append(lastRow + i)
//                 winningColumns.append(lastColumn - i)
//             else:
//                 break
//         else:
//             break
//     if in_a_row >= 4:
//         hasFourInARow = true
//     else:
//         if in_a_row > 1:
//             for i in range(in_a_row - 1):
//                 winningRows.pop()
//                 winningColumns.pop()
//     if not hasFourInARow:
//         // Also remove initial piece
//         winningRows.pop()
//         winningColumns.pop()
//     return hasFourInARow
// }

// Clear the screen, make winning pieces green, and print winning message.
func win() {
	var piece string
	var winner int
	// Clear the screen
	clear()
	// Change colors of the winning pieces (only on Mac/Linux)
	if turn == 2 {
		piece = "x"
	} else {
		piece = "o"
	}
	if runtime.GOOS != "windows" {
		piece = "\033[38;5;118m" + piece + "\033[0m"
	}
	for i := 0; i < len(winningRows); i++ {
		board[winningRows[i]][winningColumns[i]] = piece
	}
	// Draw the board with a unique winning message above and below
	fmt.Println()
	fmt.Println(" ~DING DING DING!~")
	drawBoard()
	if turn == 1 {
		winner = 1
	} else {
		winner = 2
	}
	fmt.Printf("Four in a row!!! Player %d wins!!! "+
		"Party time.\n", winner)
	fmt.Println()
}

// Ask the player if they want to play again and respond accordingly.
func again() {
	scanner := bufio.NewScanner(os.Stdin)
	var choice string
    fmt.Print("Play again? (Y/n): ")
	for {
		scanner.Scan()
		choice = scanner.Text()
		choice = strings.ToLower(choice)
		choice = strings.Trim(choice, " ")
		if err := scanner.Err(); err != nil {
			log.Fatal("reading standard input:", err)
		}
		// Accept no input as a default action
		if len(choice) == 0 {
			play()
		} else {
			// Accept any word starting with "y"
			if string(choice[0]) == "y" {
				play()
			} else if string(choice[0]) == "n" {
				// Accept any word starting with "n"
				fmt.Println("Thanks for playing!")
				fmt.Println()
				os.Exit(0)
			} else {
				fmt.Println("Please type a \"y\" (or hit enter) for yes, " +
					"or an \"n\" for no.")
			}
		}
	}
}

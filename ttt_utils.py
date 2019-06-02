# Author:       R. Bowie Smith
# Class:        CMSC 481 - Computer Networks
# Assignment:   Tic-Tac-Toe Project 2 - UDP
# Professor:    Edward Zieglar
# File:         ttt_utils.py
# Description:  Utility functions to help implement client and server sides of
#               tic-tac-toe game.

import os
import random

# Make "new game" [u,u,u,u,u,u,u,u,u]
def newGame():
    return ["u" for _ in range(0,9)]

# Turn gamestate data structure (list) to string
# Ex: [u,u,u,u,u,u,u,u,u] -> "uuuuuuuuu"
#     [u,X,u,O,O,u,X,u,u] -> "uXuOOuXuu"
def gameToString(state):
    return "".join(state)

# Turn gamestate string to gamestate data structure (list)
# Ex: "uuuuuuuuu" -> [u,u,u,u,u,u,u,u,u]
#     "uXuOOuXuu" -> [u,X,u,O,O,u,X,u,u]
def stringToGame(gameString):
    return list(gameString)

# Print out tic-tac-toe board with index key.
# 'X' and 'O' remain, but 'u' transformed to blank space
def printGame(state):
    state = list(map(lambda e: ' ' if e == 'u' else 'X' if e == 'X' else 'O', state))
    print()
    print("   ~~~   T I C   T A C   T O E   ~~~")
    print()
    print(f'    {state[0]} | {state[1]} | {state[2]}            0 | 1 | 2 ')
    print(f'   ---|---|---          ---|---|---          X = you')
    print(f'    {state[3]} | {state[4]} | {state[5]}            3 | 4 | 5 ')
    print(f'   ---|---|---          ---|---|---          O = nemesis')
    print(f'    {state[6]} | {state[7]} | {state[8]}            6 | 7 | 8 ')
    print()

# Given current game state, prompt player for move, performing error checking
# and reprompting if player makes invalid move
def promptPlayer(state):
    while True:
        print("Input the integer indicating which square you would like to 'X'.")
        playNumber = input("--> ")
        try:
            try:
                playNumber = int(playNumber)
            except Exception as e:
                raise ValueError(f"Position '{playNumber}' is not valid.")
            if playNumber < 0 or playNumber > 8:
                raise ValueError(f"Position '{playNumber}' is not valid.")
            if state[playNumber] != 'u':
                raise ValueError(f"Position '{playNumber}' already played.")
            return str(playNumber)
            break
        except Exception as e:
            print(e, "\n")

# Given game state, return winner as 'X' or 'O'
# If no winner, return 'N'
def checkWinner(state):
    if ((state[0] == 'X' and state[1] == 'X' and state[2] == 'X') or
        (state[3] == 'X' and state[4] == 'X' and state[5] == 'X') or
        (state[6] == 'X' and state[7] == 'X' and state[8] == 'X') or
        (state[0] == 'X' and state[3] == 'X' and state[6] == 'X') or
        (state[1] == 'X' and state[4] == 'X' and state[7] == 'X') or
        (state[2] == 'X' and state[5] == 'X' and state[8] == 'X') or
        (state[0] == 'X' and state[4] == 'X' and state[8] == 'X') or
        (state[2] == 'X' and state[4] == 'X' and state[6] == 'X')):
        return 'X'
    if ((state[0] == 'O' and state[1] == 'O' and state[2] == 'O') or
        (state[3] == 'O' and state[4] == 'O' and state[5] == 'O') or
        (state[6] == 'O' and state[7] == 'O' and state[8] == 'O') or
        (state[0] == 'O' and state[3] == 'O' and state[6] == 'O') or
        (state[1] == 'O' and state[4] == 'O' and state[7] == 'O') or
        (state[2] == 'O' and state[5] == 'O' and state[8] == 'O') or
        (state[0] == 'O' and state[4] == 'O' and state[8] == 'O') or
        (state[2] == 'O' and state[4] == 'O' and state[6] == 'O')):
        return 'O'
    return 'N'

# Given game state, returns true if tic-tac-toe board is "full" (no unplayed spaces)
# Returns false if blank spaces remain
def isBoardFull(state):
    return sum(1 if e == 'u' else 0 for e in state) == 0

# Given winner ('X' or 'O'), print winner message
def printWinner(winner):
    if winner == 'X':
        print("You Win!")
    elif winner == 'O':
        print("You lose :(")

# Print cat game message (when game board fills with no winner)
def printCatGame():
    print("Cat Game!")

# Cear user screen
def clearScreen():
    os.system('clear') if os.name == 'posix' else os.system('cls')

# Given game state, AI determines which square to place 'O'
# Returns random number from list of square indices not yet played
def aiDecision(gameState):
    openPositions = []
    for idx,val in enumerate(gameState):
        if val == 'u':
            openPositions.append(idx)
    return openPositions[random.randint(0, len(openPositions) - 1)]


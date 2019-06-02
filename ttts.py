# Author:       R. Bowie Smith
# Class:        CMSC 481 - Computer Networks
# Assignment:   Tic-Tac-Toe Project 2 - UDP
# Professor:    Edward Zieglar
# File:         ttts.py
# Description:  Server side of Tic-Tac_Toe game. Using UDP, server can handle multiple
#               concurrent client connections. Server has built-in "AI" that choses
#               random moves to play against client. See protocol specification for
#               information on messages exchanged between server and client.
#
#               Server holds the state of the game. Tic-Tac-Toe board has 9 squares
#               that can be in one of three states: 'X', 'O', or 'u' for unplayed.
#               Thus game state starts as [u,u,u,u,u,u,u,u,u] and u's are replaced
#               with 'X' and 'O' as gameplay commences.
#
# Usage:        python3 ttts.py

import socket
import sys
import signal
import random
import time

import ttt_utils as ttt



# Function to handle keyboard interrupt when cntl-c is pressed
# Closes socket and exits
# Args: Signal Number, Current Stack Frame Object
def cntl_c_handler(sig, frame):
    print("Closing listening socket and shutting down server...")
    serverSocket.close()
    sys.exit(0)
signal.signal(signal.SIGINT, cntl_c_handler) # register cntl-c handler



serverPort = 13037                                                  # Port Number
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)     # IPV4/UDP socket
serverSocket.bind(('', serverPort))                                 # Bind to all interfaces
print("Listening at:", serverSocket.getsockname())

# Dict structure to store games in key-value store
# Key:     (ipAddress, port)  Value: gameState
# Example: (123.34.98.7, 63456) - "XuuXOOuXO"
gameStates = {}

# Infinite loop to accept and handle gameplay requests
while True:
    request, clientAddress = serverSocket.recvfrom(2048)            # receive request
    requestMessage = request.decode()                               # decode message to string
    print(f"Received: '{requestMessage}', from: {clientAddress}")

    if clientAddress in gameStates:                                 # ongoing game logic
        gameState = ttt.stringToGame(gameStates[clientAddress])     # get matching game state

        gameState[int(requestMessage)] = 'X'                        # apply client move
        winner = ttt.checkWinner(gameState)
        # If winner or cat game after client move, send final game state and remove game
        if (winner != 'N' or ttt.isBoardFull(gameState)):
            if (winner == 'X'):
                serverSocket.sendto(('w_' + ttt.gameToString(gameState)).encode(), clientAddress)
            elif (winner == 'O'):
                serverSocket.sendto(('l_' + ttt.gameToString(gameState)).encode(), clientAddress)
            else:
                serverSocket.sendto(('c_' + ttt.gameToString(gameState)).encode(), clientAddress)
            del gameStates[clientAddress]
            continue

        indexOfAiMove = ttt.aiDecision(gameState)                   # AI decides move index
        gameState[indexOfAiMove] = 'O'                              # apply AI move

        winner = ttt.checkWinner(gameState)
        # If winner or cat game after server move, send final game state and remove game
        if (winner != 'N' or ttt.isBoardFull(gameState)):
            if (winner == 'X'):
                serverSocket.sendto(('w_' + ttt.gameToString(gameState)).encode(), clientAddress)
            elif (winner == 'O'):
                serverSocket.sendto(('l_' + ttt.gameToString(gameState)).encode(), clientAddress)
            else:
                serverSocket.sendto(('c_' + ttt.gameToString(gameState)).encode(), clientAddress)
            del gameStates[clientAddress]
            continue

        gameStates[clientAddress] = ttt.gameToString(gameState)     # store gameplay
        # send gamestate and indicator to continue play
        serverSocket.sendto(('p_' + ttt.gameToString(gameState)).encode(), clientAddress)


    else:                                           # new game logic (no entry in gameStates)
        gameState = ttt.newGame()                   # new game state list (empty board)
        if requestMessage != 's':                   # client makes first move if request != 's'
            gameState[int(requestMessage)] = 'X'    # Update gamestate with clients requested move

        indexOfAiMove = ttt.aiDecision(gameState)   # AI decides on first move
        gameState[indexOfAiMove] = 'O'              # AI makes first move

        gameStates[clientAddress] = ttt.gameToString(gameState)  # store new game
        # respond to client with game board and indication to continue play
        serverSocket.sendto(('p_' + ttt.gameToString(gameState)).encode(), clientAddress)

# Author:       R. Bowie Smith
# Class:        CMSC 481 - Computer Networks
# Assignment:   Tic-Tac-Toe Project 2 - UDP
# Professor:    Edward Zieglar
# File:         tttc.py
# Description:  Client side of Tic-Tac_Toe game. Using UDP, client makes connection
#               to tic-tac-toe server which plays client with AI. See protocol
#               specification for information on messages exchanged between client
#               and server.
#
# Usage:        python3 tttc.py -s serverIpOrHostname [-c]
#               Optional '-c' argument gives client the first move.

import socket
import sys
import ttt_utils as ttt

serverPort = 13037
usage = "USAGE: python tttc.py [-c] -s serverIP"

# If '-s' in command line arg list, serverName = indexOf('-s') + 1
# If no '-s' flag or no arg after 's', print usage and exit
if ('-s' in sys.argv):
    if (sys.argv.index('-s') + 1 >= len(sys.argv)):
        print(usage);
        sys.exit()
    else:
        serverName = sys.argv[sys.argv.index('-s') + 1]
        serverAddress = (serverName, serverPort)
else:
    print(usage);
    sys.exit()

# If '-c' in command line arg list, set clientFirst flag to true, indicating
# client makes first move. Else server makes first move
if ('-c' in sys.argv):
    clientFirst = True
else:
    clientFirst = False

# Create socket using AF_INET family using UDP transport protocol
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Function to retransmit previous requests until success or maxAttempts occurs
# messageToResend - last message sent by client
# numberAttempts  - current number of attempts by client
# maxAttempts     - max allowed attempts by client
# timeout         - number of seconds client waits before retransmission
def tryReceive(clientSocket, serverAddress, messageToResend, numberAttempts, maxAttempts, timeout):
    clientSocket.settimeout(timeout)
    try:
        response, serverResponseAddress = clientSocket.recvfrom(2048)
        return (response, serverResponseAddress)
    except socket.timeout:
        print(f'TIMEOUT {numberAttempts} of {maxAttempts}')
        if (numberAttempts >= maxAttempts):
            print("Exceeded max attempts. Server not responding. Aborting game.")
            clientSocket.close()
            sys.exit(0)
        else:
            clientSocket.sendto(messageToResend, serverAddress)
            return tryReceive(clientSocket, serverAddress, messageToResend, numberAttempts + 1, maxAttempts, timeout)


# Last request message -- holds value of last request in case timeout occurs and
# request needs to be resent
lastMessage = ''

if (clientFirst):   # If client first, prompt client for initial move and send request
    ttt.printGame(['u' for _ in range(0,9)])                # Print empty board with key
    firstMove = ttt.promptPlayer(['u' for _ in range(0,9)]) # Prompt user for move
    lastMessage = firstMove.encode()
    clientSocket.sendto(lastMessage, serverAddress)         # Send message to server
else:               # If client not first, send 's' to server indicating it makes first move
    lastMessage = b's'
    clientSocket.sendto(lastMessage, serverAddress)


# Game loop. Repeatedly receive reply from server and respond with index of desired
# move or 'e' to signal game end. Close socket when server responds with 'c'
while True:
    ttt.clearScreen()
    response, serverResponseAddress = tryReceive(clientSocket, serverAddress, lastMessage, 1, 10, 1.0)
    response = response.decode()
    action = response[0]
    gameState = ttt.stringToGame(response[2:])
    ttt.printGame(gameState)

    if (action == 'w' or action == 'l' or action == 'c'):   # win, loss, or cat game
        if (action == 'w' or action == 'l'):
            ttt.printWinner('X' if action == 'w' else 'O')
        if (action == 'c'):
            ttt.printCatGame()
        clientSocket.close()
        input("Press enter to continue")
        break
    else:                                                   # continue play
        nextMove = ttt.promptPlayer(gameState)
        lastMessage = nextMove.encode()
        clientSocket.sendto(lastMessage, serverResponseAddress)    # Send index of desired move

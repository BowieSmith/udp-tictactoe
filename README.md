# UDP Tic-Tac-Toe

## Usage
To start server:
`python3 ttts.py`

To start client:
`python3 tttc.py -s serverIP [-c]`

Options:
- -s : serverIP is the IP address of the machine running the UDP Tic-Tac-Toe server
If running the client on the same machine as the server, use 'localhost'
- -c : Optional. Allows client to make first move. Server makes first move by default.

## About
UDP Tic-Tac-Toe is exactly that. Tic-Tac-Toe over UDP.

In order to write the client and server sides of this application, a protocol was needed.
That protocol is defined in the document ttt_protocol_spec.pdf.

The client and server are simple implementations of the given protocol. The server
uses a naive AI to play against the client.

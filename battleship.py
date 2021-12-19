import sys
import socket
import pickle
import numpy
from tkinter import *

def endGameGUI(stat):
    for widget in root.winfo_children():
        widget.destroy()

    if(stat):
        Label(root, text="You win!", borderwidth=15, bg="blue").pack()
    else:
        Label(root, text="You lost :(", borderwidth=15, bg="floral white").pack()

def gameGetNameGUI():
    Player = StringVar(root)
    Label(root, text="Player write your name").pack()
    e1 = Entry(root, textvariable=Player).pack()

    def myClick():
        for widget in root.winfo_children():
            widget.destroy()
        initGame(Player.get())

    myButton = Button(root,
                      text='Ok',
                      fg='White',
                      bg='dark green', height=1, width=10, command=myClick).pack()


def gameBoardGUI(hostName, opponentName):
    borderWidth = 10
    Label(root, text=hostName, bg="green", relief="ridge", width=39, height=2).grid(row=0, column=1, columnspan=10,
                                                                                    rowspan=1,
                                                                                    sticky=E)
    Label(root, text=opponentName, bg="yellow", relief="ridge", width=39, height=2).grid(row=0, column=11,
                                                                                         columnspan=10,
                                                                                         rowspan=1, sticky=E)

    Label(root, text="", borderwidth=borderWidth).grid(row=1, column=0)
    Label(root, text="0", borderwidth=borderWidth, bg="green").grid(row=1, column=1)
    Label(root, text="1", borderwidth=borderWidth, bg="green").grid(row=1, column=2)
    Label(root, text="2", borderwidth=borderWidth, bg="green").grid(row=1, column=3)
    Label(root, text="3", borderwidth=borderWidth, bg="green").grid(row=1, column=4)
    Label(root, text="4", borderwidth=borderWidth, bg="green").grid(row=1, column=5)
    Label(root, text="5", borderwidth=borderWidth, bg="green").grid(row=1, column=6)
    Label(root, text="6", borderwidth=borderWidth, bg="green").grid(row=1, column=7)
    Label(root, text="7", borderwidth=borderWidth, bg="green").grid(row=1, column=8)
    Label(root, text="8", borderwidth=borderWidth, bg="green").grid(row=1, column=9)
    Label(root, text="9", borderwidth=borderWidth, bg="green").grid(row=1, column=10)

    Label(root, text="0", borderwidth=borderWidth, bg="yellow").grid(row=1, column=11)
    Label(root, text="1", borderwidth=borderWidth, bg="yellow").grid(row=1, column=12)
    Label(root, text="2", borderwidth=borderWidth, bg="yellow").grid(row=1, column=13)
    Label(root, text="3", borderwidth=borderWidth, bg="yellow").grid(row=1, column=14)
    Label(root, text="4", borderwidth=borderWidth, bg="yellow").grid(row=1, column=15)
    Label(root, text="5", borderwidth=borderWidth, bg="yellow").grid(row=1, column=16)
    Label(root, text="6", borderwidth=borderWidth, bg="yellow").grid(row=1, column=17)
    Label(root, text="7", borderwidth=borderWidth, bg="yellow").grid(row=1, column=18)
    Label(root, text="8", borderwidth=borderWidth, bg="yellow").grid(row=1, column=19)
    Label(root, text="9", borderwidth=borderWidth, bg="yellow").grid(row=1, column=20)

    Label(root, text="0", borderwidth=borderWidth, bg="white").grid(row=2, column=0)
    Label(root, text="1", borderwidth=borderWidth, bg="white").grid(row=3, column=0)
    Label(root, text="2", borderwidth=borderWidth, bg="white").grid(row=4, column=0)
    Label(root, text="3", borderwidth=borderWidth, bg="white").grid(row=5, column=0)
    Label(root, text="4", borderwidth=borderWidth, bg="white").grid(row=6, column=0)
    Label(root, text="5", borderwidth=borderWidth, bg="white").grid(row=7, column=0)
    Label(root, text="6", borderwidth=borderWidth, bg="white").grid(row=8, column=0)
    Label(root, text="7", borderwidth=borderWidth, bg="white").grid(row=9, column=0)
    Label(root, text="8", borderwidth=borderWidth, bg="white").grid(row=10, column=0)
    Label(root, text="9", borderwidth=borderWidth, bg="white").grid(row=11, column=0)

    for i in range(2, 12):
        for j in range(1, 11):
            labels.append(
                Label(root, text=" ", width=2, height=1, underline=2, bg="floral white", relief="groove").grid(row=i,
                                                                                                               column=j))

    for i in range(2, 12):
        for j in range(11, 21):
            labels.append(
                Label(root, text=" ", width=2, height=1, underline=2, bg="sky blue", relief="groove").grid(row=i,
                                                                                                           column=j))


# Parent class for other pieces.
class Piece:
    def __init__(self, size, horizontal):
        self.size = size
        self.horizontal = horizontal


class Carrier(Piece):
    sign = "C"
    name = "Carrier"
    size = 5

    def __init__(self, horizontal):
        Piece.__init__(self, Carrier.size, horizontal)


class Battleship(Piece):
    sign = "B"
    name = "Battleship"
    size = 4

    def __init__(self, horizontal):
        Piece.__init__(self, Battleship.size, horizontal)


class Submarine(Piece):
    name = "Submarine"
    sign = "S"
    size = 3

    def __init__(self, horizontal):
        Piece.__init__(self, Submarine.size, horizontal)


class Destroyer(Piece):
    name = "Destroyer"
    sign = "D"
    size = 2

    def __init__(self, horizontal):
        Piece.__init__(self, Destroyer.size, horizontal)


class Player:
    # All pieces every player must place on board
    pieces = [Carrier, Battleship, Submarine, Destroyer]

    def __init__(self):
        self.isTurn = False  # Turn to play
        self.unitCount = None  # Number of pieces as grid units.
        self.unitsLeft = None  # Total units - Shot units
        self.totalHits = 0  # Number of successful hits
        self.grid = numpy.zeros(shape=(10, 10))
        self.piecesPlaced = []  # To avoid placing the same units.

    def placePiece(self, piece, position):
        if self.checkPosition(piece, position) and self.checkPieceRepetition(piece):
            if piece.horizontal:
                for y in range(position[1], position[1] + piece.size):
                    self.grid[position[0], y] = 1
                    labelText[10 * position[0] + y] = piece.sign
            else:
                for x in range(position[0], position[0] + piece.size):
                    self.grid[x, position[1]] = 1
                    labelText[10 * x + position[1]] = piece.sign
            self.piecesPlaced.append(type(piece))

    # Check if occuppied or out of grid boundaries.
    def checkPosition(self, piece, position):
        if piece.horizontal:
            if (position[1] + piece.size) >= numpy.size(self.grid, 0):
                print("Piece is outside of the grid boundaries")
                return False
            for x in range(position[1], position[1] + piece.size):
                if self.grid[position[0], x] != 0:
                    print("Area occupied")
                    return False
        else:
            if (position[0] + piece.size) >= numpy.size(self.grid, 1):
                print("Piece is outside of the grid boundaries")
                return False
            for y in range(position[0], position[0] + piece.size):
                if self.grid[y, position[1]] != 0:
                    print("Area occupied")
                    return False
        return True

    # Check if any piece of same type is already placed.
    def checkPieceRepetition(self, piece):
        if self.piecesPlaced.count(type(piece)) == 0:
            return True
        else:
            print("This type of piece has already been placed.")
            return False

    # Returns the total number of squares occupied by the pieces.
    def countUnits(self):
        count = 0
        for piece in self.piecesPlaced:
            count += piece.size
        return count

    # Place pieces one by one via user input.
    def initBoard(self):
        for piece in Player.pieces:
            while self.piecesPlaced.count(piece) == 0:
                print("\nPlace ", piece.name, "(", piece.size, ") on grid.")
                pos = self.getPosInput()
                self.placePiece(piece(pos[2]), (pos[0], pos[1]))
            displayGrid(self.grid, 1)
        self.unitsLeft = self.countUnits()
        self.unitCount = self.countUnits()

    # Get position input for piece placement. (eg. 5,5,V)
    # H: Horizontal V: Vertical
    def getPosInput(self):
        while True:
            raw = input("Enter position as row,column,alignment: ")
            position = raw.split(',')

            if len(position) != 3:
                print("Invalid position format.")
                continue

            try:
                position[0] = int(position[0])
                position[1] = int(position[1])
            except:
                print("First two inputs must be an integer.")
                continue

            if position[2] == "H" or position[2] == "h":
                position[2] = True
            elif position[2] == "V" or position[2] == "v":
                position[2] = False
            else:
                print("Last input must be H or V")
                continue
            break
        return position

    # Get shot position input (eg. 5,5)
    def getShotInput(self):
        while True:
            raw = input("Enter the shot coordinates as row,column: ")
            position = raw.split(',')

            if len(position) != 2:
                print("Invalid position format.")
                continue

            try:
                position[0] = int(position[0])
                position[1] = int(position[1])
            except:
                print("Inputs must be an integer.")
                continue

            if position[0] > 9 or position[1] > 9:
                print("Position outside of the grid")
            break
        return position


# End of classes

#  Colorfully display grid
def displayGrid(grid, side):
    MySide = side  # host grid
    if (MySide):
        for row in range(0, grid.shape[0]):
            for col in range(0, grid.shape[1]):
                if grid[row][col] == 0:
                    labelText[row * 10 + col] = ""
                if grid[row][col] == 1:
                    labelText[row * 10 + col] = labelText[row * 10 + col]
                if grid[row][col] == 4:
                    labelText[row * 10 + col] = "x"
                    colors[row * 10 + col] = "green"
                if grid[row][col] == 8:
                    labelText[row * 10 + col] = labelText[row * 10 + col]
                    colors[row * 10 + col] = "red"
        print("\n")
    else:
        for row in range(0, grid.shape[0]):
            for col in range(0, grid.shape[1]):
                if grid[row][col] == 0:
                    labelText[100 + row * 10 + col] = ""
                if grid[row][col] == 1:
                    labelText[100 + row * 10 + col] = "B"
                if grid[row][col] == 4:
                    labelText[100 + row * 10 + col] = "x"
                    colors[100 + row * 10 + col] = "red"
                if grid[row][col] == 8:
                    labelText[100 + row * 10 + col] = "H"
                    colors[100 + row * 10 + col] = "green"
        print("\n")
    index = 0
    for i in range(2, 12):
        for j in range(1, 11):
            labels.append(
                Label(root, text=labelText[index], width=2, height=1, underline=2, bg=colors[index],
                      relief="groove").grid(row=i,
                                            column=j))
            index = index + 1

    for i in range(2, 12):
        for j in range(11, 21):
            labels.append(
                Label(root, text=labelText[index], width=2, height=1, underline=2, bg=colors[index],
                      relief="groove").grid(row=i,
                                            column=j))
            index = index + 1


# Handles shot send/recv operations.
def shootByTurns(player, connection, hostName, opponentName):
    isGameOver = False
    opponentGrid = numpy.zeros(shape=(10, 10))

    while not (isGameOver):
        while player.isTurn and not (isGameOver):
            # Get shoot position from player.
            shotPos = player.getShotInput()

            # Send position to opponent.
            connection.send(pickle.dumps(shotPos))

            # Opponent sends back whether the sent position was a hit or not.
            hitOrMiss = pickle.loads(connection.recv(1024))

            if hitOrMiss == 1:
                opponentGrid[shotPos[0]][shotPos[1]] = 8
                displayGrid(opponentGrid, 0)
                player.totalHits += 1
                if player.totalHits >= player.unitCount:
                    print(hostName, " won!")
                    isGameOver = True
                    player.isTurn = False
                    endGameGUI(1)
                continue
            elif hitOrMiss == 0:
                # If it's not a hit, player's turn ends.
                opponentGrid[shotPos[0]][shotPos[1]] = 4
                player.isTurn = False
                displayGrid(opponentGrid, 0)
                print("\nWaiting for ", opponentName, ".\n", sep="")
            else:
                print("Shot already made.")
                continue
        while not (player.isTurn) and not (isGameOver):
            shotRecieved = pickle.loads(connection.recv(1024))

            # Check if shot made by opponent was a hit or not, send back the result.
            if player.grid[shotRecieved[0]][shotRecieved[1]] == 1:
                player.grid[shotRecieved[0]][shotRecieved[1]] = 8
                player.unitsLeft -= 1
                if player.unitsLeft <= 0:
                    print(hostName, "lost!")
                    isGameOver = True
                    endGameGUI(0)
                connection.send(pickle.dumps(1))
            elif player.grid[shotRecieved[0]][shotRecieved[1]] == 4:
                connection.send(pickle.dumps(2))
            elif player.grid[shotRecieved[0]][shotRecieved[1]] == 8:
                connection.send(pickle.dumps(2))
            else:
                # If it's not a hit, player's turn begins.
                player.grid[shotRecieved[0]][shotRecieved[1]] = 4
                connection.send(pickle.dumps(0))
                player.isTurn = True
            displayGrid(player.grid, 1)


def initGame(hostName):
    opponentName = None

    # Host player
    if (isHost):
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serverSocket.bind(('0.0.0.0', port))
        serverSocket.listen(1)

        print("Waiting for player...\n")
        (connection, clientAddress) = serverSocket.accept()

        connection.send(pickle.dumps(hostName))
        opponentName = pickle.loads(connection.recv(1024))

        gameBoardGUI(hostName, opponentName)

        print("Player connected! Address:", clientAddress, "\n")
        print("Opponent name:", opponentName, "\n")

        hostPlayer = Player()
        hostPlayer.initBoard()
        hostPlayer.isTurn = True

        shootByTurns(hostPlayer, connection, hostName, opponentName)
        connection.close()
    else:
        # Client player
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serverAddress = hostIP, port
        clientSocket.connect(serverAddress)

        clientSocket.send(pickle.dumps(hostName))
        opponentName = pickle.loads(clientSocket.recv(1024))

        gameBoardGUI(hostName, opponentName)

        print("Player connected! Address:", serverAddress, "\n")
        print("Opponent name:", opponentName, "\n")

        clientPlayer = Player()
        clientPlayer.initBoard()

        shootByTurns(clientPlayer, clientSocket, hostName, opponentName)
        clientSocket.close()


# Handling the command line arguments
isHost = False
if len(sys.argv) == 2:
    isHost = True
    port = int(sys.argv[1])
elif len(sys.argv) == 3:
    hostIP = sys.argv[1]
    port = int(sys.argv[2])
else:
    print("Invalid arguments.")
    sys.exit()

labelText = []
for i in range(200):
    labelText.append(" ")
colors = []
for i in range(100):
    colors.append("floral white")
for i in range(100, 200):
    colors.append("sky blue")
labels = []
root = Tk()
root.wm_title("BATTLESHIP")
gameGetNameGUI()
root.mainloop()

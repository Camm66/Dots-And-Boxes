from collections import deque
from Box import *

class Board:
    def __init__(self, _m, _n):
        self.playerScore = 0
        self.aiScore = 0
        self.m = _m
        self.n = _n
        self.boxes = self.generateBoxes(_m, _n)
        self.openVectors = self.generateVectors(_m, _n)
        self.connectedVectors = set()
        self.lastValue = 0
        self.prevComplete = False
        # For alpha beta pruning
        self.alpha = -100000
        self.beta = 100000

    def generateBoxes(self, m, n):
        '''
        This function generates number of Box objects represented on the board.
        The Box serves as a data structure for the requisite meta data needed to represent
        state information.
        '''
        cols = n
        rows = m
        boxes = [[Box(0, 0) for j in range(cols)] for i in range(rows)]
        for i in range(m):
            for j in range(n):
                boxes[i][j] = (Box(i, j))
        return boxes

    def generateVectors(self, m, n):
        '''
        The vectors represent all of the available moves, or lines, which can
        be played on a game board of m rows and n columns. These are stored as tuples
        containing each coordinate and are stored on a queue. The vector queue, along
        with the list of boxes that correspond to the coordinates, are used to represent
        game state.
        Vector format: ((x1, y1), (x2, y2))
        '''
        vectors = deque()
        for i in range(0, m+1):
            for j in range(0, n):
                vectors.append(((j, i), (j + 1, i)))
                if i < m:
                    vectors.append(((j, i), (j, i + 1)))
            if i < m:
                vectors.append(((n, i), (n, i + 1)))
        return vectors

    def displayBoard(self):
        '''
        This function generates a text-based representation of the current board state
        to be displayed on the command line. The display is based on the row & column
        values stored on the board, along with the connectedVectors set objects, which
        stores previously connected dots.
        '''
        print("Player 1: %s" % self.playerScore)
        print("Player AI: %s" % self.aiScore)
        # Set X axis Labels
        str1 = "\n  "
        for i in range(self.m + 1):
            str1 = str1 + "   %s" % i
        print(str1)

        # Draw remaining board
        boxVal = " "
        for i in range(self.m + 1):
            # Append the Y axis label to the beginning of a row
            str1 = "%s " % i
            str2 = "     "
            for j in range(self.n + 1):
                # Check for horizontal connections
                if ((j - 1, i), (j, i)) in self.connectedVectors:
                    str1 = str1 + "---*"
                else:
                    str1 = str1 + "   *"

                # Check for the box value of a given square based on the top left coordinate
                if j < self.n:
                    if self.boxes[j][i - 1].TopLeft == (j, i - 1):
                        boxVal = self.boxes[j][i - 1].value
                else:
                    boxVal = " "

                # Check for vertical connections
                if ((j, i - 1), (j, i)) in self.connectedVectors:
                    str2 = str2 + "| %s " % boxVal
                else:
                    str2 = str2 + "  %s " % boxVal
            print(str2)
            print(str1)
        print("")

    def move(self, coordinates, player):
        '''
        We place move on the board by checking searching the queue of openVectors for our
        selected coordinates. On success, we pop the coordinates off the queue and add
        them to the list of connectedVectors before searching the list of boxes for potential
        completions.
        An unsuccessful attempt will inform the calling function by returning -1
        '''
        if player is True:
            player = 1
        elif player is False:
            player = 0
        if coordinates in self.openVectors:
            self.openVectors.remove(coordinates)
            self.connectedVectors.add(coordinates)
            self.checkBoxes(coordinates, player)
            return 0
        else:
            return -1

    def checkBoxes(self, coordinates, player):
        '''
        This function takes a set of coordinates, and the current player arguments.
        It iterates over the list of boxes to find if the line falls on a stored box.
        If this completes the box, the player that initiated this process is awarded points.
        '''
        for i in range(self.m):
            for j in range(self.n):
                # Identify box based on upper left coordinate
                box = self.boxes[i][j]
                if coordinates in box.lines:
                    box.connectDot(coordinates)
                    # Store the value of most recently selected box, to be used by AI
                    self.lastValue = box.value
                if box.complete is True and box.owner is None:
                    box.owner = player
                    self.prevComplete = True
                    # Assign points to whomever completed the box
                    if player == 0:
                        self.playerScore += box.value
                    elif player == 1:
                        self.aiScore += box.value
                else:
                    self.prevComplete = False

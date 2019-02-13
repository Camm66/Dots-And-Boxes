'''
Components

1. UI
    - Displays Current Board
    - Gets User action
    - Reports Results

2. Board
    - Generate board based on dimensions
    - Represent in a 2d array?

3. Intelligent Agent
    - IE) the AI opponent
    - Takes board state after user moves, makes a new move, returns altered board state
    - Utilizes minimax search to make move selection
'''
from random import randint


class DotsAndBoxes:
    def __init__(self, _ply, _x, _y):
        self.playerScore = 0
        self.aiScore = 0
        self.ply = _ply
        self.board = Board(_x, _y)

    def playGame(self):
        print("Dots And Boxes")
        while True:
            self.board.displayBoard()
            print("Player 1 Score: %s" % self.playerScore)
            print("Player 2 Score: %s\n" % self.aiScore)
            print("Coordinate format == x,y,x2,y2")
            print("Hit 0 and enter to quit")
            try:
                integers = input("Enter the coordinates of the dots you wish to connect:")
                if integers == 0:
                    break
                coordinate = (integers[0], integers[1])
                coordinate2 = (integers[2], integers[3])
                success = self.board.move((coordinate, coordinate2))
                if success:
                    print("Please wait while your opponent moves...")
                else:
                    print("Invalid coordinates specified!")
            except SyntaxError:
                print("Invalid input, please try again...")
        print("\nExiting game...")

    def minimax(self):
        pass


class Board:
    def __init__(self, _m, _n):
        self.m = _m
        self.n = _n
        self.moves = (_m + 1) * (_n + 1)
        self.boxes = self.generateBoxes(_m, _n)
        self.connectedVectors = set()
        self.openVectors = self.generateVectors(_m, _n)
        # Test Box
        self.connectedVectors.add(((0, 0), (1, 0)))
        self.connectedVectors.add(((1, 0), (1, 1)))
        self.connectedVectors.add(((0, 0), (0, 1)))
        self.connectedVectors.add(((0, 1), (1, 1)))

        self.openVectors.remove(((0, 0), (1, 0)))
        self.openVectors.remove(((1, 0), (1, 1)))
        self.openVectors.remove(((0, 0), (0, 1)))
        self.openVectors.remove(((0, 1), (1, 1)))

    def generateBoxes(self, m, n):
        cols = n
        rows = m
        boxes = [[Box(0, 0) for j in range(cols)] for i in range(rows)]
        for i in range(m):
            for j in range(n):
                boxes[i][j] = (Box(i, j))
        return boxes

    def generateVectors(self, m, n):
        vectors = set()
        for i in range(0, m):
            for j in range(0, n):
                vectors.add(((j, i), (j, i + 1)))
                vectors.add(((j, i), (j + 1, i)))
            vectors.add(((n, i), (n, i + 1)))
        return vectors

    def displayBoard(self):
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

    def move(self, coordinates):
        if coordinates in self.openVectors:
            self.openVectors.discard(coordinates)
            self.connectedVectors.add(coordinates)
            self.checkBoxes(coordinates)
            return True
        else:
            return False

    def checkBoxes(self, coordinates):
        pass
    '''




    value = 0
    box = None
    for i in range(self.m):
        for j in range(self.n):
            box = boxes[i][j]
            if coordinates in box.lines:
                box.check(coordinates)
            if box.complete == true:
                value = box.value
                break
    return value
    '''

class Box:
    def __init__(self, _x, _y):
        # Top Left Coordinate
        self.TopLeft = (_x, _y)
        # Top Right Coordinate
        self.TopRight = (_x + 1, _y)
        # Bottom Left Coordinate
        self.BottomLeft = (_x, _y + 1)
        # Bottom Right Coordinate
        self.BottomRight = (_x + 1, _y + 1)
        # Coordinate Set
        self.coordinates = set([self.TopLeft, self.TopRight, self.BottomLeft, self.BottomRight])
        # Top line
        self.TopLine = (self.TopLeft, self.TopRight)
        # Right Line
        self.RightLine = (self.TopRight, self.BottomRight)
        # Bottom Line
        self.BottomLine = (self.BottomLeft, self.BottomRight)
        # Left Line
        self.LeftLine = (self.TopLeft, self.BottomLeft)
        # Line set
        self.lines = ([self.TopLine, self.RightLine, self.BottomLine, self.LeftLine])
        # Indicator for connected dots
        self.top = False
        self.right = False
        self.bottom = False
        self.left = False
        # Player that completed this box
        self.owner = None
        self.complete = False
        # Random number 1-5 indicating the value of this box
        self.value = randint(1, 5)

    def connectDot(self, coordinate, coordinate2):
        line = (coordinate, coordinate2)
        success = False
        if line in self.lines:
            if line == self.TopLine and self.top is False:
                self.top = True
                success = True
            elif line == self.RightLine and self.right is False:
                self.right = True
                success = True
            elif line == self.BottomLine and self.bottom is False:
                self.bottom = True
                success = True
            elif line == self.LeftLine and self.left is False:
                self.left = True
                success = True
        return success

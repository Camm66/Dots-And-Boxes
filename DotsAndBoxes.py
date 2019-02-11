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
        self.board.displayBoard()
#        while True:
#            action = input("Enter the coordinates of the dots you wish to connect:")
#            integers = [int(x) for x in action.split()]
#            coordinate = (integers[0], integers[1])
#            coordinate2 = (integers[2], integers[3])
#            self.board.move(coordinate, coordinate2)

    def minimax(self):
        pass


class Board:
    def __init__(self, _m, _n):
        self.m = _m
        self.n = _n
        self.moves = (_m + 1) * (_n + 1)
        self.board = self.generateBoxes(_m, _n)

    def generateBoxes(self, m, n):
        cols = n
        rows = m
        boxes = [[Box(0, 0) for j in range(cols)] for i in range(rows)]
        for i in range(m):
            for j in range(n):
                boxes[i][j] = (Box(i, j))
        return boxes

    def displayBoard(self):
        print("Dots And Boxes")
        
        str = "  "
        for i in range(self.m + 1):
            str = str + "%s   " % i
        print(str)

        for i in range(self.m + 1):
            str = "%s " % i
            for j in range(self.n + 1):
                str = str + "*   "
            print(str)
            print("")

    def move(self, coordinate, coordinate2):
        pass


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



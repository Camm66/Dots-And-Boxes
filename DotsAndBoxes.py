from random import randint


class DotsAndBoxes:
    def __init__(self, _ply, _x, _y):
        self.ply = _ply
        self.board = Board(_x, _y)

    def playGame(self):
        print("Dots And Boxes")
        while len(self.board.openVectors) > 0:
            print("Player 1 Score: %s" % self.board.playerScore)
            print("Player 2 Score: %s\n" % self.board.aiScore)
            print("Coordinate format == x,y,x2,y2")
            print("Hit 0 and enter to quit")
            success = self.playerMove()
            if success is False:
                break
            print("Please wait while your opponent moves...")
            self.aiMove()
        self.reportWinner()

    def reportWinner(self):
        if self.board.playerScore > self.board.aiScore:
            print("You won!")
        elif self.board.playerScore < self.board.aiScore:
            print("The AI won!")
        else:
            print("The game was a draw")
        print("Player 1 Score: %s" % self.board.playerScore)
        print("AI Score: %s" % self.board.aiScore)
        print("Exiting game...")

    def playerMove(self):
        while True:
            try:
                self.board.displayBoard()
                integers = input("Enter the coordinates of the dots you wish to connect:")

                if integers is 0:
                    return False

                coordinate = (integers[0], integers[1])
                coordinate2 = (integers[2], integers[3])

                success = self.board.move1((coordinate, coordinate2))

                if success == 0:
                    break
                elif success == -1:
                    print("Invalid coordinates specified!")
            except SyntaxError:
                print("Invalid input, please try again...")
        return True

    def aiMove(self):
        pass

    def minimax(self):
        pass

class Board:
    def __init__(self, _m, _n):
        self.playerScore = 0
        self.aiScore = 0
        self.m = _m
        self.n = _n
        self.moves = (_m + 1) * (_n + 1)
        self.boxes = self.generateBoxes(_m, _n)
        self.connectedVectors = set()
        self.openVectors = self.generateVectors(_m, _n)

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
        for i in range(0, m+1):
            for j in range(0, n):
                vectors.add(((j, i), (j + 1, i)))
                if i < m:
                    vectors.add(((j, i), (j, i + 1)))
            if i < m:
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

    def move1(self, coordinates):
        if coordinates in self.openVectors:
            self.openVectors.discard(coordinates)
            self.connectedVectors.add(coordinates)
            success = self.checkBoxes(coordinates, 1)
            if success:
                return 1
            else:
                return 0
        else:
            return -1

    def checkBoxes(self, coordinates, owner):
        success = False
        for i in range(self.m):
            for j in range(self.n):
                box = self.boxes[i][j]
                if coordinates in box.lines:
                    box.connectDot(coordinates)
                if box.complete is True and box.owner is None:
                    box.owner = owner
                    if owner == 1:
                        self.playerScore += box.value
                    success = True
                    print("Success!")
        return success


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

    def connectDot(self, coordinates):
        line = coordinates
        print("Connecting")
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
        if self.top is True and self.right is True and self.bottom is True and self.right is True:
            self.complete = True
        return success

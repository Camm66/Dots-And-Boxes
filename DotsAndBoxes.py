from copy import deepcopy
from collections import deque
from Box import *


class DotsAndBoxes:
    def __init__(self, _x, _y, _ply):
        self.ply = _ply
        self.board = Board(_x, _y)

    def playGame(self):
        '''
        This function contains the main loop of the game. It oscillates moves between the player
        and the AI until the number of available moves is exhausted.
        '''
        print("Dots And Boxes")
        while len(self.board.openVectors) > 0:
            print("Coordinate format == x,y,x2,y2")
            print("Hit 0 and enter to quit")

            self.board.displayBoard()

            success = self.playerMove()
            if success is False:
                break
            print("Please wait while your opponent moves...")

            self.aiMove()
        self.reportWinner()

    def reportWinner(self):
        '''
        This function is called upon the completion, or exit, from the game. A summary containing the scores
        and the winner of the game is printed to the command line.
        '''
        self.board.displayBoard()
        if self.board.playerScore > self.board.aiScore:
            print("You won!")
        elif self.board.playerScore < self.board.aiScore:
            print("The AI won!")
        else:
            print("The game was a draw")
        print("Player Score: %s" % self.board.playerScore)
        print("AI Score: %s" % self.board.aiScore)
        print("\nExiting game...")

    def playerMove(self):
        '''
        This enables users to select their move by taking user input from the command line in the
        following format: x1,y1,x2,y2
        Alternatively, the user may enter 0 to exit the loop and quit the game. A successful move on the
        board returns a 0 and exits the loop, and unsuccessful move returns -1, specifying invalid user input.
        '''
        while True:
            try:
                integers = input("Enter the coordinates of the dots you wish to connect:")
                if integers is 0:
                    return False

                coordinates = ((integers[0], integers[1]), (integers[2], integers[3]))

                success = self.board.move(coordinates, False)

                if success == 0:
                    break
                elif success == -1:
                    print("Invalid coordinates specified!")
            except SyntaxError:
                print("Invalid input, please try again...")
        return True

    def aiMove(self):
        '''
        This function is called from the main playGame() function upon the successful completion of a
        player move. It makes a call to minimax() to execute the minimax algorithm and retrieve the
        move to be executed by the AI on the game board.
        '''
        # Create a copy of the current board state for tree calculation
        state = deepcopy(self.board)
        openVectors = deepcopy(self.board.openVectors)

        # Retrieve coordinates from minimax algorithm
        coordinates = self.minimax(state, openVectors, self.ply, True)

        self.board.move(coordinates[1], True)

    def minimax(self, state, openVectors, ply, max):
        '''
        This function contains the core logic regarding the minimax algorithm.
        Parameters:
            state - represents the current board state
            openVectors - represents the available successors from the current state
            ply - represents the total depth of the game tree
            max - a value of True represents the AI, False represents the adversary
        Individual successor states are created in the main loop, before recursively
        calling the minimax algorithm to explore subsequent descendants of the tree.
        '''
        # The value of bestMove defaults to -inf for a Max layer, and +inf for a Min Layer
        if max is True:
            bestMove = (-1, None)
        else:
            bestMove = (1000000, None)

        # If the ply depth limit is reached or available successors are exhausted,
        # we evaluate and return the value of the current state
        if ply == 0 or len(openVectors) == 0:
            h = self.evaluationFunction(state)
            return (h, None)

        # Get successors
        for i in range(0, len(openVectors)):
            # Retrieve coordinates of current successor state
            move = openVectors.pop()

            # Create a deep copy of the state to be explored
            stateCopy = deepcopy(state)
            openVectorsCopy = deepcopy(openVectors)
            stateCopy.move(move, max)

            # Add the coordinates back onto the openVector list, this ensures subsequent
            # child states at the current depth can fully explore the remainder of the tree
            openVectors.appendleft(move)

            # Make a recursive call to the minimax function with the child state
            # The goal state is back propagated up the tree upon the end of recursion,
            # IE, when ply limit is reached or the open moves are exhausted
            nextMove = self.minimax(stateCopy, openVectorsCopy, ply - 1, not max)

            # Check the score returned from the child state against the 'bestScore'
            if max is True:
                # At a max level, we seek scores higher than the current max
                if nextMove[0] > bestMove[0]:
                    bestMove = (nextMove[0], move)
            else:
                # At a min level, we seek scores lower than the current max
                if nextMove[0] < bestMove[0]:
                    bestMove = (nextMove[0], move)
        return bestMove

    def evaluationFunction(self, state):
        '''
        This an evaluation function which calculates the heuristic value of a given leaf state.
        In this case, h == current point total for the AI in this state.
        Additionally, x == the value of the most recent partially filled box / 10.
        This is used to bias the AI towards larger value squares at lower ply values and initial states
        '''
        if state.prevComplete is False:
            x = float(state.lastValue) / float(10)
        else:
            x = 0
        h = state.aiScore
        return float(h) + x


class Board:
    def __init__(self, _m, _n):
        self.playerScore = 0
        self.aiScore = 0
        self.lastValue = 0
        self.prevComplete = False
        self.m = _m
        self.n = _n
        self.boxes = self.generateBoxes(_m, _n)
        self.openVectors = self.generateVectors(_m, _n)
        self.connectedVectors = set()

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
        print("Player 2: %s" % self.aiScore)
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
                    if player is False:
                        self.playerScore += box.value
                    elif player is True:
                        self.aiScore += box.value
                else:
                    self.prevComplete = False

from copy import deepcopy
from Board import *


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
            print(self.board.openVectors)
            success = self.playerMove()
            if success is False:
                break
            print(self.board.playerScore)
            print(self.board.aiScore)
            print("Please wait while your opponent moves...")
            self.aiMove()
            print(self.board.playerScore)
            print(self.board.aiScore)
        self.reportWinner()

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

                success = self.board.move(coordinates, 0)

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
        state = self.copy(self.board)

        # Retrieve coordinates from minimax algorithm
        coordinates = self.minimax(state, self.ply, True)
        print(coordinates)
        self.board.move(coordinates[1], 1)

    def minimax(self, state, ply, max_min):
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
        if max_min is True:
            bestMove = (-1000000, None)
        else:
            bestMove = (1000000, None)

        # If the ply depth limit is reached or available successors are exhausted,
        # we evaluate and return the value of the current state
        if ply <= 0 or len(state.openVectors) == 0:
            h = state.aiScore
            print("Leaf score %s" % h)
            return (h, None)

        # Get successors
        for i in range(0, len(state.openVectors)):
            # Retrieve coordinates of current successor state
            move = state.openVectors.pop()

            # Create a deep copy of the state to be explored
            stateCopy = self.copy(state)
            if max_min is True:
                stateCopy.move(move, 0)
            else:
                stateCopy.move(move, 1)

            # Add the coordinates back onto the openVector list, this ensures subsequent
            # child states at the current depth can fully explore the remainder of the tree
            state.openVectors.appendleft(move)

            # Make a recursive call to the minimax function with the child state
            # The goal state is back propagated up the tree upon the end of recursion,
            # IE, when ply limit is reached or the open moves are exhausted
            nextMove = self.minimax(stateCopy, ply - 1, not max_min)
            print("%s %s" % (nextMove[0], move))
            # Check the score returned from the child state against the 'bestScore'
            if max_min is True:
                # At a max level, we seek scores higher than the current max
                if nextMove[0] > bestMove[0]:
                    bestMove = (nextMove[0], move)
            else:
                # At a min level, we seek scores lower than the current max
                if nextMove[0] < bestMove[0]:
                    bestMove = (nextMove[0], move)
        return bestMove

    def copy(self, state):
        stateCopy = deepcopy(state)
        stateCopy.openVectors = deepcopy(state.openVectors)
        stateCopy.boxes = deepcopy(state.boxes)
        return stateCopy

    def evaluationFunction(self, state):
        '''
        This an evaluation function which calculates the heuristic value of a given leaf state.
        In this case, h == point total for the AI - point total for the player
        Additionally, x == the value of the most recent partially filled box / 10.
        This is used to bias the AI towards larger value squares at lower ply values and initial states
        '''
        h = state.aiScore
        return h

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


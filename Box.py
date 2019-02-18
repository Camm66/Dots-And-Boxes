from random import randint


class Box:
    def __init__(self, _x, _y):
        # Coordinate Set
        self.coordinates = [(_x, _y), (_x + 1, _y), (_x, _y + 1), (_x + 1, _y + 1)]
        # Top Left coordinate for easy identification
        self.TopLeft = (_x, _y)
        # Top line
        self.TopLine = (self.coordinates[0], self.coordinates[1])
        # Right Line
        self.RightLine = (self.coordinates[1], self.coordinates[3])
        # Bottom Line
        self.BottomLine = (self.coordinates[2],  self.coordinates[3])
        # Left Line
        self.LeftLine = (self.coordinates[0],  self.coordinates[2])
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
        if self.top is True and self.right is True and self.bottom is True and self.left is True:
            self.complete = True
        return success

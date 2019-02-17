from DotsAndBoxes import *

integers = input("Please enter the length, width, and (ai)depth of the board (x,y,z): ")
m = integers[0]
n = integers[1]
ply = integers[2]
game = DotsAndBoxes(m, n, ply)
game.playGame()
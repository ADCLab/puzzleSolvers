import sys
sys.path.append('../')

from puzzleSolver import PuzzlePiece,PuzzlePieces, Solver
from numpy.random import uniform
from numpy import zeros
#--------------------------------------------------------
# Create individual puzzle pieces then add to the puzzle
#--------------------------------------------------------
p1=PuzzlePiece([0,0],[5,5])
p2=PuzzlePiece([1,1],[6,6])
pps=PuzzlePieces()
pps.addPuzzlePieceObj(p1)
pps.addPuzzlePieceObj(p2)


#--------------------------------------------------------
# Create puzzle from list of xy points
#--------------------------------------------------------
numPieces=6
xy_0=uniform(0,1,size=(numPieces,2))
xy_d=uniform(5,6,size=(numPieces,2))
pps=PuzzlePieces()
pps.addPuzzlePieceXYs(xy_0,xy_d)
mySolver=Solver(pps)
mySolver.optimize()


A=zeros((numPieces,numPieces))
A[mySolver.ridx,mySolver.cidx]=1
print(A)
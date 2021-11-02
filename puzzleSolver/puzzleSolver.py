#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import deque
from scipy.spatial import distance
from numpy import zeros, eye
from scipy.optimize import linear_sum_assignment

def delete_nth(d, n):
    d.rotate(-n)
    d.popleft()
    d.rotate(n)

class PuzzlePiece(object):
    def __init__(self,initPos,desiredPos):
        self.initPos=initPos
        self.desiredPos=desiredPos

class PuzzlePieces(deque):
    def __init__(self):
        self.num=0
        
        
    def addPuzzlePieceObj(self,newPiece):
        if isinstance(newPiece, PuzzlePiece):
            self.append(newPiece)
            self.num=self.num+1
        else:
            raise ValueError('Expecting new puzzle piece of type puzzlePiece.')        

    def addPuzzlePieceObjs(self,newPieces):
        if isinstance(newPieces,list):
            for newPiece in newPieces:
                self.addPuzzlePieceObj(newPiece)

    def addPuzzlePieceXY(self,initPos,desiredPos):
        self.addPuzzlePieceObj(   PuzzlePiece(initPos,desiredPos)     )
        self.num=self.num+1
        
    def addPuzzlePieceXYs(self,initPos_list,desiredPos_list):
        for initPos,desiredPos in zip(initPos_list,desiredPos_list):
            self.addPuzzlePieceObj(   PuzzlePiece(initPos,desiredPos)     )

    def addPuzzlePieceXYrows(self,initdesiredPos_list):
        for initdesiredPos, in initdesiredPos_list:
            self.addPuzzlePieceObj(   PuzzlePiece(initdesiredPos[0:2],initdesiredPos[2:4])     )

    def calcDistI2D(self,idx1,idx2):
        return distance.euclidean(self[idx1].initPos,self[idx2].desiredPos)


    def deletePuzzlePiece(self,idx):
        delete_nth(self.pieces, idx)
        self.num=self.num-1
        
    

        
        

class Solver(object):
    def __init__(self,puzzlepieces=None,useMethod='hungarian'):   
        if isinstance(puzzlepieces, PuzzlePieces):
            self.pieces=puzzlepieces
        else:
            raise ValueError('Expecting an object of type PuzzlePieces.')
        self.makeDistanceMatrix()
            
    def makeDistanceMatrix(self):      
        distMatrix=zeros((self.pieces.num,self.pieces.num))
        for p1 in range(self.pieces.num):
            for p2 in range(self.pieces.num):
                if p2>p1:
                    distMatrix[p1,p2]=self.pieces.calcDistI2D(p1,p2)
                    distMatrix[p2,p1]=distMatrix[p1,p2]
        self.distMatrix=distMatrix+1000*distMatrix.max()*eye(self.pieces.num)
                
    def optimize(self):
        self.ridx,self.cidx=linear_sum_assignment(self.distMatrix)



    # def updateInitial(self,initialPos):
    #     self.initialPos=initialPos

    # def updateDesired(self,desiredPos):
    #     self.desiredPos=desiredPos    
        
    # def updateInitialDesired(self,initialPos,desiredPos):
    #     self.updateInitial(initialPos)
    #     self.updateDesired(desiredPos)
        
    
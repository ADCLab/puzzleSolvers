from collections import deque
from scipy.spatial import distance
from numpy import zeros, eye
from scipy.optimize import linear_sum_assignment
from python_tsp.heuristics import solve_tsp_simulated_annealing, solve_tsp_local_search
from python_tsp.exact import solve_tsp_dynamic_programming




class PuzzlePiece(object):
    def __init__(self,initPos,desiredPos,uid=None):
        self.initPos=initPos
        self.desiredPos=desiredPos
        self.uid=None

class PuzzlePieces(deque):
    def __init__(self):
        self.num=0
        self.uids=deque()
        
    def addPuzzlePieceObj(self,newPiece):
        if isinstance(newPiece, PuzzlePiece):
            if newPiece.uid is None:
                newPiece.uid=self.num+1
            self.append(newPiece)
            self.uids.append(newPiece.uid)
            self.num=self.num+1
        else:
            raise ValueError('Expecting new puzzle piece of type puzzlePiece.')        

    def addPuzzlePieceObjs(self,newPieces):
        if isinstance(newPieces,list):
            for newPiece in newPieces:
                self.addPuzzlePieceObj(newPiece)

    def addPuzzlePieceXY(self,initPos,desiredPos,uid=None):
        self.addPuzzlePieceObj(   PuzzlePiece(initPos,desiredPos,uid)     )
        
    def addPuzzlePieceXYs(self,initPos_list,desiredPos_list, uid_list=None):
        if uid_list is None:
            uid_list=len(initPos_list)*[None]
        for initPos,desiredPos, uid in zip(initPos_list,desiredPos_list, uid_list):
            self.addPuzzlePieceObj(   PuzzlePiece(initPos,desiredPos,uid)     )

    def addPuzzlePieceXYrows(self,initdesiredPos_list):
        for initdesiredPos, in initdesiredPos_list:
            self.addPuzzlePieceObj(   PuzzlePiece(initdesiredPos[0:2],initdesiredPos[2:4])     )

    def calcDistI2D(self,uid1,uid2):
        idx1=self.uids.index(uid1)
        idx2=self.uids.index(uid2)
        return distance.euclidean(self[idx1].initPos,self[idx2].desiredPos)

    def delete_nth(self, n):
        self.rotate(-n)
        self.popleft()
        self.rotate(n)
        self.uids.rotate(-n)
        self.uids.popleft()
        self.uids.rotate(n)

    def deletePuzzlePiece(self,uid):
        self.delete_nth(self.uids.index(uid)  )
        self.num=self.num-1
        
    
def forceList(x):
    if isinstance(x,list):
        return x
    else:
        return [x]
        

class Solver(object):
    def __init__(self,puzzlepieces=None,useMethod='SA'):   
        if isinstance(puzzlepieces, PuzzlePieces):
            self.pieces=puzzlepieces
        else:
            raise ValueError('Expecting an object of type PuzzlePieces.')
        self.useMethods=forceList(useMethod)
        self.makeDistanceMatrix()
        self.lastSolution=None
        self.lastDist=None
        self.__editPieces=False

            
    def makeDistanceMatrix(self):      
        distMatrix=zeros((self.pieces.num,self.pieces.num))
        for p1 in range(self.pieces.num):
            uid1=self.pieces.uids[p1]
            for p2 in range(self.pieces.num):
                uid2=self.pieces.uids[p2]
                if p1!=p2:
                    distMatrix[p1,p2]=self.pieces.calcDistI2D(uid1,uid2)
        self.distMatrix=distMatrix

                
    def optimize(self,overRideMethods=None):
        if overRideMethods is None:
            useMethods=self.useMethods
        else:
            useMethods=forceList(overRideMethods) 
        if self.__editPieces:
            self.makeDistanceMatrix()
        for useMethod in useMethods:
            self.__idxSolution,self.distance=self.lastDist=solveTSP(useMethod,self.distMatrix,self.idxSolution)
        self.__editPieces=False
        self.lastSolution=self.solution
        return self.lastSolution
    
    @property
    def solution(self):
        return [self.pieces[x].uid for x in self.__idxSolution]

    @property
    def idxSolution(self):
        if self.lastSolution is not None:
            return [self.pieces.uids.index(x) for x in self.lastSolution]
        else:
            return None

    def removePiece(self,uid):
        self.pieces.deletePuzzlePiece(uid)
        # idx=self.pieces.uids.index(uid)
        self.lastSolution=[x for x in self.lastSolution if x!=uid]
        self.__idxSolution=self.idxSolution
        self.__editPieces=True

    def removePieces(self,uids):
        for uid in uids:
            self.removePiece(uid)
        self.__editPieces=True



def solveTSP(useMethod,distMatrix,initSolution=None):
    if useMethod=='SA':
        solution,distance = solve_tsp_simulated_annealing(distMatrix, x0=initSolution)
    elif useMethod=='local':
        solution,distance = solve_tsp_local_search(distMatrix, x0=initSolution)
    return solution,distance
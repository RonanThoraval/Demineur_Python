from tkinter import *
import random

class jeu :
    def __init__(self,nbCol=17,nbLigne=17,nbBombes=50) :
        self.nbCol=nbCol
        self.nbLigne=nbLigne
        self.nbBombes=nbBombes
        self.nbDrapeaux=0
        
        self.revelation=[[False for i in range(nbCol)] for j in range(nbLigne)]
        self.grille=[[0 for i in range(nbCol)] for j in range(nbLigne)]
        self.drapeaux=[[False for i in range(nbCol)] for j in range(nbLigne)]
        


    def jeuGagne(self) :
            for i in range(self.nbLigne) :
                for j in range(self.nbCol) :
                    if self.grille[i][j]!=-1 and not(self.revelation[i][j]) or self.grille[i][j]==-1 and not(self.drapeaux[i][j]):
                        return False
            return True



    def PositionsAutour(self,i,j):
        if i>0 and j>0 and i<len(self.grille)-1 and j<len(self.grille[0])-1:
            return[[i-1,j-1],[i-1,j],[i-1,j+1],[i,j+1],[i+1,j+1],[i+1,j],[i+1,j-1],[i,j-1]]
        if i==0 and j==0 :
            return [[1,0],[0,1],[1,1]]
        if i==len(self.grille)-1 and j==0 :
            return [[i-1,j],[i-1,j+1],[i,j+1]]
        if i==0 and j==len(self.grille[0])-1 :
            return [[i,j-1],[i+1,j-1],[i+1,j]]
        if i==len(self.grille)-1 and j==len(self.grille[0])-1 :
            return [[i-1,j],[i-1,j-1],[i,j-1]]
        if i==0 :
            return [[0,j-1],[0,j+1],[1,j-1],[1,j],[1,j+1]]
        if j==0 :
            return [[i-1,0],[i+1,0],[i-1,1],[i,1],[i+1,1]]
        if i==len(self.grille)-1 :
            return [[i,j-1],[i,j+1],[i-1,j-1],[i-1,j],[i-1,j+1]]
        if j==len(self.grille[0])-1 :
            return [[i-1,j],[i+1,j],[i-1,j-1],[i,j-1],[i+1,j-1]]
        else :
            return []

        
    #O vide
    #-1 bombe
    def CreationGrille(self,a,b) :
        l=self.PositionsAutour(a,b)
        for i in range(self.nbBombes) :
            x=random.randint(0,self.nbLigne-1)
            y=random.randint(0,self.nbCol-1)
            while (self.grille[x][y]==-1 or (x==a and y==b) or ([x,y] in l)) :
                x=random.randint(0,self.nbLigne-1)
                y=random.randint(0,self.nbCol-1)
            self.grille[x][y]=-1

        for i in range(self.nbLigne) :
            for j in range(self.nbCol) :
                if self.grille[i][j]!=-1 :
                    self.grille[i][j]=self.compterBombes(i,j)

    def compterBombes(self,i,j) :
        cpt=0
        for m in self.PositionsAutour(i,j):
            if self.grille[m[0]][m[1]]==-1:
                cpt+=1
        return cpt


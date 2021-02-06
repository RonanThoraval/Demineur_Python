import random

#O vide
#-1 bombe
def CreationGrille(grille,nbLignes,nbColonnes,n, a,b) :
    l=PositionsAutour(grille,a,b)
    for i in range(n) :
        x=random.randint(0,nbLignes-1)
        y=random.randint(0,nbColonnes-1)
        while (grille[x][y]==-1 or (x==a and y==b) or ([x,y] in l)) :
            x=random.randint(0,nbLignes-1)
            y=random.randint(0,nbColonnes-1)
        grille[x][y]=-1

    for i in range(nbLignes) :
        for j in range(nbColonnes) :
            if grille[i][j]!=-1 :
                grille[i][j]=compterBombes(grille,i,j)
    return grille

def compterBombes(grille,i,j) :
    cpt=0
    for m in PositionsAutour(grille,i,j):
        if grille[m[0]][m[1]]==-1:
            cpt+=1
    return cpt

def PositionsAutour(grille,i,j):
    if i>0 and j>0 and i<len(grille)-1 and j<len(grille[0])-1:
        return[[i-1,j-1],[i-1,j],[i-1,j+1],[i,j+1],[i+1,j+1],[i+1,j],[i+1,j-1],[i,j-1]]
    if i==0 and j==0 :
        return [[1,0],[0,1],[1,1]]
    if i==len(grille)-1 and j==0 :
        return [[i-1,j],[i-1,j+1],[i,j+1]]
    if i==0 and j==len(grille[0])-1 :
        return [[i,j-1],[i+1,j-1],[i+1,j]]
    if i==len(grille)-1 and j==len(grille[0])-1 :
        return [[i-1,j],[i-1,j-1],[i,j-1]]
    if i==0 :
        return [[0,j-1],[0,j+1],[1,j-1],[1,j],[1,j+1]]
    if j==0 :
        return [[i-1,0],[i+1,0],[i-1,1],[i,1],[i+1,1]]
    if i==len(grille)-1 :
        return [[i,j-1],[i,j+1],[i-1,j-1],[i-1,j],[i-1,j+1]]
    if j==len(grille[0])-1 :
        return [[i-1,j],[i+1,j],[i-1,j-1],[i,j-1],[i+1,j-1]]
    else :
        return []

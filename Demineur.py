from tkinter import *
from gestiondelagriy import *

fenetre=Tk()
fenetre.title("Démineur")
n=15
c=50
can=Canvas(fenetre,width=n*c,height=n*c, bg="grey")

nbBombes=50
grille=CreationGrille(n,n,nbBombes)

for i in range(n) :
    can.create_line(0,i*c,n*c,i*c, fill="black")

for j in range(n) :
    can.create_line(j*c,0,j*c,n*c,fill="black")
    
duchon = PhotoImage(file="duchon.png")
reveillere = PhotoImage(file="reveillere.png")

def fonc1(event) :
    x,y=event.x,event.y
    x=x-x%50
    y=y-y%50
    if grille[y//50][x//50]==-1 :
        can.create_image(x,y, anchor=NW, image=duchon)
    elif grille[y//50][x//50] == 0 :
        can.create_rectangle(x,y,x+50,y+50,fill="light grey")
    else :
        can.create_text(x+25,y+25,text=grille[y//50][x//50],fill="blue")

def fonc2(event) :
    x,y=event.x,event.y
    x=x-x%50
    y=y-y%50
    can.create_image(x,y, anchor=NW, image=reveillere)
       
can.bind("<Button-1>", fonc1)
can.bind("<Button-3>",fonc2)
can.pack()
chaine = Label(fenetre)
chaine.pack()























































































"""
for i in range(n) :
    for j in range(n) :
        if grille[i][j]==-1 :
            can.create_image(j*50,i*50,anchor=NW,image=duchon)
        else :
            can.create_text(j*50+25,i*50+25,text=grille[i][j],fill="blue")
    """ 

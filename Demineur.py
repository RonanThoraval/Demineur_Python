from tkinter import *
from gestiondelagriy import *

def start():
    
    def jeu(nbBombes,nbCol,nbLigne):
        fenetre=Tk()
        fenetre.title("Démineur")
        StatusBar=70
        c=50
        bombe=PhotoImage(file="bombe.png")
        drapeau=PhotoImage(file="drap.png")
        nbdrapeaux=[0]

        couleurs=["blue","green","red","purple","yellow","orange","white","brown"]
        couleursTexte=["red","black"]

        can=Canvas(fenetre,width=nbCol*c,height=nbLigne*c+StatusBar, bg="dark grey")



        can.create_rectangle(0,nbLigne*c,nbCol*c,nbLigne*c+StatusBar,fill="grey")

        can.create_image(c,nbLigne*c+StatusBar/2, anchor=CENTER, image=drapeau)
        can.create_text(c+StatusBar,nbLigne*c+StatusBar/2,text=str(nbdrapeaux[0])+"/"+str(nbBombes),fill="black",font=("Arial",20))
        can.create_rectangle(nbCol*c-3*c+3,nbLigne*c+3,nbCol*c-3,nbLigne*c+StatusBar-3,fill="yellow")
        can.create_text(nbCol*c-1.5*c,nbLigne*c+StatusBar/2,text="Nouvelle Partie")

        grille=[[0 for i in range(nbCol)] for j in range(nbLigne)]
        estLePremierMouv=[True]

        revelation=[ [False for i in range(nbCol)] for j in range(nbLigne)]
        drapeaux=[[False for i in range(nbCol)] for j in range(nbLigne)]

        for i in range(nbLigne) :
            can.create_line(0,i*c,nbCol*c,i*c, fill="black")

        for j in range(nbCol) :
            can.create_line(j*c,0,j*c,nbLigne*c,fill="black")
            
        def revelerCasesAutour(grille,y,x) :
            l=PositionsAutour(grille,y,x)
            for m in l :
                if grille[m[0]][m[1]]== 0 and revelation[m[0]][m[1]]==False :
                    revelation[m[0]][m[1]]=True
                    can.create_rectangle(m[1]*50,m[0]*50,m[1]*50+50,m[0]*50+50,fill="light grey")
                    revelerCasesAutour(grille,m[0],m[1])
                elif revelation[m[0]][m[1]]==False :
                    revelation[m[0]][m[1]]=True
                    can.create_rectangle(m[1]*50,m[0]*50,m[1]*50+50,m[0]*50+50,fill="light grey")
                    can.create_text(m[1]*50+25,m[0]*50+25,text=grille[m[0]][m[1]],fill=couleurs[grille[m[0]][m[1]]-1],font=("Arial",20))

        def jeuGagne() :
            for i in range(nbLigne) :
                for j in range(nbCol) :
                    if grille[i][j]!=-1 and not(revelation[i][j]) or grille[i][j]==-1 and not(drapeaux[i][j]):
                        return False
            return True

                
        def fonc1(event) :
            x,y=event.x,event.y
            x=x-x%50
            y=y-y%50
            #Nouvelle Partie
            if (x>=nbCol*c-3*c and y>=nbLigne*c ) :
                fenetre.destroy()
                start()
                return
            
            #Sur la status bar
            if y>=nbLigne*c :
                return 
            #Premier clic : définition de la grille de jeu
            if(estLePremierMouv[0]):
                estLePremierMouv[0]=False
                CreationGrille(grille,nbLigne,nbCol,nbBombes,y//50,x/50)
            if(not (revelation[y//50][x//50] or drapeaux[y//50][x//50])):
                revelation[y//50][x//50]=True
                if grille[y//50][x//50]==-1 :
                    montrerLesBombes()
                    perdu=Tk()
                    perducan=Canvas(perdu,width=500,height=500, bg="pink")
                    perducan.create_text(250,250,text="Perdu",font=("Arial",50),fill="white")
                    perducan.pack()
                elif grille[y//50][x//50] == 0 :
                    revelerCasesAutour(grille,y//50,x//50)
                    can.create_rectangle(x,y,x+50,y+50,fill="light grey")
                    if jeuGagne() :
                        gagne=Tk()
                        gagnecan=Canvas(gagne,width=500,height=500, bg="pink")
                        gagnecan.create_text(250,250,text="Gagné",font=("Arial",50),fill="white")
                        gagnecan.pack()
                    
                else :
                    can.create_rectangle(x,y,x+50,y+50,fill="light grey")
                    can.create_text(x+25,y+25,text=grille[y//50][x//50],fill=couleurs[grille[y//50][x//50]-1],font=("Arial",20))
                    if jeuGagne() :
                        gagne=Tk()
                        gagnecan=Canvas(gagne,width=500,height=500, bg="pink")
                        gagnecan.create_text(250,250,text="Gagné",font=("Arial",50),fill="white")
                        gagnecan.pack()



        
        def fonc3(event) :
            x,y=event.x,event.y
            x=x-x%50
            y=y-y%50
            if revelation[y//50][x//50]==False :
                if drapeaux[y//50][x//50]==True :
                    drapeaux[y//50][x//50]=False
                    can.create_rectangle(x,y,x+50,y+50,fill="dark grey")
                    nbdrapeaux[0]-=1
                    can.create_rectangle(0,nbLigne*c,nbCol*c,nbLigne*c+StatusBar,fill="grey")
                    can.create_image(c,nbLigne*c+StatusBar/2, anchor=CENTER, image=drapeau)
                    can.create_text(c+StatusBar,nbLigne*c+StatusBar/2,text=str(nbdrapeaux[0])+"/"+str(nbBombes),fill=couleursTexte[nbdrapeaux[0]<=nbBombes],font=("Arial",20))
                    can.create_rectangle(nbCol*c-3*c+3,nbLigne*c+3,nbCol*c-3,nbLigne*c+StatusBar-3,fill="yellow")
                    can.create_text(nbCol*c-1.5*c,nbLigne*c+StatusBar/2,text="Nouvelle Partie")
                else :
                    drapeaux[y//50][x//50]=True
                    nbdrapeaux[0]+=1
                    can.create_rectangle(0,nbLigne*c,nbCol*c,nbLigne*c+StatusBar,fill="grey")
                    can.create_image(c,nbLigne*c+StatusBar/2, anchor=CENTER, image=drapeau)
                    can.create_text(c+StatusBar,nbLigne*c+StatusBar/2,text=str(nbdrapeaux[0])+"/"+str(nbBombes),fill=couleursTexte[nbdrapeaux[0]<=nbBombes],font=("Arial",20))
                    can.create_image(x,y,anchor=NW,image=drapeau)
                    can.create_rectangle(nbCol*c-3*c+3,nbLigne*c+3,nbCol*c-3,nbLigne*c+StatusBar-3,fill="yellow")
                    can.create_text(nbCol*c-1.5*c,nbLigne*c+StatusBar/2,text="Nouvelle Partie")
                    if jeuGagne() :
                        gagne=Tk()
                        gagnecan=Canvas(gagne,width=500,height=500, bg="pink")
                        gagnecan.create_text(250,250,text="Gagné",font=("Arial",50),fill="white")
                        gagnecan.pack()

        def montrerLesBombes():
            for i in range(nbLigne):
                for j in range(nbCol):
                    if grille[i][j]==-1:
                        can.create_rectangle(j*50,i*50,j*50+50,i*50+50,fill="red")
                        can.create_image(j*50+3,i*50+3, anchor=NW, image=bombe)
                
               
        can.bind("<Button-1>",fonc1)
        can.bind("<Button-3>",fonc3)

        can.pack()
    """
    choix=Tk()
    canchoix=Canvas(choix,width=400,height=150, bg="dark grey")
    canchoix.create_text(200,50,text="Quel est le nombre de bombes ?",font=("Arial",20))
    canchoix.create_line(75,75,325,75,fill="black")
    canchoix.create_line(75,110,325,110,fill="black")
    for i in range(10):
        canchoix.create_line(75+i*(250/9),75,75+i*(250/9),110,fill="black")
        if(i!=0):
            canchoix.create_text(75+i*(250/9)-(250/18),97.5,text=i)
    canchoix.create_rectangle(375,125,400,150,fill="yellow")
    canchoix.create_text(387.5,137.5,text="ok")
    canchoix.pack()


    
    def fonc(event):
        canchoix.create_rectangle(0,0,400,150,fill="yellow")
        canchoix.create_text(200,50,text="Quel est le nombre de bombes ?",font=("Arial",20))
        canchoix.create_line(50,75,350,75,fill="black")
        canchoix.create_line(50,110,350,110,fill="black")
        for i in range(11):
            canchoix.create_line(50+i*(250/9),75,50+i*(250/9),110,fill="black")
            print(75+i*(250/9))
        x,y=event.x,event.y
        if(x<325 and x>75 and y<110 and y>75):
            for i in range(10):
                if(x<75+(i+1)*250/9):
                    return i+1
        return -1
        
    canchoix.bind("<Button-1>",fonc)
    """
    
    print("Quel est le nombre de bombes ?")
    nbBombes=int(input())
    #canchoix.create_text(200,100,text=nbBombes,font=("Arial",20))
    print("Quel est le nombre de colonnes ?")
    nbCol=int(input())
    print("Quel est le nombre de lignes ?")
    nbLignes=int(input())
    jeu(nbBombes,nbCol,nbLignes)
    
start()

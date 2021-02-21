from tkinter import *
from Game import *


class GameEngine :

    def __init__(self,jeu) :
        
        self.jeu=jeu
        self.fenetre=Tk()
        self.fenetre.title("Démineur")
        self.StatusBar=70
        self.c=50
        self.bombe=PhotoImage(file="bombe.png")
        self.drapeau=PhotoImage(file="drap.png")
        self.estLePremierMouv=True

        self.couleurs=["blue","green","red","purple","yellow","orange","white","brown"]
        self.couleursTexte=["red","black"]
        self.can=Canvas(self.fenetre,width=self.jeu.nbCol*self.c,height=self.jeu.nbLigne*self.c+self.StatusBar, bg="dark grey")

        self.can.create_rectangle(0,self.jeu.nbLigne*self.c,self.jeu.nbCol*self.c,self.jeu.nbLigne*self.c+self.StatusBar,fill="grey")
        self.can.create_image(self.c,self.jeu.nbLigne*self.c+self.StatusBar/2, anchor=CENTER, image=self.drapeau)
        self.can.create_text(2*self.c,self.jeu.nbLigne*self.c+self.StatusBar/2,text=str(self.jeu.nbDrapeaux)+"/"+str(self.jeu.nbBombes),fill="black",font=("Arial",15))
        self.can.create_rectangle(self.jeu.nbCol*self.c*(1/3)+1,self.jeu.nbLigne*self.c+3,self.jeu.nbCol*self.c*(2/3)-1,self.jeu.nbLigne*self.c+self.StatusBar-3,fill="light sea green")
        self.can.create_rectangle(self.jeu.nbCol*self.c*(2/3)+1,self.jeu.nbLigne*self.c+3,self.jeu.nbCol*self.c-1,self.jeu.nbLigne*self.c+self.StatusBar-3,fill="HotPink3")
        self.can.create_text(self.jeu.nbCol*self.c//2,self.jeu.nbLigne*self.c+self.StatusBar/2,text="Changer de diffilculté",font=("Arial",10))
        self.can.create_text(self.jeu.nbCol*self.c*(5/6),self.jeu.nbLigne*self.c+self.StatusBar/2,text="Nouvelle Partie",font=("Arial",10))
        
        for i in range(self.jeu.nbLigne) :
            self.can.create_line(0,i*self.c,self.jeu.nbCol*self.c,i*self.c, fill="black")

        for j in range(self.jeu.nbCol) :
            self.can.create_line(j*self.c,0,j*self.c,self.jeu.nbLigne*self.c,fill="black")
        self.can.pack()
        self.can.bind("<Button-1>",self.fonc1)
        self.can.bind("<Button-3>",self.fonc3)
        self.fenetre.mainloop()


    

       
    def montrerLesBombes(self):
            for i in range(self.jeu.nbLigne):
                for j in range(self.jeu.nbCol):
                    if self.jeu.grille[i][j]==-1:
                        self.can.create_rectangle(j*50,i*50,j*50+50,i*50+50,fill="red")
                        self.can.create_image(j*50+3,i*50+3, anchor=NW, image=self.bombe)
                        
    def revelerCasesAutour(self,y,x) :
                l=self.jeu.PositionsAutour(y,x)
                for m in l :
                    if self.jeu.grille[m[0]][m[1]]== 0 and self.jeu.revelation[m[0]][m[1]]==False :
                        self.jeu.revelation[m[0]][m[1]]=True
                        self.can.create_rectangle(m[1]*50,m[0]*50,m[1]*50+50,m[0]*50+50,fill="light grey")
                        self.revelerCasesAutour(m[0],m[1])
                    elif self.jeu.revelation[m[0]][m[1]]==False :
                        self.jeu.revelation[m[0]][m[1]]=True
                        self.can.create_rectangle(m[1]*50,m[0]*50,m[1]*50+50,m[0]*50+50,fill="light grey")
                        self.can.create_text(m[1]*50+25,m[0]*50+25,text=self.jeu.grille[m[0]][m[1]],fill=self.couleurs[self.jeu.grille[m[0]][m[1]]-1],font=("Arial",20))

    


    

    def fonc1(self,event) :                
            x,y=event.x,event.y
            
            #Nouvelle Partie
            if (x>=self.jeu.nbCol*self.c*(2/3)+1 and y>=self.jeu.nbLigne*self.c ) :
                self.fenetre.destroy()
                j=jeu(self.jeu.nbCol,self.jeu.nbLigne,self.jeu.nbBombes)
                GameEngine(j)
                return
            #Changer de difficulté
            if(y>=self.jeu.nbLigne*self.c and x>=self.jeu.nbCol*self.c*(1/3)+1 and x<=self.jeu.nbCol*self.c*(2/3)-1):
                self.fenetre.destroy()
                start()
                return
            #Sur la status bar
            if y>=self.jeu.nbLigne*self.c :
                return
            x=x-x%50
            y=y-y%50
            #Premier clic : définition de la self.jeu.grille de jeu
            if(self.estLePremierMouv):
                self.estLePremierMouv=False
                self.jeu.CreationGrille(y//50,x/50)
            if(not (self.jeu.revelation[y//50][x//50] or self.jeu.drapeaux[y//50][x//50])):
                self.jeu.revelation[y//50][x//50]=True
                if self.jeu.grille[y//50][x//50]==-1 :
                    self.montrerLesBombes()
                    perdu=Tk()
                    perducan=Canvas(perdu,width=500,height=500, bg="pink")
                    perducan.create_text(250,250,text="Perdu",font=("Arial",50),fill="white")
                    perducan.pack()
                    perdu.mainloop()
                elif self.jeu.grille[y//50][x//50] == 0 :
                    self.revelerCasesAutour(y//50,x//50)
                    self.can.create_rectangle(x,y,x+50,y+50,fill="light grey")
                    if self.jeu.jeuGagne() :
                        gagne=Tk()
                        gagnecan=Canvas(gagne,width=500,height=500, bg="pink")
                        gagnecan.create_text(250,250,text="Gagné",font=("Arial",50),fill="white")
                        gagnecan.pack()
                        gagne.mainloop()
                    
                else :
                    self.can.create_rectangle(x,y,x+50,y+50,fill="light grey")
                    self.can.create_text(x+25,y+25,text=self.jeu.grille[y//50][x//50],fill=self.couleurs[self.jeu.grille[y//50][x//50]-1],font=("Arial",20))
                    if self.jeu.jeuGagne() :
                        gagne=Tk()
                        gagnecan=Canvas(gagne,width=500,height=500, bg="pink")
                        gagnecan.create_text(250,250,text="Gagné",font=("Arial",50),fill="white")
                        gagnecan.pack()
                        gagne.mainloop()



      
    def fonc3(self,event) :
        x,y=event.x,event.y
        x=x-x%50
        y=y-y%50
        if self.jeu.revelation[y//50][x//50]==False :
            if self.jeu.drapeaux[y//50][x//50]==True :
                self.jeu.drapeaux[y//50][x//50]=False
                self.can.create_rectangle(x,y,x+50,y+50,fill="dark grey")
                self.jeu.nbDrapeaux-=1
                self.can.create_rectangle(0,self.jeu.nbLigne*self.c,self.jeu.nbCol*self.c,self.jeu.nbLigne*self.c+self.StatusBar,fill="grey")
                self.can.create_image(self.c,self.jeu.nbLigne*self.c+self.StatusBar/2, anchor=CENTER, image=self.drapeau)
                self.can.create_text(2*self.c,self.jeu.nbLigne*self.c+self.StatusBar/2,text=str(self.jeu.nbDrapeaux)+"/"+str(self.jeu.nbBombes),fill="black",font=("Arial",15))
                self.can.create_rectangle(self.jeu.nbCol*self.c*(1/3)+2,self.jeu.nbLigne*self.c+3,self.jeu.nbCol*self.c*(2/3)-2,self.jeu.nbLigne*self.c+self.StatusBar-3,fill="light sea green")
                self.can.create_rectangle(self.jeu.nbCol*self.c*(2/3)+2,self.jeu.nbLigne*self.c+3,self.jeu.nbCol*self.c-2,self.jeu.nbLigne*self.c+self.StatusBar-3,fill="HotPink3")
                self.can.create_text(self.jeu.nbCol*self.c//2,self.jeu.nbLigne*self.c+self.StatusBar/2,text="Changer de diffilculté",font=("Arial",10))
                self.can.create_text(self.jeu.nbCol*self.c*(5/6),self.jeu.nbLigne*self.c+self.StatusBar/2,text="Nouvelle Partie",font=("Arial",10))
            else :
                self.jeu.drapeaux[y//50][x//50]=True
                self.jeu.nbDrapeaux+=1
                self.can.create_rectangle(0,self.jeu.nbLigne*self.c,self.jeu.nbCol*self.c,self.jeu.nbLigne*self.c+self.StatusBar,fill="grey")
                self.can.create_image(self.c,self.jeu.nbLigne*self.c+self.StatusBar/2, anchor=CENTER, image=self.drapeau)
                self.can.create_text(2*self.c,self.jeu.nbLigne*self.c+self.StatusBar/2,text=str(self.jeu.nbDrapeaux)+"/"+str(self.jeu.nbBombes),fill="black",font=("Arial",15))
                self.can.create_rectangle(self.jeu.nbCol*self.c*(1/3)+2,self.jeu.nbLigne*self.c+3,self.jeu.nbCol*self.c*(2/3)-2,self.jeu.nbLigne*self.c+self.StatusBar-3,fill="light sea green")
                self.can.create_rectangle(self.jeu.nbCol*self.c*(2/3)+2,self.jeu.nbLigne*self.c+3,self.jeu.nbCol*self.c-2,self.jeu.nbLigne*self.c+self.StatusBar-3,fill="HotPink3")
                self.can.create_text(self.jeu.nbCol*self.c//2,self.jeu.nbLigne*self.c+self.StatusBar/2,text="Changer de diffilculté",font=("Arial",10))
                self.can.create_text(self.jeu.nbCol*self.c*(5/6),self.jeu.nbLigne*self.c+self.StatusBar/2,text="Nouvelle Partie",font=("Arial",10))
                self.can.create_image(x,y,anchor=NW,image=self.drapeau)
                
                if self.jeu.jeuGagne() :
                    gagne=Tk()
                    gagnecan=Canvas(gagne,width=500,height=500, bg="pink")
                    gagnecan.create_text(250,250,text="Gagné",font=("Arial",50),fill="white")
                    gagnecan.pack()
                    gagne.mainloop()

############################
                    


class start:
    def __init__(self) :
        
        self.choix=Tk()
        self.choix.title("Menu des tailles")
        self.canchoix=Canvas(self.choix,width=800,height=800, bg="black")
        self.canchoix.create_rectangle(5,5,397,397,fill="white")
        self.canchoix.create_rectangle(402,5,795,397,fill="dark grey")
        self.canchoix.create_rectangle(5,402,397,795,fill="grey20")
        self.canchoix.create_rectangle(402,402,795,795,fill="pink")
        self.canchoix.create_text(200,200,fill="black",text="Facile : 8x8",font=("Arial",25))
        self.canchoix.create_text(600,200,fill="grey35",text="Moyen : 13x13",font=("Arial",25))
        self.canchoix.create_text(200,600,fill="white",text="Difficile : 17x17",font=("Arial",25))
        self.canchoix.create_text(600,600,fill="dark slate blue",text="Jeu personnalisable",font=("Arial",25))
        
        self.canchoix.pack()
        
        self.canchoix.bind("<Button-1>",self.fonc)
    
        
        self.choix.mainloop()
        
    def f(self) :
        tab=[]

        def isDigit(c):
            return c in ["1","2","3","4","5","6","7","8","9","0"]

        
        ###Perso1###
        perso1=Tk()
        canPerso1=Label(perso1,text="Paramètres")
        canPerso1.grid(row=0, columnspan=2, pady=8)
        
        def g1(event) :
            tab.append(int(rep1.get()))
            perso1.destroy()
            h()

            
        lbl_reponse = Label(perso1, text="Nombre de Lignes : ")
        lbl_reponse.grid(row=1, column=0, pady=5, padx=5)

        rep1=Entry(perso1)
        rep1.grid(row=1, column=1, pady=5, padx=5)
        rep1.bind("<Return>", g1)





        ###Perso2##
        def h():
            perso2=Tk()
            canPerso2=Label(perso2,text="Paramètres")
            canPerso2.grid(row=0, columnspan=2, pady=8)

            def g2(event) :
                tab.append(int(rep2.get()))
                perso2.destroy()
                i()


            lbl_reponse = Label(perso2, text="Nombre de Colonnes : ")
            lbl_reponse.grid(row=1, column=0, pady=5, padx=5)
                
            rep2=Entry(perso2)
            rep2.grid(row=1, column=1, pady=5, padx=5)
            rep2.bind("<Return>", g2)



        ###Perso3###
        def i():
            perso3=Tk()
            canPerso3=Label(perso3,text="Paramètres")
            canPerso3.grid(row=0, columnspan=2, pady=8)

            def g3(event) :
                tab.append(int(rep3.get()))
                perso3.destroy()
                self.choix.destroy()
                GameEngine(jeu(tab[0],tab[1],tab[2]))


            lbl_reponse = Label(perso3, text="Nombre de Bombes : ")
            lbl_reponse.grid(row=1, column=0, pady=5, padx=5)
            

            rep3=Entry(perso3)
            rep3.grid(row=1, column=1, pady=5, padx=5)
            rep3.bind("<Return>", g3)



            
        

       

        

    def fonc(self,event):
            
        x = event.x
        y = event.y
        if (x>=402 and y>=402 and x<=795 and y<=795) :
            self.f()
        else :
            if (x<=397 and y <=397 and x>=5 and y>=5 ) :
                j=jeu(8,8,10)
            elif (x>=402 and x<=795 and y>=5 and y<=397) :
                j=jeu(13,13,40)
            elif (x>=5 and x<=397 and y>=402 and y<=795) :
                j=jeu(17,17,75)
            self.choix.destroy()
            GameEngine(j)
        return
        
        

    
start()

######################################################################################################
######################################################################################################



    

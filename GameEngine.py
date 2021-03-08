from tkinter import *
from Game import *
from time import time


class GameEngine :

    def __init__(self,game) :
        
        self.game=game
        self.window=Tk()
        self.window.title("Démineur")
        self.width=800
        self.height=800
        self.StatusBar=70
        self.c=self.height//max(self.game.nbRows,self.game.nbCols)
        self.bomb=PhotoImage(file="bombe.png")
        self.flag=PhotoImage(file="drap.png")
        self.flagBar=PhotoImage(file="drap.png")
        self.isFirstMove=True
        self.isOver=False

        self.colors=["blue","green","red","purple","yellow","orange","white","brown"]
        self.textColors=["black","red"]
        self.can=Canvas(self.window,width=self.width,height=self.height+self.StatusBar, bg="dark grey")
        self.can.bind("<Button-1>",self.fonc1)
        self.can.bind("<Button-3>",self.fonc3)
        self.can.pack()
        

        for i in range(self.game.nbRows) :
            self.can.create_line(0,i*self.c,self.game.nbCols*self.c,i*self.c, fill="black")

        for j in range(self.game.nbCols) :
            self.can.create_line(j*self.c,0,j*self.c,self.game.nbRows*self.c,fill="black")

        ##StatusBar
        self.can.create_rectangle(0,self.game.nbRows*self.c,self.game.nbCols*self.c,self.game.nbRows*self.c+self.StatusBar,fill="grey")
        self.can.create_image(10,810, anchor=NW, image=self.flagBar)
        self.flagsLabel = Label(self.window, bg="grey", fg=self.textColors[self.game.nbFlags>self.game.nbBombs],text=str(self.game.nbFlags)+"/"+str(self.game.nbBombs),font=("Times",20))
        self.flagsLabel.place(x=90,y=self.c*self.game.nbRows+self.StatusBar//2+5, anchor=CENTER)
        self.can.create_rectangle(self.game.nbCols*self.c*(1/3)+2,self.game.nbRows*self.c+3,self.game.nbCols*self.c*(2/3)-2,self.game.nbRows*self.c+self.StatusBar-3,fill="light sea green")
        self.can.create_rectangle(self.game.nbCols*self.c*(2/3)+2,self.game.nbRows*self.c+3,self.game.nbCols*self.c-2,self.game.nbRows*self.c+self.StatusBar-3,fill="HotPink3")
        self.can.create_text(self.game.nbCols*self.c//2,self.game.nbRows*self.c+self.StatusBar/2+5,text="Changer de diffilculté",font=("Times",15))
        self.can.create_text(self.game.nbCols*self.c*(5/6),self.game.nbRows*self.c+self.StatusBar/2+5,text="Nouvelle Partie",font=("Times",15))

        
        ### Timer
        self.clock_label = Label(self.window, bg="grey", fg="black", font = ("Times", 20))
        self.clock_label.place(x = 200, y = self.c*self.game.nbRows+self.StatusBar//2+5, anchor=CENTER)
        self.start_time=time()
        self.update_timer()

        #Resizing flag and bomb image in function of game size
        self.flag=self.flag.zoom(self.c,self.c)
        self.flag=self.flag.subsample(50,50)
        self.bomb=self.bomb.zoom(self.c,self.c)
        self.bomb=self.bomb.subsample(50,50)
        
        
        self.window.mainloop()

        
        
    def update_timer(self):
        if self.isOver :
            return
        delta=int(time()-self.start_time)
        time_string='{:02}:{:02}'.format(*divmod(delta, 60))
        self.clock_label.configure(text=time_string)
        self.clock_label.after(1000, self.update_timer)

    def restart(self,end) :
        end.destroy()
        self.window.destroy()
        start()
    
    def EndGame(self,status) :
        self.isOver=True
        end=Tk()
        end.title("END")
        ending=Canvas(end,width=200,height=200, bg="pink")
        ending.create_text(100,100,text=status,font=("Arial",20),fill="black")
        ending.pack()
        end.mainloop()
       
    def showBombs(self):
            for i in range(self.game.nbRows):
                for j in range(self.game.nbCols):
                    if self.game.grille[i][j]==-1:
                        self.can.create_rectangle(j*self.c,i*self.c,j*self.c+self.c,i*self.c+self.c,fill="red")
                        self.can.create_image(j*self.c+3,i*self.c+3, anchor=NW, image=self.bomb)
                        
    def revealCasesAround(self,y,x) :
                l=self.game.PositionsAutour(y,x)
                for m in l :
                    if self.game.grille[m[0]][m[1]]== 0 and self.game.revelation[m[0]][m[1]]==False :
                        self.game.revelation[m[0]][m[1]]=True
                        self.can.create_rectangle(m[1]*self.c,m[0]*self.c,m[1]*self.c+self.c,m[0]*self.c+self.c,fill="light grey")
                        self.revealCasesAround(m[0],m[1])
                    elif self.game.revelation[m[0]][m[1]]==False :
                        self.game.revelation[m[0]][m[1]]=True
                        self.can.create_rectangle(m[1]*self.c,m[0]*self.c,m[1]*self.c+self.c,m[0]*self.c+self.c,fill="light grey")
                        self.can.create_text(m[1]*self.c+self.c/2,m[0]*self.c+self.c/2,text=self.game.grille[m[0]][m[1]],fill=self.colors[self.game.grille[m[0]][m[1]]-1],font=("Arial",(2*self.c)//5))

    


    
    #Clic gauche
    def fonc1(self,event) :
            x,y=event.x,event.y
            
            #Nouvelle Partie
            if (x>=self.game.nbCols*self.c*(2/3)+1 and y>=self.game.nbRows*self.c ) :
                self.window.destroy()
                j=game(self.game.nbCols,self.game.nbRows,self.game.nbBombs)
                GameEngine(j)
                return
            #Changer de difficulté
            if(y>=self.game.nbRows*self.c and x>=self.game.nbCols*self.c*(1/3)+1 and x<=self.game.nbCols*self.c*(2/3)-1):
                self.window.destroy()
                start()
                return
            #Sur la status bar
            if y>=self.game.nbRows*self.c :
                return

            if (self.isOver) :
                return
            
            x=x-x%self.c
            y=y-y%self.c
            #Premier clic : définition de la grille de game
            if(self.isFirstMove):
                self.isFirstMove=False
                self.game.CreationGrille(y//self.c,x//self.c)
            if(not (self.game.revelation[y//self.c][x//self.c] or self.game.flags[y//self.c][x//self.c])):
                self.game.revelation[y//self.c][x//self.c]=True
                if self.game.grille[y//self.c][x//self.c]==-1 :
                    self.showBombs()
                    self.EndGame("Perdu")
                elif self.game.grille[y//self.c][x//self.c] == 0 :
                    self.revealCasesAround(y//self.c,x//self.c)
                    self.can.create_rectangle(x,y,x+self.c,y+self.c,fill="light grey")
                    if self.game.hasWon() :
                        self.EndGame("Gagné")
                    
                else :
                    self.can.create_rectangle(x,y,x+self.c,y+self.c,fill="light grey")
                    self.can.create_text(x+self.c/2,y+self.c/2,text=self.game.grille[y//self.c][x//self.c],fill=self.colors[self.game.grille[y//self.c][x//self.c]-1],font=("Arial",(self.c*2)//5))
                    if self.game.hasWon() :
                        self.EndGame("Gagné")



    #Clic droit 
    def fonc3(self,event) :
        if self.isOver :
            return
        x,y=event.x,event.y
        x=x-x%self.c
        y=y-y%self.c
        if self.game.revelation[y//self.c][x//self.c]==False :
            if self.game.flags[y//self.c][x//self.c]==True :
                self.game.flags[y//self.c][x//self.c]=False
                self.can.create_rectangle(x,y,x+self.c,y+self.c,fill="dark grey") #remove flag
                self.game.nbFlags-=1
                self.flagsLabel.configure(text=str(self.game.nbFlags)+"/"+str(self.game.nbBombs),fg=self.textColors[self.game.nbFlags>self.game.nbBombs]) #update Status Bar
            else :
                self.game.flags[y//self.c][x//self.c]=True
                self.game.nbFlags+=1
                self.flagsLabel.configure(text=str(self.game.nbFlags)+"/"+str(self.game.nbBombs),fg=self.textColors[self.game.nbFlags>self.game.nbBombs]) #update Status Bar
                self.can.create_image(x+self.c//2,y+self.c//2,anchor=CENTER,image=self.flag) #display flag
                
                if self.game.hasWon() :
                    self.EndGame("Gagné")


############################
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
        perso1.title("Choix du nombre de lignes")
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
            perso2.title("Choix du nombre de colonnes")
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
            perso3.title("Choix du nombre de bombes")
            canPerso3=Label(perso3,text="Paramètres")
            canPerso3.grid(row=0, columnspan=2, pady=8)

            def g3(event) :
                tab.append(int(rep3.get()))
                perso3.destroy()
                self.choix.destroy()
                GameEngine(game(tab[0],tab[1],tab[2]))


            lbl_reponse = Label(perso3, text="Nombre de bombs : ")
            lbl_reponse.grid(row=1, column=0, pady=5, padx=5)
            

            rep3=Entry(perso3)
            rep3.grid(row=1, column=1, pady=5, padx=5)
            rep3.bind("<Return>", g3)
            
    #Clic gauche
    def fonc(self,event):
            
        x = event.x
        y = event.y
        if (x>=402 and y>=402 and x<=795 and y<=795) :
            self.f()
        else :
            if (x<=397 and y <=397 and x>=5 and y>=5 ) :
                j=game(8,8,10)
            elif (x>=402 and x<=795 and y>=5 and y<=397) :
                j=game(13,13,30)
            elif (x>=5 and x<=397 and y>=402 and y<=795) :
                j=game(17,17,60)
            self.choix.destroy()
            GameEngine(j)
        return
        
        

    
start()

######################################################################################################
######################################################################################################



    

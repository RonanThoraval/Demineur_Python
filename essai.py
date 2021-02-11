from random import randint
import tkinter as tk

app = tk.Tk()
titre = tk.Label(app, text="Devine le nombre auquel je pense", font=("", 16))
titre.grid(row=0, columnspan=2, pady=8)

nombre_secret = randint(0, 100) + 1

lbl_reponse = tk.Label(app, text="Choisi un nombre entre 1 et 100 inclus:")
lbl_reponse.grid(row=1, column=0, pady=5, padx=5)

reponse = tk.Entry(app)
reponse.grid(row=1, column=1, pady=5, padx=5)

def nombre_choisi(event):
    "Callback quand le joueur a entré un nombre."
    nbre_choisi = int(reponse.get())
    if nombre_secret > nbre_choisi:
        print("Non")
    elif nombre_secret < nbre_choisi:
        print("Non plus")
    else:
        print("Oui")

reponse.bind("<Return>", nombre_choisi)

app.mainloop()

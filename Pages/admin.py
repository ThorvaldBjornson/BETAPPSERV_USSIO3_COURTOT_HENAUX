from tkinter import *

window = Tk()

window.title("BetApp")
window.geometry("1280x720")
window.minsize(480,360)


#Logo
window.iconbitmap("logo.ico")
window.config(background="#87CEFA")

#Mise en place de la Frame
frame = Frame(window, bg="#87CEFA", bd=1)


#Initialisation des titre
label_title = Label(frame, text="BetApp", font=("Arial", 40), bg="#87CEFA", fg="white")
label_title.grid(row=0, column=3)

label_Rencontre = Label(frame, text="Rencontre", font=("Arial", 20), bg="#87CEFA", fg="white")
label_Rencontre.grid(row=2, column=1)

label_Ajout_Rencontre = Label(frame, text="Ajouter Une Rencontre", font=("Arial", 20), bg="#87CEFA", fg="white")
label_Ajout_Rencontre.grid(row=2, column=5)

label_Vainqueur = Label(frame, text="Choisir un Vainqueur", font=("Arial", 20), bg="#87CEFA", fg="white")
label_Vainqueur.grid(row=12, column=5)

#Récuperation identité
User = "Admin"

label_User = Label(frame, text=User, font=("Arial", 15), bg="#87CEFA", fg="white")
label_User.grid(row=0, column=0, sticky=W)

## Rencontre

#feed + affichage des rencontres
rencontre = ['Rencontre1', 'Rencontre2', 'Rencontre3']
for i in range(len(rencontre)):
    label_Rencontre = Label(frame, text=rencontre[i], font=("Arial", 15), bg="#87CEFA", fg="white")
    label_Rencontre.grid(row=i+3, column=0, sticky=W)
    log_button = Button(frame, text="Annuler", font=("Arial", 15), bg="white", fg="#87CEFA")
    log_button.grid(row=i+3, column=1)


## Ajout d'une rencontre
#Nom rencontre
label_Nom_Rencontre = Label(frame, text="Nom de la Rencontre :", font=("Arial", 15), bg="#87CEFA", fg="white")
label_Nom_Rencontre.grid(row=3, column=4)
entry_Nom_Rencontre = Entry(frame, font=("Arial", 15), bg="#87CEFA", fg="white")
entry_Nom_Rencontre.grid(row=4, column=4)

#Date Rencontre
label_Date_Rencontre = Label(frame, text="Date de la Rencontre :", font=("Arial", 15), bg="#87CEFA", fg="white")
label_Date_Rencontre.grid(row=5, column=4)
entry_Date_Rencontre = Entry(frame, font=("Arial", 15), bg="#87CEFA", fg="white")
entry_Date_Rencontre.grid(row=6, column=4)

#Lieu Rencontre
label_Nom_Rencontre = Label(frame, text="Lieux de la Rencontre :", font=("Arial", 15), bg="#87CEFA", fg="white")
label_Nom_Rencontre.grid(row=7, column=4)
entry_Nom_Rencontre = Entry(frame, font=("Arial", 15), bg="#87CEFA", fg="white")
entry_Nom_Rencontre.grid(row=8, column=4)

#Challenger
val = ["January","February","March","April"]
label_Challenger_1 = Label(frame, text="inserer combobox chall 1", font=("Arial", 15), bg="#87CEFA", fg="white")
label_Challenger_1.grid(row=9, column=4)

label_vs = Label(frame, text="VS", font=("Arial", 17), bg="#87CEFA", fg="white")
label_vs.grid(row=9, column=5)

label_Challenger_1 = Label(frame, text="inserer combobox chall 2", font=("Arial", 15), bg="#87CEFA", fg="white")
label_Challenger_1.grid(row=9, column=6)

#Discipline
label_Discipline = Label(frame, text="inserer combobox Discipline", font=("Arial", 15), bg="#87CEFA", fg="white")
label_Discipline.grid(row=3, column=6)

#bouton ajout
log_button = Button(frame, text="Ajouter", font=("Arial", 15), bg="white", fg="#87CEFA")
log_button.grid(row=10, column=5)

##Choisir un Vainqueur

#Choix Rencontre
label_Rencontre_Vainqueur = Label(frame, text="inserer combobox rencontre", font=("Arial", 15), bg="#87CEFA", fg="white")
label_Rencontre_Vainqueur.grid(row=13, column=4)

#Choix Vainqueur
label_Vainqueur_Rencontre = Label(frame, text="inserer combobox vainqueur", font=("Arial", 15), bg="#87CEFA", fg="white")
label_Vainqueur_Rencontre.grid(row=13, column=6)

#Bouton
log_button = Button(frame, text="Ajouter", font=("Arial", 15), bg="white", fg="#87CEFA")
log_button.grid(row=14, column=5)

frame.pack(expand=YES)

window.mainloop()
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
label_title.grid(row=0, column=2)

label_Statistique = Label(frame, text="Statistique", font=("Arial", 20), bg="#87CEFA", fg="white")
label_Statistique.grid(row=1, column=2)

label_Historique = Label(frame, text="Historique des gains", font=("Arial", 20), bg="#87CEFA", fg="white")
label_Historique.grid(row=1, column=1)

#Affichage des fonds
Fond = " Fond : " + str(1024) + " €"
label_Fond = Label(frame, text=Fond, font=("Arial", 15), bg="#87CEFA", fg="white")
label_Fond.grid(row=1, column=3)

#Récuperation identité
User = "Olivier Flauzac"

label_User = Label(frame, text=User, font=("Arial", 15), bg="#87CEFA", fg="white")
label_User.grid(row=0, column=0, sticky=W)

#feed + affichage de l'historique
historique = ['+10€', '+87€', '-12€']
for i in range(len(historique)):
    label_Rencontre = Label(frame, text=historique[i], font=("Arial", 15), bg="#87CEFA", fg="white")
    label_Rencontre.grid(row=i + 2, column=1, sticky=W)

#Affichage des statistiques
pourcentVictoire = "90%"
label_pourcentVictoire = Label(frame, text="Victoire : " + pourcentVictoire, font=("Arial", 15), bg="#87CEFA", fg="white")
label_pourcentVictoire.grid(row=2, column=2)

TotalGains = "1000€"
label_Statistique = Label(frame, text="Total des Gains : " + TotalGains, font=("Arial", 15), bg="#87CEFA", fg="white")
label_Statistique.grid(row=3, column=2)

NbParis = "2"
label_Statistique = Label(frame, text="Nombre de paris : " + NbParis, font=("Arial", 15), bg="#87CEFA", fg="white")
label_Statistique.grid(row=4, column=2)

label_depot = Label(frame, text="inserer combobox dépot", font=("Arial", 15), bg="#87CEFA", fg="white")
label_depot.grid(row=5, column=2)

depot_button = Button(frame, text="Déposer", font=("Arial", 15), bg="white", fg="#87CEFA")
depot_button.grid(row=6, column=2)

frame.pack(expand=YES)

window.mainloop()
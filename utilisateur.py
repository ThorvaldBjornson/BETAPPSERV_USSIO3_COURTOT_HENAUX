from tkinter import *
import socket
import json

class donnees:
    def __init__(self, data):
        self.__dict__ = json.loads(data)

def rencontre():
    rq = {
        "action": "afficher rencontre",
    }
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('192.168.1.86', 9999))
    message = json.dumps(rq)
    message_obj = donnees(message)
    print(message_obj.action)
    s.send(message.encode("ascii"))
    data = s.recv(1024)
    s.close()
    print(repr(data), 'Reçue')
    print(rq)
    data = donnees(data)
    return data


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
label_title.grid(row=0, column=2, sticky=N)

label_Rencontre = Label(frame, text="Rencontre", font=("Arial", 20), bg="#87CEFA", fg="white")
label_Rencontre.grid(row=1, column=1, sticky=W)

label_Historique = Label(frame, text="Historique des gains", font=("Arial", 20), bg="#87CEFA", fg="white")
label_Historique.grid(row=1, column=3, sticky=E)

#Récuperation identité
User = "Olivier Flauzac"

label_User = Label(frame, text=User, font=("Arial", 15), bg="#87CEFA", fg="white")
label_User.grid(row=0, column=0, sticky=W)

#feed + affichage des rencontres
rencontre = rencontre().rencontre
for i in range(len(rencontre)):
    r = donnees(json.dumps(rencontre[i]))
    values = r.nom + " le " + r.date + " à " + r.lieu

    label_Rencontre = Label(frame, text=values, font=("Arial", 15), bg="#87CEFA", fg="white")
    label_Rencontre.grid(row=i+2, column=0, sticky=W)
    log_button = Button(frame, text="Parier", font=("Arial", 15), bg="white", fg="#87CEFA")
    log_button.grid(row=i+2, column=1)

#feed + affichage de l'historique
historique = ['+10€', '+87€', '-12€']
for i in range(len(historique)):
    label_Rencontre = Label(frame, text=historique[i], font=("Arial", 15), bg="#87CEFA", fg="white")
    label_Rencontre.grid(row=i + 2, column=3, sticky=E)

#Affichage des fonds
Fond = " Fond : " + str(1024) + " €"
label_Fond = Label(frame, text=Fond, font=("Arial", 15), bg="#87CEFA", fg="white")
label_Fond.grid(row=0, column=3, sticky=E)

frame.pack(expand=YES)

window.mainloop()
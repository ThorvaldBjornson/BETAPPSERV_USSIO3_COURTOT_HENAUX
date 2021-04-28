import tkinter as tkinter
import tkinter.ttk as ttk
from tkinter import messagebox
import socket
import json

class donnees:
    def __init__(self, data):
        self.__dict__ = json.loads(data)

def parier():
    Montant = entry_Bet.get()
    Rencontre = "1"
    Challenger = label_Choix_Vainqueur.get()
    User = "6"
    print(Montant)
    rq = {
        "action": "parier",
        "utilisateur": User,
        "montant": Montant,
        "rencontre": Rencontre,
        "challenger": Challenger
    }
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('192.168.1.86', 9999))
    message = json.dumps(rq)
    message_obj = donnees(message)
    print(message_obj.action)
    s.send(message.encode("ascii"))
    data = s.recv(1024)
    s.close()
    print(rq)
    data = data.decode("ascii")
    if data == "fail":
        tkinter.messagebox.showwarning(title="Erreur", message="Vous n'avez pas les fonds nécessaire")

def challenger():
    Rencontre = "1"
    rq = {
        "action": "afficher challenger",
        "rencontre": Rencontre,
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

window = tkinter.Tk()

window.title("BetApp")
window.geometry("1280x720")
window.minsize(480,360)

#Logo
window.iconbitmap("logo.ico")
window.config(background="#87CEFA")

#Mise en place de la Frame
frame = tkinter.Frame(window, bg="#87CEFA", bd=1)

#Initialisation des titre
label_title = tkinter.Label(frame, text="BetApp", font=("Arial", 40), bg="#87CEFA", fg="white")
label_title.grid(row=0, column=2)

label_Rencontre = tkinter.Label(frame, text="Rencontre", font=("Arial", 15), bg="#87CEFA", fg="white")
label_Rencontre.grid(row=1, column=1)

val = challenger().challengers
print(val)
nomChall = []
for challenger in val:
    challenger = donnees(json.dumps(challenger))
    nomChall.append(challenger.nom)

label_Choix_Vainqueur = ttk.Combobox(frame, values=nomChall)
print(dict(label_Choix_Vainqueur))
label_Choix_Vainqueur.current(1)
label_Choix_Vainqueur.grid(row=2, column=2)

entry_Bet = tkinter.Entry(frame, font=("Arial", 15), bg="#87CEFA", fg="white")
entry_Bet.grid(row=1, column=3)

bet_Button = tkinter.Button(frame, text="Parier", font=("Arial", 15), bg="white", fg="#87CEFA", command=parier)
bet_Button.grid(row=3, column=2)

frame.pack()

window.mainloop()
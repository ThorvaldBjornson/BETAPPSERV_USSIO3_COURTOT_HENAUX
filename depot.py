import tkinter as tkinter
import tkinter.ttk as ttk
import socket
import json

class donnees:
    def __init__(self, data):
        self.__dict__ = json.loads(data)

def depot():
    print("Appel de depot")
    Montant = Combobox_depot.get()
    User = "1"
    print(Montant)
    rq = {
        "action": "deposer",
        "utilisateur": User,
        "montant": Montant,
    }
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('192.168.1.86', 9999))
    message = json.dumps(rq)
    message_obj = donnees(message)
    print(message_obj.action)
    s.send(message.encode("ascii"))
    print(rq)
    fond()

def historique():
    print("Appel de historique")
    User = "1"
    rq = {
        "action": "afficher historique",
        "utilisateur": User
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

def fond():
    print("Appel de fond")
    User = "1"
    rq = {
        "action": "afficher fonds",
        "utilisateur": User
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

def statistiques():
    print("Appel de statistiques")
    User = "1"
    rq = {
        "action": "afficher stats",
        "utilisateur": User
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

label_Statistique = tkinter.Label(frame, text="Statistique", font=("Arial", 20), bg="#87CEFA", fg="white")
label_Statistique.grid(row=1, column=2)

label_Historique = tkinter.Label(frame, text="Historique des gains", font=("Arial", 20), bg="#87CEFA", fg="white")
label_Historique.grid(row=1, column=1)

#Affichage des fonds
Fond = " Fonds : " + str(fond().fonds) + " €"
label_Fond = tkinter.Label(frame, text=Fond, font=("Arial", 15), bg="#87CEFA", fg="white")
label_Fond.grid(row=1, column=3)

#Récuperation identité
User = "Olivier Flauzac"

label_User = tkinter.Label(frame, text=User, font=("Arial", 15), bg="#87CEFA", fg="white")
label_User.grid(row=0, column=0)

#feed + affichage de l'historique
historique = historique().historique
for i in range(len(historique)):
    h = donnees(json.dumps(historique[i]))
    v = h.rencontre + " " + str(h.resultat) + " €"

    label_Rencontre = tkinter.Label(frame, text=v, font=("Arial", 15), bg="#87CEFA", fg="white")
    label_Rencontre.grid(row=i + 2, column=1)


#Affichage des statistiques
pourcentVictoire = str(statistiques().Ratio) + "%"
label_pourcentVictoire = tkinter.Label(frame, text="Victoire : " + pourcentVictoire, font=("Arial", 15), bg="#87CEFA", fg="white")
label_pourcentVictoire.grid(row=2, column=2)

TotalGains = str(statistiques().totalGain) + " €"
label_Statistique = tkinter.Label(frame, text="Total des Gains : " + TotalGains, font=("Arial", 15), bg="#87CEFA", fg="white")
label_Statistique.grid(row=3, column=2)

NbParis = str(statistiques().totalParis)
label_Statistique = tkinter.Label(frame, text="Nombre de paris : " + NbParis, font=("Arial", 15), bg="#87CEFA", fg="white")
label_Statistique.grid(row=4, column=2)

Combobox_depot = ttk.Combobox(frame,
                            values=[
                                    "10",
                                    "20",
                                    "50",
                                    "100",
                                    "200",
                                    "500",
                                    ])
print(dict(Combobox_depot))
Combobox_depot.current(1)
Combobox_depot.grid(row=5, column=2)

depot_button = tkinter.Button(frame, text="Déposer", font=("Arial", 15), bg="white", fg="#87CEFA", command=depot)
depot_button.grid(row=6, column=2)

frame.pack()

window.mainloop()
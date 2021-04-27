import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
import socket
import json

class donnees:
    def __init__(self, data):
        self.__dict__ = json.loads(data)

def raise_frame(frame):
    frame.tkraise()

root = tk.Tk()

root.title("BetApp")
root.geometry("1280x720")
root.minsize(480,360)
#Logo
root.iconbitmap("logo.ico")
root.config(background="#87CEFA")
#Ajout du Menu Bar
Menu_bar = tk.Menu(root)

action_menu = tk.Menu(Menu_bar, tearoff=0)
action_menu.add_command(label="Mon Compte", command=lambda: raise_frame(frameCompte))
action_menu.add_command(label="Quitter", command=root.quit)

Menu_bar.add_cascade(label="Action", menu=action_menu)


admin_menu = tk.Menu(Menu_bar, tearoff=0)
admin_menu.add_command(label="Administrer", command=lambda:raise_frame(frameAdmin))

Menu_bar.add_cascade(label="Administrateur", menu=admin_menu)

root.config(menu=Menu_bar)

#======================================================================
#-------------------------Frame Login---------------------------------
#======================================================================
def connect():
    User = entry_login.get()
    password = entry_mdp.get()
    rq = {
            "action" : "connection",
            "login"   : User,
            "password": password
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
    if('success' in data.decode("ascii")):
        raise_frame(frameUser)


#Mise en place de la Frame
frameLogin = tk.Frame(root, bg="#87CEFA", bd=1)

#Initialisation du titre
label_title = tk.Label(frameLogin, text="Bienvenue sur BetAppServeur", font=("Arial", 40), bg="#87CEFA", fg="white")
label_title.pack()

#Initialisation du formulaire
label_login = tk.Label(frameLogin, text="Login", font=("Arial", 20), bg="#87CEFA", fg="white")
label_login.pack()

entry_login = tk.Entry(frameLogin, font=("Arial", 20), bg="#87CEFA", fg="white")
entry_login.pack()

label_mdp = tk.Label(frameLogin, text="Mot de Passe", font=("Arial", 20), bg="#87CEFA", fg="white")
label_mdp.pack()

entry_mdp = tk.Entry(frameLogin, font=("Arial", 20), bg="#87CEFA", fg="white")
entry_mdp.pack()

log_button = tk.Button(frameLogin, text="Login", font=("Arial", 20), bg="#DCDCDC", fg="white", command=connect)
log_button.pack()





#======================================================================
#-------------------------Frame Utilisateur----------------------------
#======================================================================
class utilisateur:
    def rencontre(self):
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

    def historique(self):
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


    def fond(self):
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
ut = utilisateur()
#Mise en place de la Frame

frameUser= tk.Frame(root, bg="#87CEFA", bd=1)


#Initialisation des titre
label_title = tk.Label(frameUser, text="BetApp", font=("Arial", 40), bg="#87CEFA", fg="white")
label_title.grid(row=0, column=2)

label_Rencontre = tk.Label(frameUser, text="Rencontre", font=("Arial", 20), bg="#87CEFA", fg="white")
label_Rencontre.grid(row=1, column=1)

label_Historique = tk.Label(frameUser, text="Historique des gains", font=("Arial", 20), bg="#87CEFA", fg="white")
label_Historique.grid(row=1, column=3)

#Récuperation identité
User = "Olivier Flauzac"

label_User = tk.Label(frameUser, text=User, font=("Arial", 15), bg="#87CEFA", fg="white")
label_User.grid(row=0, column=0)

#feed + affichage des rencontres
rencontre = ut.rencontre().rencontre
for i in range(len(rencontre)):
    r = donnees(json.dumps(rencontre[i]))
    values = r.nom + " le " + r.date + " à " + r.lieu

    label_Rencontre = tk.Label(frameUser, text=values, font=("Arial", 15), bg="#87CEFA", fg="white")
    label_Rencontre.grid(row=i+2, column=0)
    log_button = tk.Button(frameUser, text="Parier", font=("Arial", 15), bg="white", fg="#87CEFA", command=lambda:raise_frame(framePari))
    log_button.grid(row=i+2, column=1)

#feed + affichage de l'historique
historique = ut.historique().historique
for i in range(len(historique)):
    h = donnees(json.dumps(historique[i]))
    v = str(h.resultat) + " €"

    label_Rencontre = tk.Label(frameUser, text=v, font=("Arial", 15), bg="#87CEFA", fg="white")
    label_Rencontre.grid(row=i + 2, column=3)

#Affichage des fonds
Fond = " Fonds : " + str(ut.fond().fonds) + " €"
label_Fond = tk.Label(frameUser, text=Fond, font=("Arial", 15), bg="#87CEFA", fg="white")
label_Fond.grid(row=0, column=3)

#======================================================================
#-------------------------Frame Pari-----------------------------------
#======================================================================
class Pari:
    def parier(self):
        Montant = entry_Bet.get()
        Rencontre = "1"
        Challenger = label_Choix_Vainqueur.get()
        User = "1"
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
            tk.messagebox.showwarning(title="Erreur", message="Vous n'avez pas les fonds nécessaire")

    def challenger(self):
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
pari = Pari()
#Mise en place de la Frame
framePari = tk.Frame(root, bg="#87CEFA", bd=1)

#Initialisation des titre
label_title = tk.Label(framePari, text="BetApp", font=("Arial", 40), bg="#87CEFA", fg="white")
label_title.grid(row=0, column=2)

label_Rencontre = tk.Label(framePari, text="Rencontre", font=("Arial", 15), bg="#87CEFA", fg="white")
label_Rencontre.grid(row=1, column=1)

val = pari.challenger().challengers
print(val)
nomChall = []
for challenger in val:
    challenger = donnees(json.dumps(challenger))
    nomChall.append(challenger.nom)

label_Choix_Vainqueur = ttk.Combobox(framePari, values=nomChall)
print(dict(label_Choix_Vainqueur))
label_Choix_Vainqueur.current(1)
label_Choix_Vainqueur.grid(row=2, column=2)

entry_Bet = tk.Entry(framePari, font=("Arial", 15), bg="#87CEFA", fg="white")
entry_Bet.grid(row=1, column=3)

bet_Button = tk.Button(framePari, text="Parier", font=("Arial", 15), bg="white", fg="#87CEFA", command=lambda:pari.parier()).grid(row=3, column=2)

#======================================================================
#-----------------------Frame visualisation compte---------------------
#======================================================================
class compte:
    def depot(self):
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

    def historique(self):
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

    def fond(self):
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

    def statistiques(self):
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
compteUser = compte()
#Mise en place de la Frame
frameCompte = tk.Frame(root, bg="#87CEFA", bd=1)

#Initialisation des titre
label_title = tk.Label(frameCompte, text="BetApp", font=("Arial", 40), bg="#87CEFA", fg="white")
label_title.grid(row=0, column=2)

label_Statistique = tk.Label(frameCompte, text="Statistique", font=("Arial", 20), bg="#87CEFA", fg="white")
label_Statistique.grid(row=1, column=2)

label_Historique = tk.Label(frameCompte, text="Historique des gains", font=("Arial", 20), bg="#87CEFA", fg="white")
label_Historique.grid(row=1, column=1)

#Affichage des fonds
Fond = " Fonds : " + str(compteUser.fond().fonds) + " €"
label_Fond = tk.Label(frameCompte, text=Fond, font=("Arial", 15), bg="#87CEFA", fg="white")
label_Fond.grid(row=1, column=3)

#Récuperation identité
User = "Olivier Flauzac"

label_User = tk.Label(frameCompte, text=User, font=("Arial", 15), bg="#87CEFA", fg="white")
label_User.grid(row=0, column=0)

#feed + affichage de l'historique
historique = compteUser.historique().historique
for i in range(len(historique)):
    h = donnees(json.dumps(historique[i]))
    v = h.rencontre + " " + str(h.resultat) + " €"

    label_Rencontre = tk.Label(frameCompte, text=v, font=("Arial", 15), bg="#87CEFA", fg="white")
    label_Rencontre.grid(row=i + 2, column=1)


#Affichage des statistiques
pourcentVictoire = str(compteUser.statistiques().Ratio) + "%"
label_pourcentVictoire = tk.Label(frameCompte, text="Victoire : " + pourcentVictoire, font=("Arial", 15), bg="#87CEFA", fg="white")
label_pourcentVictoire.grid(row=2, column=2)

TotalGains = str(compteUser.statistiques().totalGain) + " €"
label_Statistique = tk.Label(frameCompte, text="Total des Gains : " + TotalGains, font=("Arial", 15), bg="#87CEFA", fg="white")
label_Statistique.grid(row=3, column=2)

NbParis = str(compteUser.statistiques().totalParis)
label_Statistique = tk.Label(frameCompte, text="Nombre de paris : " + NbParis, font=("Arial", 15), bg="#87CEFA", fg="white")
label_Statistique.grid(row=4, column=2)

Combobox_depot = ttk.Combobox(frameCompte,
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

depot_button = tk.Button(frameCompte, text="Déposer", font=("Arial", 15), bg="white", fg="#87CEFA", command=lambda:compteUser.depot())
depot_button.grid(row=6, column=2)


#======================================================================
#-----------------------------Frame Admin------------------------------
#======================================================================
class admin:
    def rencontre(self):
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

    def challenger(self):
        rq = {
            "action": "afficher all challenger"
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

    def discipline(self):
        rq = {
            "action": "afficher discipline"
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

admin = admin()
#Mise en place de la Frame
frameAdmin = tk.Frame(root, bg="#87CEFA", bd=1)


#Initialisation des titre
label_title = tk.Label(frameAdmin, text="BetApp", font=("Arial", 40), bg="#87CEFA", fg="white")
label_title.grid(row=0, column=3)

label_Rencontre = tk.Label(frameAdmin, text="Rencontre", font=("Arial", 20), bg="#87CEFA", fg="white")
label_Rencontre.grid(row=2, column=1, columnspan=2)

label_Ajout_Rencontre = tk.Label(frameAdmin, text="Ajouter Une Rencontre", font=("Arial", 20), bg="#87CEFA", fg="white")
label_Ajout_Rencontre.grid(row=2, column=5)

#Récuperation identité
User = "Admin"

label_User = tk.Label(frameAdmin, text=User, font=("Arial", 15), bg="#87CEFA", fg="white")
label_User.grid(row=0, column=0)

## Rencontre

#feed + affichage des rencontres
rencontre = admin.rencontre().rencontre
for i in range(len(rencontre)):
    r = donnees(json.dumps(rencontre[i]))
    values = r.nom + " le " + r.date + " à " + r.lieu

    label_Rencontre = tk.Label(frameAdmin, text=values, font=("Arial", 15), bg="#87CEFA", fg="white")
    label_Rencontre.grid(row=i+3, column=0)
    Cancel_button = tk.Button(frameAdmin, text="Annulé", font=("Arial", 15), bg="white", fg="#87CEFA", command=lambda:raise_frame(framePari))
    Cancel_button.grid(row=i+3, column=1)
    Winner_button = tk.Button(frameAdmin, text="Choisir un Vainqueur", font=("Arial", 15), bg="white", fg="#87CEFA", command=lambda: raise_frame(frameVainqueur))
    Winner_button.grid(row=i + 3, column=2)

## Ajout d'une rencontre
#Nom rencontre
label_Nom_Rencontre = tk.Label(frameAdmin, text="Nom de la Rencontre :", font=("Arial", 15), bg="#87CEFA", fg="white")
label_Nom_Rencontre.grid(row=3, column=4)
entry_Nom_Rencontre = tk.Entry(frameAdmin, font=("Arial", 15), bg="#87CEFA", fg="white")
entry_Nom_Rencontre.grid(row=4, column=4)

#Date Rencontre
label_Date_Rencontre = tk.Label(frameAdmin, text="Date de la Rencontre :", font=("Arial", 15), bg="#87CEFA", fg="white")
label_Date_Rencontre.grid(row=5, column=4)
entry_Date_Rencontre = tk.Entry(frameAdmin, font=("Arial", 15), bg="#87CEFA", fg="white")
entry_Date_Rencontre.grid(row=6, column=4)

#Lieu Rencontre
label_Nom_Rencontre = tk.Label(frameAdmin, text="Lieux de la Rencontre :", font=("Arial", 15), bg="#87CEFA", fg="white")
label_Nom_Rencontre.grid(row=7, column=4)
entry_Nom_Rencontre = tk.Entry(frameAdmin, font=("Arial", 15), bg="#87CEFA", fg="white")
entry_Nom_Rencontre.grid(row=8, column=4)

#Challenger
v = admin.challenger().challengers
nomChall = []
for challenger in v:
    challenger = donnees(json.dumps(challenger))
    nomChall.append(challenger.nom)

label_Choix_Challenger1 = ttk.Combobox(frameAdmin, values=nomChall)
print(dict(label_Choix_Challenger1))
label_Choix_Challenger1.current(0)
label_Choix_Challenger1.grid(row=9, column=4)

label_vs = tk.Label(frameAdmin, text="VS", font=("Arial", 17), bg="#87CEFA", fg="white")
label_vs.grid(row=9, column=5)

va = admin.challenger().challengers
nomChall = []
for challenger in va:
    challenger = donnees(json.dumps(challenger))
    nomChall.append(challenger.nom)

label_Choix_Challenger2 = ttk.Combobox(frameAdmin, values=nomChall)
print(dict(label_Choix_Challenger2))
label_Choix_Challenger2.current(0)
label_Choix_Challenger2.grid(row=9, column=6)

#Discipline
label_Discipline = tk.Label(frameAdmin, text="Choix de la Discipline :", font=("Arial", 15), bg="#87CEFA", fg="white")
label_Discipline.grid(row=4, column=6)
valueDiscipline = admin.discipline().disciplines
Discipline = []
for discipline in valueDiscipline:
    discipline = donnees(json.dumps(discipline))
    Discipline.append(discipline.nom)

label_Choix_Discipline = ttk.Combobox(frameAdmin, values=Discipline)
print(dict(label_Choix_Discipline))
label_Choix_Discipline.current(0)
label_Choix_Discipline.grid(row=5, column=6)


#bouton ajout
log_button = tk.Button(frameAdmin, text="Ajouter", font=("Arial", 15), bg="white", fg="#87CEFA")
log_button.grid(row=10, column=5)

#======================================================================
#---------------------------Choix Vainqueur----------------------------
#======================================================================
class Vainqueur:

    def challenger(self):
        Rencontre = "1"
        rq = {
            "action": "afficher challenger",
            "rencontre": Rencontre
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

frameVainqueur= tk.Frame(root, bg="#87CEFA", bd=1)

#Choix Rencontre
label_Rencontre_Vainqueur = tk.Label(frameVainqueur, text="inserer combobox rencontre", font=("Arial", 15), bg="#87CEFA", fg="white")
label_Rencontre_Vainqueur.grid(row=13, column=4)

#Choix Vainqueur
Vainqueur = admin.challenger().challengers
nomVainqueur = []
for challenger in Vainqueur:
    challenger = donnees(json.dumps(challenger))
    nomVainqueur.append(challenger.nom)

label_Choix_Challenger1 = ttk.Combobox(frameVainqueur, values=nomVainqueur)
print(dict(label_Choix_Challenger1))
label_Choix_Challenger1.current(0)
label_Choix_Challenger1.grid(row=9, column=4)

#Bouton
log_button = tk.Button(frameVainqueur, text="Ajouter", font=("Arial", 15), bg="white", fg="#87CEFA")
log_button.grid(row=14, column=5)

#======================================================================
#-------------Assemblage des frames, génération de la page-------------
#======================================================================

for frame in (frameLogin, frameUser, frameCompte, framePari, frameAdmin, frameVainqueur):
    frame.grid(row=0, column=0, sticky='news')

raise_frame(frameLogin)
root.mainloop()
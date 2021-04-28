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
AjoutRencontre = tk.Menu(Menu_bar, tearoff=0)
admin_menu.add_command(label="Accueil", command=lambda:raise_frame(frameRencontre))
AjoutRencontre.add_command(label="Ajouter Une Rencontre", command=lambda:raise_frame(frameAjout))

Menu_bar.add_cascade(label="Administrateur", menu=admin_menu)

root.config(menu=Menu_bar)

#======================================================================
#-------------------------Frame Login----------------------------------
#======================================================================
def connect():
    User = EntryLogin.get()
    password = EntryPassword.get()
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
    else:
        tk.messagebox.showwarning(title="Erreur", message="Vous n'avez pas entrez le bon couple identifiant mot de passe.")

#Mise en place de la Frame
frameLogin = tk.Frame(root, bg="#87CEFA", bd=1)

#Initialisation du titre
LabelTitleAccueil = tk.Label(frameLogin, text="Bienvenue sur BetAppServeur", font=("Arial", 40), bg="#87CEFA", fg="white")
LabelTitleAccueil.grid()

#Initialisation du formulaire de Login
LabelLogin = tk.Label(frameLogin, text="Login", font=("Arial", 20), bg="#87CEFA", fg="white")
LabelLogin.grid()

EntryLogin = tk.Entry(frameLogin, font=("Arial", 20), bg="#87CEFA", fg="white")
EntryLogin.grid()

LabelMdp = tk.Label(frameLogin, text="Mot de Passe", font=("Arial", 20), bg="#87CEFA", fg="white")
LabelMdp.grid()

EntryPassword = tk.Entry(frameLogin, font=("Arial", 20), bg="#87CEFA", fg="white", show='*')
EntryPassword.grid()

ButtonConnexion = tk.Button(frameLogin, text="Login", font=("Arial", 20), bg="#DCDCDC", fg="white", command=connect)
ButtonConnexion.grid()

ButtonGoToRegister = tk.Button(frameLogin, text="S'enregistrer", font=("Arial", 20), bg="#DCDCDC", fg="white", command=lambda: raise_frame(frameRegister) )
ButtonGoToRegister.grid()

#======================================================================
#------------------------Frame Register--------------------------------
#======================================================================
def register():
    User = EntryRegister.get()
    if LabelRegisterPassword.get() != EntryConfirmPassword.get():
        tk.messagebox.showwarning(title="Erreur", message="Vous n'avez pas entrez les mêmes mot de passe.")
    password = EntryRegisterPassword.get()
    rq = {
            "action" : "register",
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
    print(rq)
    if('success' in data.decode("ascii")):
        raise_frame(frameUser)
    elif('login existant' in data.decode("ascii")):
        tk.messagebox.showwarning(title="Erreur", message="Cette identifiant existe déjà.")
    else:
        tk.messagebox.showwarning(title="Erreur", message="Erreur.")

frameRegister = tk.Frame(root, bg="#87CEFA", bd=1)

LabelTitleRegister = tk.Label(frameRegister, text="Bienvenue sur BetAppServeur", font=("Arial", 40), bg="#87CEFA", fg="white")
LabelTitleRegister.grid(row=0, column=0)
#Initialisation du formulaire de Register
LabelRegister = tk.Label(frameRegister, text="Identifiant", font=("Arial", 20), bg="#87CEFA", fg="white")
LabelRegister.grid(row=1, column=0)

EntryRegister = tk.Entry(frameRegister, font=("Arial", 20), bg="#87CEFA", fg="white")
EntryRegister.grid(row=2, column=0)

LabelRegisterPassword = tk.Label(frameRegister, text="Mot de Passe", font=("Arial", 20), bg="#87CEFA", fg="white")
LabelRegisterPassword.grid(row=3, column=0)

EntryRegisterPassword = tk.Entry(frameRegister, font=("Arial", 20), bg="#87CEFA", fg="white", show='*')
EntryRegisterPassword.grid(row=4, column=0)

LabelConfirmPassword = tk.Label(frameRegister, text="Confirmer le Mot de Passe", font=("Arial", 20), bg="#87CEFA", fg="white")
LabelConfirmPassword.grid(row=5, column=0)

EntryConfirmPassword = tk.Entry(frameRegister, font=("Arial", 20), bg="#87CEFA", fg="white", show='*')
EntryConfirmPassword.grid(row=6, column=0)

ButtonRegister = tk.Button(frameRegister, text="S'enregistrer", font=("Arial", 20), bg="#DCDCDC", fg="white", command=register)
ButtonRegister.grid(row=7, column=0)

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
        User = "6"
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
        data = s.recv(999999)
        s.close()
        print(repr(data), 'Reçue')
        print(rq)
        data = donnees(data)
        return data


    def fond(self):
        User = "6"
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
LabelTitleUser = tk.Label(frameUser, text="BetApp", font=("Arial", 40), bg="#87CEFA", fg="white")
LabelTitleUser.grid(row=0, column=2)

LabelTitleRencontre = tk.Label(frameUser, text="Rencontre", font=("Arial", 20), bg="#87CEFA", fg="white")
LabelTitleRencontre.grid(row=1, column=0)

LabelTitleHistorique = tk.Label(frameUser, text="Historique des gains", font=("Arial", 20), bg="#87CEFA", fg="white")
LabelTitleHistorique.grid(row=1, column=2)

#Récuperation identité
User = "Olivier Flauzac"

LabelUser = tk.Label(frameUser, text=User, font=("Arial", 15), bg="#87CEFA", fg="white")
LabelUser.grid(row=0, column=0)

#feed + affichage des rencontres
rencontre = ut.rencontre().rencontre
for i in range(len(rencontre)):
    r = donnees(json.dumps(rencontre[i]))
    values = r.nom + " le " + r.date + " à " + r.lieu

    LabelRencontre = tk.Label(frameUser, text=values, font=("Arial", 15), bg="#87CEFA", fg="white")
    LabelRencontre.grid(row=i+2, column=0)
ButtonParier = tk.Button(frameUser, text="Parier", font=("Arial", 15), bg="white", fg="#87CEFA", command=lambda:raise_frame(framePari))
ButtonParier.grid(row=i+3, column=0)

#feed + affichage de l'historique
historique = ut.historique().historique
for i in range(len(historique)):
    h = donnees(json.dumps(historique[i]))
    v = str(h.resultat) + " €"

    LabelHistorique = tk.Label(frameUser, text=v, font=("Arial", 15), bg="#87CEFA", fg="white")
    LabelHistorique.grid(row=i + 2, column=3)

#Affichage des fonds
Fond = " Fonds : " + str(ut.fond().fonds) + " €"
LabelFond = tk.Label(frameUser, text=Fond, font=("Arial", 15), bg="#87CEFA", fg="white")
LabelFond.grid(row=0, column=3)

#======================================================================
#-------------------------Frame Pari-----------------------------------
#======================================================================
class Pari:
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

    def parier(self):
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
            tk.messagebox.showwarning(title="Erreur", message="Vous n'avez pas les fonds nécessaire")

    def challenger(self):
        Rencontre = "5"
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
LabelTitrePari = tk.Label(framePari, text="BetApp", font=("Arial", 40), bg="#87CEFA", fg="white")
LabelTitrePari.grid(row=0, column=0, columnspan=2)

LabelTitreRencontre = tk.Label(framePari, text="Choisir une rencontre : ", font=("Arial", 15), bg="#87CEFA", fg="white")
LabelTitreRencontre.grid(row=1, column=0)

RencontrePari = pari.rencontre().rencontre
nomRencontrePari = []
idRencontrePari = []
for rencontre in RencontrePari:
    rencontre = donnees(json.dumps(rencontre))
    nomRencontrePari.append(rencontre.nom)
    idRencontrePari.append(rencontre.id)

ComboboxRencontrePari = ttk.Combobox(framePari, values=nomRencontrePari, state="readonly")
print(dict(ComboboxRencontrePari))
ComboboxRencontrePari.current(0)
ComboboxRencontrePari.grid(row=1, column=1)

ValeurChallenger = pari.challenger().challengers
print(ValeurChallenger)

LabelChallengerPari = tk.Label(framePari, text="Choisir une challenger : ", font=("Arial", 15), bg="#87CEFA", fg="white")
LabelChallengerPari.grid(row=2, column=0)

nomChall = []
for challenger in ValeurChallenger:
    challenger = donnees(json.dumps(challenger))
    nomChall.append(challenger.nom)

LabelChoixVainqueur = ttk.Combobox(framePari, values=nomChall, state="readonly")
print(dict(LabelChoixVainqueur))

LabelChoixVainqueur.current(0)
LabelChoixVainqueur.grid(row=2, column=1)

LabelMontantPari = tk.Label(framePari, text="Choisir un montant : ", font=("Arial", 15), bg="#87CEFA", fg="white")
LabelMontantPari.grid(row=3, column=0)

EntryPari = tk.Entry(framePari, font=("Arial", 15), bg="#87CEFA", fg="white")
EntryPari.grid(row=3, column=1)

ButtonPari = tk.Button(framePari, text="Parier", font=("Arial", 15), bg="white", fg="#87CEFA", command=lambda:pari.parier()).grid(row=4, column=0, columnspan=2)

#======================================================================
#-----------------------Frame visualisation compte---------------------
#======================================================================
class compte:
    def depot(self):
        print("Appel de depot")
        Montant = Combobox_depot.get()
        User = "6"
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
        self.fond()

    def historique(self):
        print("Appel de historique")
        User = "6"
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
        data = s.recv(999999)
        s.close()
        print(repr(data), 'Reçue')
        print(rq)
        data = donnees(data)
        return data

    def fond(self):
        print("Appel de fond")
        User = "6"
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
        User = "6"
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
LabelTitreCompte = tk.Label(frameCompte, text="BetApp", font=("Arial", 40), bg="#87CEFA", fg="white")
LabelTitreCompte.grid(row=0, column=2)

LabelStatistique = tk.Label(frameCompte, text="Statistique", font=("Arial", 20), bg="#87CEFA", fg="white")
LabelStatistique.grid(row=1, column=2)

LabelHistorique = tk.Label(frameCompte, text="Historique des gains", font=("Arial", 20), bg="#87CEFA", fg="white")
LabelHistorique.grid(row=1, column=1)

#Affichage des fonds
Fond = " Fonds : " + str(compteUser.fond().fonds) + " €"
LabelFond = tk.Label(frameCompte, text=Fond, font=("Arial", 15), bg="#87CEFA", fg="white")
LabelFond.grid(row=1, column=3)

#Récuperation identité
User = "Olivier Flauzac"

LabelUser = tk.Label(frameCompte, text=User, font=("Arial", 15), bg="#87CEFA", fg="white")
LabelUser.grid(row=0, column=0)

#feed + affichage de l'historique
Historique = compteUser.historique().historique
for i in range(len(Historique)):
    h = donnees(json.dumps(Historique[i]))
    valueHistorique = h.rencontre + " " + str(h.resultat) + " €"

    LabelRencontreUser = tk.Label(frameCompte, text=valueHistorique, font=("Arial", 15), bg="#87CEFA", fg="white")
    LabelRencontreUser.grid(row=i + 2, column=1)


#Affichage des statistiques
StatPourcentVictoire = str(compteUser.statistiques().Ratio) + "%"
LabelStatPourcentVictoire = tk.Label(frameCompte, text="Victoire : " + StatPourcentVictoire, font=("Arial", 15), bg="#87CEFA", fg="white")
LabelStatPourcentVictoire.grid(row=2, column=2)

StatTotalGains = str(compteUser.statistiques().totalGain) + " €"
LabelStatTotalGains = tk.Label(frameCompte, text="Total des Gains : " + StatTotalGains, font=("Arial", 15), bg="#87CEFA", fg="white")
LabelStatTotalGains.grid(row=3, column=2)

StatNombreParis = str(compteUser.statistiques().totalParis)
LabelStatNombreParis = tk.Label(frameCompte, text="Nombre de paris : " + StatNombreParis, font=("Arial", 15), bg="#87CEFA", fg="white")
LabelStatNombreParis.grid(row=4, column=2)

ComboboxDepot = ttk.Combobox(frameCompte,
                            values=[
                                    "10",
                                    "20",
                                    "50",
                                    "100",
                                    "200",
                                    "500",
                                    ], state="readonly")
print(dict(ComboboxDepot))
ComboboxDepot.current(1)
ComboboxDepot.grid(row=5, column=2)

ButtonDepot = tk.Button(frameCompte, text="Déposer", font=("Arial", 15), bg="white", fg="#87CEFA", command=lambda:compteUser.depot())
ButtonDepot.grid(row=6, column=2)


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

admin = admin()

#Mise en place de la Frame
frameAdmin = tk.Frame(root, bg="#87CEFA", bd=1)

#Initialisation des titre
LabelTitleAdmin = tk.Label(frameAdmin, text="BetApp", font=("Arial", 40), bg="#87CEFA", fg="white")
LabelTitleAdmin.grid(row=0, column=3)

LabelTitleRencontreAdmin = tk.Label(frameAdmin, text="Rencontre", font=("Arial", 20), bg="#87CEFA", fg="white")
LabelTitleRencontreAdmin.grid(row=2, column=1, columnspan=2)

LabelAjoutRencontre = tk.Label(frameAdmin, text="Ajouter Une Rencontre", font=("Arial", 20), bg="#87CEFA", fg="white")
LabelAjoutRencontre.grid(row=2, column=5)

#Récuperation identité
User = "Admin"

LabelUserAdmin = tk.Label(frameAdmin, text=User, font=("Arial", 15), bg="#87CEFA", fg="white")
LabelUserAdmin.grid(row=0, column=0)

## Rencontre
#feed + affichage des rencontres
rencontreAdmin = admin.rencontre().rencontre
for i in range(len(rencontreAdmin)):
    r = donnees(json.dumps(rencontreAdmin[i]))
    valuesRencontreAdmin = r.nom + " le " + r.date + " à " + r.lieu

    labelRencontreAdmin = tk.Label(frameAdmin, text=valuesRencontreAdmin, font=("Arial", 15), bg="#87CEFA", fg="white")
    labelRencontreAdmin.grid(row=i+3, column=0)
    ButtonCancel = tk.Button(frameAdmin, text="Annulé", font=("Arial", 15), bg="white", fg="#87CEFA", command=lambda:raise_frame(framePari))
    ButtonCancel.grid(row=i+3, column=1)
    ButtonWinner = tk.Button(frameAdmin, text="Choisir un Vainqueur", font=("Arial", 15), bg="white", fg="#87CEFA", command=lambda: raise_frame(frameVainqueur))
    ButtonWinner.grid(row=i + 3, column=2)

#======================================================================
#---------------------------Ajout Rencontre----------------------------
#======================================================================

class Rencontre:
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

    def ajoutRencontre(self):


        discipline = idDiscipline[LabelChoixDiscipline.current()]
        rencontre = EntryNomRencontre.get()
        challenger1 = idChallenger[LabelChoixChallenger1.current()]
        challenger2 = idChallenger2[LabelChoixChallenger2.current()]
        cote_challenger1 = EntryCoteChallenger1.get()
        cote_challenger2 =  EntryCoteChallenger2.get()
        date = EntryDateRencontre.get()
        lieu = EntryLieuRencontre.get()
        print(discipline)
        print(rencontre)
        print(challenger1)
        print(challenger2)
        print(cote_challenger1)
        print(cote_challenger2)
        print(date)
        print(lieu)
        if discipline == ''  or rencontre == ''  or challenger1 == ''  or challenger2 == ''  or cote_challenger1 == ''  or cote_challenger2 == ''  or date == ''  or lieu == '' :
            tk.messagebox.showwarning(title="Erreur", message="Veuillez remplir tous les champs.")
        else :
            if challenger1 ==  challenger2 :
                tk.messagebox.showwarning(title="Erreur", message="Veuillez Choisir deux challengers différents.")
            else :
                rq = {
                    "action": "ajout rencontre",
                    "admin" : 3,
                    "discipline": discipline,
                    "rencontre": rencontre,
                    "challenger1": challenger1,
                    "challenger2": challenger2,
                    "cote_challenger1": cote_challenger1,
                    "cote_challenger2": cote_challenger2,
                    "date": date,
                    "lieu": lieu
                }
                print("Appel de ajout")
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect(('192.168.1.86', 9999))
                message = json.dumps(rq)
                message_obj = donnees(message)
                print(message_obj.action)
                s.send(message.encode("ascii"))
                print(rq)

ajout = Rencontre()
## Ajout d'une rencontre
#Nom rencontre
LabelNomRencontre = tk.Label(frameAdmin, text="Nom de la Rencontre :", font=("Arial", 15), bg="#87CEFA", fg="white")
LabelNomRencontre.grid(row=3, column=4)
EntryNomRencontre = tk.Entry(frameAdmin, font=("Arial", 15), bg="#87CEFA", fg="white")
EntryNomRencontre.grid(row=4, column=4)

#Date Rencontre
LabelDateRencontre = tk.Label(frameAdmin, text="Date de la Rencontre :", font=("Arial", 15), bg="#87CEFA", fg="white")
LabelDateRencontre.grid(row=5, column=4)
EntryDateRencontre = tk.Entry(frameAdmin, font=("Arial", 15), bg="#87CEFA", fg="white")
EntryDateRencontre.grid(row=6, column=4)

#Lieu Rencontre
LabelLieuRencontre = tk.Label(frameAdmin, text="Lieux de la Rencontre :", font=("Arial", 15), bg="#87CEFA", fg="white")
LabelLieuRencontre.grid(row=7, column=4)
EntryLieuRencontre = tk.Entry(frameAdmin, font=("Arial", 15), bg="#87CEFA", fg="white")
EntryLieuRencontre.grid(row=8, column=4)

#Challenger
valeurChallengerAdmin = admin.challenger().challengers
nomChallAdmin = []
idChallengerAdmin = []
for challenger in valeurChallengerAdmin:
    challenger = donnees(json.dumps(challenger))
    nomChallAdmin.append(challenger.nom)
    idChallengerAdmin.append(challenger.id)

LabelChoixChallenger1 = ttk.Combobox(frameAdmin, values=nomChallAdmin, state="readonly")
print(dict(LabelChoixChallenger1))
LabelChoixChallenger1.current(0)
LabelChoixChallenger1.grid(row=9, column=4)

LabelCoteChallenger1 = tk.Label(frameAdmin, text="Cote du challenger :", font=("Arial", 17), bg="#87CEFA", fg="white")
LabelCoteChallenger1.grid(row=10, column=4)

EntryCoteChallenger1 = tk.Entry(frameAdmin, font=("Arial", 15), bg="#87CEFA", fg="white")
EntryCoteChallenger1.grid(row=11, column=4)

LabelVs = tk.Label(frameAdmin, text="VS", font=("Arial", 17), bg="#87CEFA", fg="white")
LabelVs.grid(row=9, column=5)

valeurChallenger2Admin = admin.challenger().challengers
nomChallAdmin2 = []
idChallengerAdmin2 = []
for challenger in valeurChallenger2Admin:
    challenger = donnees(json.dumps(challenger))
    nomChallAdmin2.append(challenger.nom)
    idChallengerAdmin2.append(challenger.id)

LabelChoixChallenger2 = ttk.Combobox(frameAdmin, values=nomChallAdmin2, state="readonly")
print(dict(LabelChoixChallenger2))
LabelChoixChallenger2.current(0)
LabelChoixChallenger2.grid(row=9, column=6)

LabelCoteChallenger2 = tk.Label(frameAdmin, text="Cote du challenger :", font=("Arial", 17), bg="#87CEFA", fg="white")
LabelCoteChallenger2.grid(row=10, column=6)

EntryCoteChallenger2 = tk.Entry(frameAdmin, font=("Arial", 15), bg="#87CEFA", fg="white")
EntryCoteChallenger2.grid(row=11, column=6)

#Discipline
LabelDiscipline = tk.Label(frameAdmin, text="Choix de la Discipline :", font=("Arial", 15), bg="#87CEFA", fg="white")
LabelDiscipline.grid(row=4, column=6)
valueDiscipline = admin.discipline().disciplines
Discipline = []
idDiscipline = []
for discipline in valueDiscipline:
    discipline = donnees(json.dumps(discipline))
    Discipline.append(discipline.nom)
    idDiscipline.append(discipline.id)

LabelChoixDiscipline = ttk.Combobox(frameAdmin, values=Discipline, state="readonly")
print(dict(LabelChoixDiscipline))
LabelChoixDiscipline.current(0)
LabelChoixDiscipline.grid(row=5, column=6)


#bouton ajout
ButtonAjoutRencontre = tk.Button(frameAdmin, text="Ajouter", font=("Arial", 15), bg="white", fg="#87CEFA", command=lambda : admin.ajoutRencontre())
ButtonAjoutRencontre.grid(row=12, column=5)

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

    def envoiVainqueur(self):
        Rencontre = "1"
        rq = {
            "action": "choisir vainqueur",
            "rencontre": Rencontre,
            "challenger": idVainqueur[ComboboxVainqueur.current()]
        }
        print(idVainqueur[cbbVainqueur.current()])
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
        return data

vainqueur = Vainqueur()

frameAjout= tk.Frame(root, bg="#87CEFA", bd=1)

LabelTitleVainqueur = tk.Label(frameAjout, text="BetApp", font=("Arial", 40), bg="#87CEFA", fg="white")
LabelTitleVainqueur.grid(row=0, column=0)

#Choix Rencontre
LabelRencontreVainqueur = tk.Label(frameAjout, text="Choisir un Vainqueur", font=("Arial", 15), bg="#87CEFA", fg="white")
LabelRencontreVainqueur.grid(row=1, column=0)

#Choix Vainqueur
Challengers = admin.challenger().challengers
nomVainqueur = []
idVainqueur = []
for challenger in Challengers:
    challenger = donnees(json.dumps(challenger))
    nomVainqueur.append(challenger.nom)
    idVainqueur.append(challenger.id)

ComboboxVainqueur = ttk.Combobox(frameAjout, values=nomVainqueur, state="readonly")
print(dict(ComboboxVainqueur))
ComboboxVainqueur.current(0)
ComboboxVainqueur.grid(row=2, column=0)

#Bouton
btnVainqueur = tk.Button(frameAjout, text="Ajouter", font=("Arial", 15), bg="white", fg="#87CEFA", command=lambda :vainqueur.envoiVainqueur())
btnVainqueur.grid(row=3, column=0)

#======================================================================
#-------------Assemblage des frames, génération de la page-------------
#======================================================================

for frame in (frameLogin, frameUser, frameCompte, framePari, frameAdmin, frameVainqueur, frameRegister, frameAjout):
    frame.grid(row=0, column=0, sticky='news')

raise_frame(frameLogin)
root.mainloop()

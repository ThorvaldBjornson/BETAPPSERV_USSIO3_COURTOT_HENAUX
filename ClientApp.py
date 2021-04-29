import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
import hashlib
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
def creationMenuDefault():
    Menu_bar = tk.Menu(root)
    action_menu = tk.Menu(Menu_bar, tearoff=0)
    action_menu.add_command(label="Quitter", command=root.quit)
    Menu_bar.add_cascade(label="Action", menu=action_menu)
    root.config(menu=Menu_bar)
def creationMenuUser():
    Menu_bar = tk.Menu(root)
    action_menu = tk.Menu(Menu_bar, tearoff=0)
    action_menu.add_command(label="Acceuil", command=lambda: creationFrameUtilisateur())
    action_menu.add_command(label="Mon Compte", command=lambda: creationFrameCompte())
    action_menu.add_command(label="deconnecter", command=lambda: deconnexion())
    action_menu.add_command(label="Quitter", command=root.quit)
    Menu_bar.add_cascade(label="Action", menu=action_menu)
    root.config(menu=Menu_bar)

def creationMenuAdmin():
    Menu_bar = tk.Menu(root)
    admin_menu = tk.Menu(Menu_bar, tearoff=0)
    admin_menu.add_command(label="Accueil", command=lambda: creationFrameAdmin())
    admin_menu.add_command(label="Ajouter Une Rencontre", command=lambda: creationFrameAjout())
    admin_menu.add_command(label="Annuler Une Rencontre", command=lambda: creationFrameCancel())
    admin_menu.add_command(label="deconnecter", command=lambda: deconnexion())
    admin_menu.add_command(label="Quitter", command=root.quit)

    Menu_bar.add_cascade(label="Administrateur", menu=admin_menu)

    root.config(menu=Menu_bar)
#======================================================================
#-------------------------Frame Login----------------------------------
#======================================================================
login = False
def connect():
    User = EntryLogin.get()
    password = EntryPassword.get()
    password = hashlib.sha256(password.encode()).hexdigest()
    rq = {
            "action" : "connection",
            "login"   : User,
            "password": password
        }
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('192.168.1.86', 9999))
    print(rq)
    message = json.dumps(rq)
    message_obj = donnees(message)
    print(message_obj.action)
    s.send(message.encode("ascii"))
    data = s.recv(1024)
    s.close()
    print(repr(data), 'Reçue')
    if('fail' in data.decode("ascii")):
        tk.messagebox.showwarning(title="Erreur", message="Vous n'avez pas entrez le bon couple identifiant mot de passe.")
    else:
        data = donnees(data)
        ut.setDataUser(data.idUtilisateur, data.login, data.role)
        if(ut.role == "parieur"):
            creationFrameUtilisateur()
            creationMenuUser()
        elif(ut.role == "admin"):
            creationFrameAdmin()
            creationMenuAdmin()


frameLogin = tk.Frame(root, bg="#87CEFA", bd=1)
#Mise en place de la Frame

creationMenuDefault()
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


ButtonGoToRegister = tk.Button(frameLogin, text="S'enregistrer", font=("Arial", 20), bg="#DCDCDC", fg="white", command=lambda: creationFrameRegister() )
ButtonGoToRegister.grid()

frameLogin.grid(sticky='news')


#======================================================================
#------------------------Frame Register--------------------------------
#======================================================================
def register():
    User = EntryRegister.get()
    if EntryRegisterPassword.get() != EntryConfirmPassword.get():
        tk.messagebox.showwarning(title="Erreur", message="Vous n'avez pas entrez les mêmes mot de passe.")
    password = EntryRegisterPassword.get()
    password = hashlib.sha256(password.encode()).hexdigest()
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
    if('fail' in data.decode("ascii")):
        tk.messagebox.showwarning(title="Erreur", message="Erreur.")
    elif('login existant' in data.decode("ascii")):
        tk.messagebox.showwarning(title="Erreur", message="Cette identifiant existe déjà.")
    else:
        tk.messagebox.showinfo(title="Succès !", message="Votre Compte à bien été créé")
        data = donnees(data)
        ut.setDataUser(data.idUtilisateur, data.login, data.role)
        if (ut.role == "parieur"):
            creationFrameUtilisateur()
            creationMenuUser()
        elif (ut.role == "admin"):
            creationFrameAdmin()
            creationMenuAdmin()

frameRegister = tk.Frame(root, bg="#87CEFA", bd=1)

def creationFrameRegister():
    global LabelTitleRegister
    LabelTitleRegister = tk.Label(frameRegister, text="Bienvenue sur BetAppServeur", font=("Arial", 40), bg="#87CEFA", fg="white")
    LabelTitleRegister.grid(row=0, column=0)
    #Initialisation du formulaire de Register
    global LabelRegister
    LabelRegister = tk.Label(frameRegister, text="Identifiant", font=("Arial", 20), bg="#87CEFA", fg="white")
    LabelRegister.grid(row=1, column=0)

    global EntryRegister
    EntryRegister = tk.Entry(frameRegister, font=("Arial", 20), bg="#87CEFA", fg="white")
    EntryRegister.grid(row=2, column=0)

    global LabelRegisterPassword
    LabelRegisterPassword = tk.Label(frameRegister, text="Mot de Passe", font=("Arial", 20), bg="#87CEFA", fg="white")
    LabelRegisterPassword.grid(row=3, column=0)

    global EntryRegisterPassword
    EntryRegisterPassword = tk.Entry(frameRegister, font=("Arial", 20), bg="#87CEFA", fg="white", show='*')
    EntryRegisterPassword.grid(row=4, column=0)

    global LabelConfirmPassword
    LabelConfirmPassword = tk.Label(frameRegister, text="Confirmer le Mot de Passe", font=("Arial", 20), bg="#87CEFA", fg="white")
    LabelConfirmPassword.grid(row=5, column=0)

    global EntryConfirmPassword
    EntryConfirmPassword = tk.Entry(frameRegister, font=("Arial", 20), bg="#87CEFA", fg="white", show='*')
    EntryConfirmPassword.grid(row=6, column=0)

    global ButtonRegister
    ButtonRegister = tk.Button(frameRegister, text="S'enregistrer", font=("Arial", 20), bg="#DCDCDC", fg="white", command=register)
    ButtonRegister.grid(row=7, column=0)

    raise_frame(frameRegister)


#======================================================================
#-------------------------Frame Utilisateur----------------------------
#======================================================================
class utilisateur:
    def __init__(self):
        self.idUtilisateur = 0
        self.login = "default"
        self.role = "parieur"

    def setDataUser(self, id, login, role):
        self.idUtilisateur = id
        self.login = login
        self.role = role
    def destructDataUser(self):
        self.idUtilisateur = 0
        self.login = "default"
        self.role = "parieur"
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

    def ParisEnCours(self):
        User = ut.idUtilisateur
        rq = {
            "action": "afficher paris en cours",
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
        if 'fail' in repr(data):
            print("fail")
        else:
            data = donnees(data)
        return data


    def fond(self):
        User = ut.idUtilisateur
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
        data = data.decode("ascii")

        return data

ut = utilisateur()


#Mise en place de la Frame
frameUser= tk.Frame(root, bg="#87CEFA", bd=1)

def creationFrameUtilisateur():
    #Initialisation des titre
    global LabelTitleUser
    LabelTitleUser = tk.Label(frameUser, text="BetApp", font=("Arial", 40), bg="#87CEFA", fg="white")
    LabelTitleUser.grid(row=0, column=2)

    global LabelTitleRencontre
    LabelTitleRencontre = tk.Label(frameUser, text="Rencontre", font=("Arial", 20), bg="#87CEFA", fg="white")
    LabelTitleRencontre.grid(row=1, column=0)

    global LabelTitleParisEnCours
    LabelTitleParisEnCours = tk.Label(frameUser, text="Paris en cours", font=("Arial", 20), bg="#87CEFA", fg="white")
    LabelTitleParisEnCours.grid(row=1, column=3)

    #Récuperation identité
    global User
    User = ut.login

    global LabelUser
    LabelUser = tk.Label(frameUser, text=User, font=("Arial", 15), bg="#87CEFA", fg="white")
    LabelUser.grid(row=0, column=0)

    #feed + affichage des rencontres
    global rencontre
    rencontre = ut.rencontre().rencontre
    i= 0
    for i in range(len(rencontre)):
        r = donnees(json.dumps(rencontre[i]))
        values = r.nom + " le " + r.date + " à " + r.lieu
        LabelRencontre = tk.Label(frameUser, text=values, font=("Arial", 15), bg="#87CEFA", fg="white")
        LabelRencontre.grid(row=i+2, column=0)

    global ButtonParier
    ButtonParier = tk.Button(frameUser, text="Parier", font=("Arial", 15), bg="white", fg="#87CEFA", command=lambda:creationFramePari())
    ButtonParier.grid(row=i+3, column=0)

    #feed + affichage de l'historique
    global ParisEnCours
    if 'fail' in repr(ut.ParisEnCours()):
        print("fail")
    else:
        ParisEnCours = ut.ParisEnCours().paris

        for i in range(len(ParisEnCours)):
            h = donnees(json.dumps(ParisEnCours[i]))
            v = str(h.mise) + "€ miser sur  " + str(h.Challenger) + " pour un gains potentiel de " + str(h.gainPotentiel)

            LabelParisEnCours = tk.Label(frameUser, text=v, font=("Arial", 15), bg="#87CEFA", fg="white")
            LabelParisEnCours.grid(row=i + 2, column=3)

    #Affichage des fonds
    global Fond
    if str(ut.fond()) == "fail" :
        Fond =  " Fonds : 0 €"
    else:
        Fond = " Fonds : " + str(ut.fond()) + " €"

    global LabelFond
    LabelFond = tk.Label(frameUser, text=Fond, font=("Arial", 15), bg="#87CEFA", fg="white")
    LabelFond.grid(row=0, column=3)

    raise_frame(frameUser)

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
        Montant = EntryPari.get()
        Rencontre = idRencontrePari[ComboboxRencontrePari.current()]
        Challenger = LabelChoixVainqueur.get()
        User = ut.idUtilisateur
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
        if data == "success":
            tk.messagebox.showinfo(title="Pari enregistré", message="Votre pari à bien été enregistré")
            creationFrameUtilisateur()

    def challenger(self):
        Rencontre = idRencontrePari[ComboboxRencontrePari.current()]
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

def creationFramePari():
    #Initialisation des titre
    global LabelTitrePari
    LabelTitrePari = tk.Label(framePari, text="BetApp", font=("Arial", 40), bg="#87CEFA", fg="white")
    LabelTitrePari.grid(row=0, column=0, columnspan=2)

    global LabelTitreRencontre
    LabelTitreRencontre = tk.Label(framePari, text="Choisir une rencontre : ", font=("Arial", 15), bg="#87CEFA", fg="white")
    LabelTitreRencontre.grid(row=1, column=0)

    global RencontrePari
    RencontrePari = pari.rencontre().rencontre
    global nomRencontrePari
    nomRencontrePari = []
    global idRencontrePari
    idRencontrePari = []
    for rencontre in RencontrePari:
        rencontre = donnees(json.dumps(rencontre))
        nomRencontrePari.append(rencontre.nom)
        idRencontrePari.append(rencontre.id)

    if idRencontrePari == []:
        nomRencontrePari = [""]
        idRencontrePari = [""]
    global ComboboxRencontrePari
    ComboboxRencontrePari = ttk.Combobox(framePari, values=nomRencontrePari, state="readonly")
    print(dict(ComboboxRencontrePari))
    ComboboxRencontrePari.current(0)
    ComboboxRencontrePari.grid(row=1, column=1)
    def rechargeChallenger(event):
        global ValeurChallenger
        ValeurChallenger = pari.challenger().challengers
        print(ValeurChallenger)

        global LabelChallengerPari
        LabelChallengerPari = tk.Label(framePari, text="Choisir une challenger : ", font=("Arial", 15), bg="#87CEFA", fg="white")
        LabelChallengerPari.grid(row=2, column=0)

        global nomChall
        nomChall = []
        for challenger in ValeurChallenger:
            challenger = donnees(json.dumps(challenger))
            nomChall.append(challenger.nom)
        if nomChall == []:
            nomChall = [""]
        global LabelChoixVainqueur
        LabelChoixVainqueur = ttk.Combobox(framePari, values=nomChall, state="readonly")
        print(dict(LabelChoixVainqueur))
        LabelChoixVainqueur.current(0)
        LabelChoixVainqueur.grid(row=2, column=1)
    ComboboxRencontrePari.bind("<<ComboboxSelected>>", rechargeChallenger)

    global ValeurChallenger
    ValeurChallenger = pari.challenger().challengers
    print(ValeurChallenger)

    global LabelChallengerPari
    LabelChallengerPari = tk.Label(framePari, text="Choisir une challenger : ", font=("Arial", 15), bg="#87CEFA",
                                   fg="white")
    LabelChallengerPari.grid(row=2, column=0)

    global nomChall
    nomChall = []
    coteChallenger = []
    for challenger in ValeurChallenger:
        challenger = donnees(json.dumps(challenger))
        nomChall.append(challenger.nom)
        coteChallenger.append((challenger.cote))
    if nomChall == []:
        nomChall = [""]
        coteChallenger = [""]
    global LabelChoixVainqueur
    LabelChoixVainqueur = ttk.Combobox(framePari, values=nomChall, state="readonly")
    print(dict(LabelChoixVainqueur))
    LabelChoixVainqueur.current(0)
    LabelChoixVainqueur.grid(row=2, column=1)


    global LabelMontantPari
    LabelMontantPari = tk.Label(framePari, text="Choisir un montant : ", font=("Arial", 15), bg="#87CEFA", fg="white")
    LabelMontantPari.grid(row=3, column=0)

    global EntryPari
    EntryPari = tk.Entry(framePari, font=("Arial", 15), bg="#87CEFA", fg="white")
    EntryPari.grid(row=3, column=1)

    def rechargeCote(event):
        cote = " " + str(coteChallenger[LabelChoixVainqueur.current()]) + " "
        global LabelCotePariVariable
        LabelCotePariVariable = tk.Label(framePari, text=cote, font=("Arial", 15), bg="#87CEFA", fg="white")
        LabelCotePariVariable.grid(row=4, column=1)
    LabelChoixVainqueur.bind("<<ComboboxSelected>>", rechargeCote)

    global LabelCotePari
    LabelCotePari = tk.Label(framePari, text="La cote est de : ", font=("Arial", 15), bg="#87CEFA", fg="white")
    LabelCotePari.grid(row=4, column=0)
    cote = coteChallenger[LabelChoixVainqueur.current()]
    global LabelCotePariVariable
    LabelCotePariVariable = tk.Label(framePari, text=cote, font=("Arial", 15), bg="#87CEFA", fg="white")
    LabelCotePariVariable.grid(row=4, column=1)

    global ButtonPari
    ButtonPari = tk.Button(framePari, text="Parier", font=("Arial", 15), bg="white", fg="#87CEFA", command=lambda:pari.parier()).grid(row=5, column=0, columnspan=2)

    raise_frame(framePari)

#======================================================================
#-----------------------Frame visualisation compte---------------------
#======================================================================
class compte:
    def depot(self):
        print("Appel de depot")
        Montant = ComboboxDepot.get()
        User = ut.idUtilisateur
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
        data = s.recv(1024)
        data = data.decode("ascii")
        print(data)
        if 'fail' in data:
            tk.messagebox.showwarning(title="Erreur d'ajout de fonds", message="Une erreur s'est produite lors de l'ajout des fonds")
        elif 'success' in data:
            tk.messagebox.showinfo(title="Ajout de fonds", message="Votre compte à bien été crédité d'un montant de "+str(Montant)+"€")
            creationFrameCompte()
        print(rq)
        self.fond()

    def historique(self):
        print("Appel de historique")
        User = ut.idUtilisateur
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
        User = ut.idUtilisateur
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
        data = data.decode("ascii")
        return data

    def statistiques(self):
        print("Appel de statistiques")
        User = ut.idUtilisateur
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
        if 'fail' in repr(data):
            data = '{' \
                   '    "totalGain" : 0,' \
                   '    "totalParis": 0,' \
                   '    "totalVictoire": 0,' \
                   '    "Ratio" : 0' \
                   '}'
        data = donnees(data)
        return data

compteUser = compte()

#Mise en place de la Frame
frameCompte = tk.Frame(root, bg="#87CEFA", bd=1)

def creationFrameCompte():
    #Initialisation des titre
    global LabelTitreCompte
    LabelTitreCompte = tk.Label(frameCompte, text="BetApp", font=("Arial", 40), bg="#87CEFA", fg="white")
    LabelTitreCompte.grid(row=0, column=2)

    global LabelStatistique
    LabelStatistique = tk.Label(frameCompte, text="Statistique", font=("Arial", 20), bg="#87CEFA", fg="white")
    LabelStatistique.grid(row=1, column=2)

    global LabelHistorique
    LabelHistorique = tk.Label(frameCompte, text="Historique des gains", font=("Arial", 20), bg="#87CEFA", fg="white")
    LabelHistorique.grid(row=1, column=1)

    #Affichage des fonds
    global Fond
    Fond = " Fonds : " + str(compteUser.fond()) + " €"

    global LabelFond
    LabelFond = tk.Label(frameCompte, text=Fond, font=("Arial", 15), bg="#87CEFA", fg="white")
    LabelFond.grid(row=1, column=3)

    #Récuperation identité
    global User
    User = ut.login

    global LabelUser
    LabelUser = tk.Label(frameCompte, text=User, font=("Arial", 15), bg="#87CEFA", fg="white")
    LabelUser.grid(row=0, column=1)

    #feed + affichage de l'historique
    global Historique
    Historique = compteUser.historique().historique
    for i in range(len(Historique)):
        h = donnees(json.dumps(Historique[i]))
        valueHistorique = h.rencontre + " " + str(h.resultat) + " €"

        LabelRencontreUser = tk.Label(frameCompte, text=valueHistorique, font=("Arial", 15), bg="#87CEFA", fg="white")
        LabelRencontreUser.grid(row=i + 2, column=1)


    #Affichage des statistiques
    global StatPourcentVictoire
    StatPourcentVictoire = str(compteUser.statistiques().Ratio) + "%"
    global LabelStatPourcentVictoire
    LabelStatPourcentVictoire = tk.Label(frameCompte, text="Victoire : " + StatPourcentVictoire, font=("Arial", 15), bg="#87CEFA", fg="white")
    LabelStatPourcentVictoire.grid(row=2, column=2)

    global StatTotalGains
    StatTotalGains = str(compteUser.statistiques().totalGain) + " €"
    global LabelStatTotalGains
    LabelStatTotalGains = tk.Label(frameCompte, text="Total des Gains : " + StatTotalGains, font=("Arial", 15), bg="#87CEFA", fg="white")
    LabelStatTotalGains.grid(row=3, column=2)

    global StatNombreParis
    StatNombreParis = str(compteUser.statistiques().totalParis)
    global LabelStatNombreParis
    LabelStatNombreParis = tk.Label(frameCompte, text="Nombre de paris : " + StatNombreParis, font=("Arial", 15), bg="#87CEFA", fg="white")
    LabelStatNombreParis.grid(row=4, column=2)

    global ComboboxDepot
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

    global ButtonDepot
    ButtonDepot = tk.Button(frameCompte, text="Déposer", font=("Arial", 15), bg="white", fg="#87CEFA", command=lambda:compteUser.depot())
    ButtonDepot.grid(row=6, column=2)

    raise_frame(frameCompte)


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

def creationFrameAdmin():
    #Initialisation des titre
    global LabelTitleAdmin
    LabelTitleAdmin = tk.Label(frameAdmin, text="BetApp", font=("Arial", 40), bg="#87CEFA", fg="white")
    LabelTitleAdmin.grid(row=0, column=1, columnspan=2)

    global LabelTitleRencontreAdmin
    LabelTitleRencontreAdmin = tk.Label(frameAdmin, text="Rencontre", font=("Arial", 20), bg="#87CEFA", fg="white")
    LabelTitleRencontreAdmin.grid(row=2, column=1, columnspan=2)

    #Récuperation identité
    global User
    User = "Admin"

    global LabelUserAdmin
    LabelUserAdmin = tk.Label(frameAdmin, text=User, font=("Arial", 15), bg="#87CEFA", fg="white")
    LabelUserAdmin.grid(row=0, column=0)

    ## Rencontre
    #feed + affichage des rencontres
    global rencontreAdmin
    rencontreAdmin = admin.rencontre().rencontre
    i = 0
    for i in range(len(rencontreAdmin)):
        r = donnees(json.dumps(rencontreAdmin[i]))
        valuesRencontreAdmin = r.nom + " le " + r.date + " à " + r.lieu

        labelRencontreAdmin = tk.Label(frameAdmin, text=valuesRencontreAdmin, font=("Arial", 15), bg="#87CEFA", fg="white")
        labelRencontreAdmin.grid(row=i+3, column=1, columnspan=2)

    ButtonCancel = tk.Button(frameAdmin, text="Annulé", font=("Arial", 15), bg="white", fg="#87CEFA", command=lambda:creationFrameCancel())
    ButtonCancel.grid(row=i + 4, column=1)
    ButtonWinner = tk.Button(frameAdmin, text="Choisir un Vainqueur", font=("Arial", 15), bg="white", fg="#87CEFA", command=lambda: creationFrameVainqueur())
    ButtonWinner.grid(row=i + 4, column=2)

    raise_frame(frameAdmin)

# =====================================================================
# -------------------------Annulé Rencontre----------------------------
# =====================================================================
class cancel:
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

    def annule(self):
        idRencontre = idRencontrePariAdmin[ComboboxRencontrePariAdmin.current()]

        rq = {
            "action": "annuler rencontre",
            "rencontre": idRencontre
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
        if ('success' in data.decode("ascii")):
            tk.messagebox.showinfo(title="Succès", message="Annulation de la rencontre effectué avec succès.")
        elif ('fail' in data.decode("ascii")):
            tk.messagebox.showwarning(title="Erreur", message="Echec de l'annulation de la rencontre.")

cancel = cancel()

frameCancel = tk.Frame(root, bg="#87CEFA", bd=1)

def creationFrameCancel():
    global LabelTitleAnnulation
    LabelTitleAnnulation = tk.Label(frameCancel, text="BetApp", font=("Arial", 40), bg="#87CEFA", fg="white")
    LabelTitleAnnulation.grid(row=0, column=0)

    global RencontrePariAdmin
    RencontrePariAdmin = cancel.rencontre().rencontre
    global nomRencontrePariAdmin
    nomRencontrePariAdmin = []
    global idRencontrePariAdmin
    idRencontrePariAdmin = []
    for rencontre in RencontrePariAdmin:
        rencontre = donnees(json.dumps(rencontre))
        nomRencontrePariAdmin.append(rencontre.nom)
        idRencontrePariAdmin.append(rencontre.id)

    if idRencontrePariAdmin == []:
        nomRencontrePariAdmin = [""]
        idRencontrePariAdmin = [""]
    global ComboboxRencontrePariAdmin
    ComboboxRencontrePariAdmin = ttk.Combobox(frameCancel, values=nomRencontrePariAdmin, state="readonly")
    print(dict(ComboboxRencontrePariAdmin))
    ComboboxRencontrePariAdmin.current(0)
    ComboboxRencontrePariAdmin.grid(row=1, column=0)

    global ButtonAnnuleRencontre
    ButtonAnnuleRencontre = tk.Button(frameCancel, text="Annuler", font=("Arial", 15), bg="white", fg="#87CEFA", command=lambda : cancel.annule())
    ButtonAnnuleRencontre.grid(row=2, column=0)

    raise_frame(frameCancel)

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
        data = s.recv(9999)
        s.close()
        print(repr(data), 'Reçue')
        print(rq)
        if 'fail' in repr(data):
            data = '{' \
                   '   "challengers" : []' \
                   '}'
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
        challenger1 = idChallengerAdmin[LabelChoixChallenger1.current()]
        challenger2 = idChallengerAdmin2[LabelChoixChallenger2.current()]
        cote_challenger1 = EntryCoteChallenger1.get()
        cote_challenger2 =  EntryCoteChallenger2.get()
        date = EntryDateRencontre.get()
        lieu = EntryLieuRencontre.get()
        if discipline == ''  or rencontre == ''  or challenger1 == ''  or challenger2 == ''  or cote_challenger1 == ''  or cote_challenger2 == ''  or date == ''  or lieu == '' :
            tk.messagebox.showwarning(title="Erreur", message="Veuillez remplir tous les champs.")
        else :
            if challenger1 ==  challenger2 :
                tk.messagebox.showwarning(title="Erreur", message="Veuillez Choisir deux challengers différents.")
            else :
                rq = {
                    "action": "ajout rencontre",
                    "admin" : 7,
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
                data = s.recv(1024)
                s.close()
                print(repr(data), 'Reçue')
                print(rq)
                if ('success' in data.decode("ascii")):
                    tk.messagebox.showinfo(title="Succès", message="Ajout de la rencontre effectué avec succès.")
                elif ('fail' in data.decode("ascii")):
                    tk.messagebox.showwarning(title="Erreur", message="Echec de l'ajout de la rencontre.")
ajout = Rencontre()

frameAjout = tk.Frame(root, bg="#87CEFA", bd=1)
## Ajout d'une rencontre
#Nom rencontre
def creationFrameAjout():
    global LabelTitleRencontre
    LabelTitleRencontre = tk.Label(frameAjout, text="BetApp", font=("Arial", 40), bg="#87CEFA", fg="white")
    LabelTitleRencontre.grid(row=0, column=5)

    global LabelNomRencontre
    LabelNomRencontre = tk.Label(frameAjout, text="Nom de la Rencontre :", font=("Arial", 15), bg="#87CEFA", fg="white")
    LabelNomRencontre.grid(row=3, column=4)
    global EntryNomRencontre
    EntryNomRencontre = tk.Entry(frameAjout, font=("Arial", 15), bg="#87CEFA", fg="white")
    EntryNomRencontre.grid(row=4, column=4)

    #Date Rencontre
    global LabelDateRencontre
    LabelDateRencontre = tk.Label(frameAjout, text="Date de la Rencontre :", font=("Arial", 15), bg="#87CEFA", fg="white")
    LabelDateRencontre.grid(row=5, column=4)
    global EntryDateRencontre
    EntryDateRencontre = tk.Entry(frameAjout, font=("Arial", 15), bg="#87CEFA", fg="white")
    EntryDateRencontre.grid(row=6, column=4)

    #Lieu Rencontre
    global LabelLieuRencontre
    LabelLieuRencontre = tk.Label(frameAjout, text="Lieux de la Rencontre :", font=("Arial", 15), bg="#87CEFA", fg="white")
    LabelLieuRencontre.grid(row=7, column=4)
    global EntryLieuRencontre
    EntryLieuRencontre = tk.Entry(frameAjout, font=("Arial", 15), bg="#87CEFA", fg="white")
    EntryLieuRencontre.grid(row=8, column=4)

    #Challenger
    global valeurChallengerAdmin
    valeurChallengerAdmin = ajout.challenger().challengers
    global nomChallAdmin
    nomChallAdmin = []
    global idChallengerAdmin
    idChallengerAdmin = []
    for challenger in valeurChallengerAdmin:
        challenger = donnees(json.dumps(challenger))
        nomChallAdmin.append(challenger.nom)
        idChallengerAdmin.append(challenger.id)

    global LabelChoixChallenger1
    LabelChoixChallenger1 = ttk.Combobox(frameAjout, values=nomChallAdmin, state="readonly")
    print(dict(LabelChoixChallenger1))
    LabelChoixChallenger1.current(0)
    LabelChoixChallenger1.grid(row=9, column=4)

    global LabelCoteChallenger1
    LabelCoteChallenger1 = tk.Label(frameAjout, text="Cote du challenger :", font=("Arial", 17), bg="#87CEFA", fg="white")
    LabelCoteChallenger1.grid(row=10, column=4)

    global EntryCoteChallenger1
    EntryCoteChallenger1 = tk.Entry(frameAjout, font=("Arial", 15), bg="#87CEFA", fg="white")
    EntryCoteChallenger1.grid(row=11, column=4)

    global LabelVs
    LabelVs = tk.Label(frameAjout, text="VS", font=("Arial", 17), bg="#87CEFA", fg="white")
    LabelVs.grid(row=9, column=5)

    global valeurChallenger2Admin
    valeurChallenger2Admin = ajout.challenger().challengers
    global nomChallAdmin2
    nomChallAdmin2 = []
    global idChallengerAdmin2
    idChallengerAdmin2 = []
    for challenger in valeurChallenger2Admin:
        challenger = donnees(json.dumps(challenger))
        nomChallAdmin2.append(challenger.nom)
        idChallengerAdmin2.append(challenger.id)

    global LabelChoixChallenger2
    LabelChoixChallenger2 = ttk.Combobox(frameAjout, values=nomChallAdmin2, state="readonly")
    print(dict(LabelChoixChallenger2))
    LabelChoixChallenger2.current(0)
    LabelChoixChallenger2.grid(row=9, column=6)

    global LabelCoteChallenger2
    LabelCoteChallenger2 = tk.Label(frameAjout, text="Cote du challenger :", font=("Arial", 17), bg="#87CEFA", fg="white")
    LabelCoteChallenger2.grid(row=10, column=6)

    global EntryCoteChallenger2
    EntryCoteChallenger2 = tk.Entry(frameAjout, font=("Arial", 15), bg="#87CEFA", fg="white")
    EntryCoteChallenger2.grid(row=11, column=6)

    #Discipline
    global LabelDiscipline
    LabelDiscipline = tk.Label(frameAjout, text="Choix de la Discipline :", font=("Arial", 15), bg="#87CEFA", fg="white")
    LabelDiscipline.grid(row=4, column=6)
    global valueDiscipline
    valueDiscipline = ajout.discipline().disciplines
    global Discipline
    Discipline = []
    global idDiscipline
    idDiscipline = []
    for discipline in valueDiscipline:
        discipline = donnees(json.dumps(discipline))
        Discipline.append(discipline.nom)
        idDiscipline.append(discipline.id)

    global LabelChoixDiscipline
    LabelChoixDiscipline = ttk.Combobox(frameAjout, values=Discipline, state="readonly")
    print(dict(LabelChoixDiscipline))
    LabelChoixDiscipline.current(0)
    LabelChoixDiscipline.grid(row=5, column=6)


    #bouton ajout
    ButtonAjoutRencontre = tk.Button(frameAjout, text="Ajouter", font=("Arial", 15), bg="white", fg="#87CEFA", command=lambda : ajout.ajoutRencontre())
    ButtonAjoutRencontre.grid(row=12, column=5)

    raise_frame(frameAjout)

#======================================================================
#---------------------------Choix Vainqueur----------------------------
#======================================================================
class Vainqueur:

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
        Rencontre = idRencontreVainqueur[ComboboxRencontreVainqueur.current()]
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
        Rencontre = idRencontreVainqueur[ComboboxRencontreVainqueur.current()]
        rq = {
            "action": "choisir vainqueur",
            "rencontre": Rencontre,
            "challenger": idVainqueur[ComboboxVainqueur.current()]
        }
        print(idVainqueur[ComboboxVainqueur.current()])
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
frameVainqueur= tk.Frame(root, bg="#87CEFA", bd=1)
def creationFrameVainqueur():
    global LabelTitleVainqueur
    LabelTitleVainqueur = tk.Label(frameVainqueur, text="BetApp", font=("Arial", 40), bg="#87CEFA", fg="white")
    LabelTitleVainqueur.grid(row=0, column=0)

    #Choix Rencontre
    global LabelRencontreVainqueur
    LabelRencontreVainqueur = tk.Label(frameVainqueur, text="Choisir un Vainqueur", font=("Arial", 15), bg="#87CEFA", fg="white")
    LabelRencontreVainqueur.grid(row=1, column=0)
    global RencontreVainqueur
    RencontreVainqueur = vainqueur.rencontre().rencontre
    global nomRencontreVainqueur
    nomRencontreVainqueur = []
    global idRencontreVainqueur
    idRencontreVainqueur = []
    for rencontreVainqueur in RencontreVainqueur:
        rencontreVainqueur = donnees(json.dumps(rencontreVainqueur))
        nomRencontreVainqueur.append(rencontreVainqueur.nom)
        idRencontreVainqueur.append(rencontreVainqueur.id)
    if (nomRencontreVainqueur == []):
        nomRencontreVainqueur = [""]
    global ComboboxRencontreVainqueur
    ComboboxRencontreVainqueur = ttk.Combobox(frameVainqueur, values=nomRencontreVainqueur, state="readonly")
    print(dict(ComboboxRencontreVainqueur))
    ComboboxRencontreVainqueur.current(0)
    ComboboxRencontreVainqueur.grid(row=2, column=0)

    def rechargeChallenger(event):
        global LabelChoixRencontreVainqueur
        LabelChoixRencontreVainqueur = tk.Label(frameVainqueur, )
        # Choix Vainqueur
        global Challengers
        Challengers = vainqueur.challenger().challengers
        global nomVainqueur
        nomVainqueur = []
        global idVainqueur
        idVainqueur = []
        for challenger in Challengers:
            challenger = donnees(json.dumps(challenger))
            nomVainqueur.append(challenger.nom)
            idVainqueur.append(challenger.id)

        if (nomVainqueur == []):
            nomVainqueur = [""]

        global ComboboxVainqueur
        ComboboxVainqueur = ttk.Combobox(frameVainqueur, values=nomVainqueur, state="readonly")
        print(dict(ComboboxVainqueur))
        ComboboxVainqueur.current()
        ComboboxVainqueur.grid(row=3, column=0)
    ComboboxRencontreVainqueur.bind("<<ComboboxSelected>>", rechargeChallenger)

    global LabelChoixRencontreVainqueur
    LabelChoixRencontreVainqueur = tk.Label(frameVainqueur, )
    # Choix Vainqueur
    global Challengers
    Challengers = vainqueur.challenger().challengers
    global nomVainqueur
    nomVainqueur = []
    global idVainqueur
    idVainqueur = []
    for challenger in Challengers:
        challenger = donnees(json.dumps(challenger))
        nomVainqueur.append(challenger.nom)
        idVainqueur.append(challenger.id)

    if (nomVainqueur == []):
        nomVainqueur = [""]

    global ComboboxVainqueur
    ComboboxVainqueur = ttk.Combobox(frameVainqueur, values=nomVainqueur, state="readonly")
    print(dict(ComboboxVainqueur))
    ComboboxVainqueur.current()
    ComboboxVainqueur.grid(row=3, column=0)


    #Bouton
    global btnVainqueur
    btnVainqueur = tk.Button(frameVainqueur, text="Vainqueur", font=("Arial", 15), bg="white", fg="#87CEFA", command=lambda :vainqueur.envoiVainqueur())
    btnVainqueur.grid(row=4, column=0)

    raise_frame(frameVainqueur)

#======================================================================
#-------------Assemblage des frames, génération de la page-------------
#======================================================================

for frame in (frameLogin, frameUser, frameCompte, framePari, frameAdmin, frameVainqueur, frameRegister, frameAjout, frameCancel):
    frame.grid(row=0, column=0, sticky='news')

#======================================================================
#-----------------------fonction de gestion----------------------------
#======================================================================
def deconnexion():
    ut.destructDataUser()
    EntryLogin.delete(0, 'end')
    EntryPassword.delete(0, 'end')
    creationMenuDefault()
    raise_frame(frameLogin)

raise_frame(frameLogin)
root.mainloop()

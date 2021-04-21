from tkinter import *

window = Tk()

# Initialisation de la fenetre
window.title("BetApp")
window.geometry("1080x720")
window.minsize(480,360)
window.config(background="#87CEFA")

#Mise en place de la Frame
frame = Frame(window, bg="#87CEFA", bd=1)

#Logo
window.iconbitmap("logo.ico")

#Initialisation du titre
label_title = Label(frame, text="Bienvenue sur BetAppServeur", font=("Arial", 40), bg="#87CEFA", fg="white")
label_title.pack()

#Initialisation du formulaire
label_login = Label(frame, text="Login", font=("Arial", 20), bg="#87CEFA", fg="white")
label_login.pack()

entry_login = Entry(frame, font=("Arial", 20), bg="#87CEFA", fg="white")
entry_login.pack()

label_mdp = Label(frame, text="Mot de Passe", font=("Arial", 20), bg="#87CEFA", fg="white")
label_mdp.pack()

entry_mdp = Entry(frame, font=("Arial", 20), bg="#87CEFA", fg="white")
entry_mdp.pack()

log_button = Button(frame, text="Login", font=("Arial", 20), bg="#DCDCDC", fg="white")
log_button.pack(pady=25, fill=X)

frame.pack(expand=YES)

#Ajout du Menu Bar
Menu_bar = Menu(window)

action_menu = Menu(Menu_bar, tearoff=0)
action_menu.add_command(label="Mon Compte")
action_menu.add_command(label="Quitter", command=window.quit)

Menu_bar.add_cascade(label="Action", menu=action_menu)


admin_menu = Menu(Menu_bar, tearoff=0)
admin_menu.add_command(label="Administrer")

Menu_bar.add_cascade(label="Administrateur", menu=admin_menu)

window.config(menu=Menu_bar)

#Empacketage de la fenetre
window.mainloop()
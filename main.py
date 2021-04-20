from tkinter import *

window = Tk()

window.title("BetAppServeur")
window.geometry("1080x720")
window.minsize(480,360)

frame = Frame(window, bg="#87CEFA", bd=1)

#Logo
#window.iconbitmap("logo.ico")
window.config(background="#87CEFA")

label_title = Label(frame, text="Bienvenue sur BetAppServeur", font=("Arial", 40), bg="#87CEFA", fg="white")
label_title.pack()

label_login = Label(frame, text="Login", font=("Arial", 20), bg="#87CEFA", fg="white")
label_login.pack()

entry_login = Entry(frame, font=("Arial", 20), bg="#87CEFA", fg="white")
entry_login.pack()

label_mdp = Label(frame, text="Mot de Passe", font=("Arial", 20), bg="#87CEFA", fg="white")
label_mdp.pack()

entry_mdp = Entry(frame, font=("Arial", 20), bg="#87CEFA", fg="white")
entry_mdp.pack()

log_button = Button(frame, text="Login", font=("Arial", 20), bg="white", fg="#87CEFA")
log_button.pack(pady=25, fill=X)

frame.pack(expand=YES)

window.mainloop()
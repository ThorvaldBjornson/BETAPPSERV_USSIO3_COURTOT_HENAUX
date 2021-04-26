from tkinter import *

def clean_exit():
    root.destroy()

def alternate_window(is_in_root, is_in_window, window):
    def alternate_processing():
        if is_in_root and not is_in_window:
            app.withdraw()
            window.deiconify()
        else:
            window.withdraw()
            app.deiconify()

    return alternate_processing

def create_window(window, text_label):
    label = Label(window, text=text_label)
    button = Button(window, text="Revenir vers root", command=alternate_window(False, True, window))
    label.grid(column=0, row=0)
    button.grid(column=0, row=1)
    window.protocol("WM_DELETE_WINDOW", clean_exit)

#Instanciation de Tkinter
app = Tk()

frame = Frame(app, bg="#87CEFA", bd=1)

#Configuration de la page
app.title("BetApp")
app.geometry("1280x720")
app.minsize(480,360)

#Logo
app.iconbitmap("logo.ico")
app.config(background="#87CEFA")

#Création des pages

login_window = Toplevel(app)
user_window = Toplevel(app)
deposit_window = Toplevel(app)
admin_window = Toplevel(app)

create_window(login_window, "Je suis dans la fenetre login")
create_window(user_window, "Je suis dans la fenetre user")
create_window(deposit_window, "Je suis dans la fenetre deposit")
create_window(admin_window, "Je suis dans la fenetre admin")

login_window.withdraw()
user_window.withdraw()
deposit_window.withdraw()
admin_window.withdraw()

login_window = Button(app, command=alternate_window(True, False, login_window), text="affiche fenetre login")
user_window = Button(app, command=alternate_window(True, False, user_window), text="affiche fenetre user")
deposit_window = Button(app, command=alternate_window(True, False, deposit_window), text="affiche fenetre deposit")
admin_window = Button(app, command=alternate_window(True, False, admin_window), text="affiche fenetre admin")

login_window.grid()
user_window.grid(column=1, row=0)
deposit_window.grid(column=2, row=0)
admin_window.grid(column=3, row=0)



app.mainloop()
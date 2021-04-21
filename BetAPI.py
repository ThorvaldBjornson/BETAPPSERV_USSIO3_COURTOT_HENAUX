#!/usr/bin/python
import socket

serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serveur.bind(('', 9999))
serveur.listen(1)
client, adresseClient = serveur.accept()
print('Connexion de ', adresseClient)
donnees = client.recv(1024).decode('ascii')
if not donnees:
	print('Erreur de reception.')
else:
	print('Reception de :' + donnees)
	reponse = donnees.upper()
	print('Envoi de : ' + reponse)
	n = client.send(reponse.encode("ascii"))
	if(n != len(reponse)):
		print('Erreur envoi.')
	else:
		print('Envoi ok.')
print('Fermeture de la connexion avec le client.')
client.close()
print('Arret du serveur.')
serveur.close()

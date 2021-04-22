#!/usr/bin/python3.7
import socket
import json
import mariadb
import sys

#connection bdd
try:
	conn = mariadb.connect(
		user="BetAppUser",
		password="perrier",
		host="localhost",
		port=3306,
		database="BetApp"
		)
except mariadb.Error as e:
	print(f"Error connecting to MariaDB Platform: {e}")
	sys.exit(1)
cur = conn.cursor()

#objet pour transformer du JSON_string en objet
class JSONtoOBJ:
	def __init__(self, data):
		self.__dict__ = json.loads(data)


#echange client-serveur
serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serveur.bind(('', 9999))
while True:
	serveur.listen(1)
	client, adresseClient = serveur.accept()
	print('Connexion de ', adresseClient)
	donnees = client.recv(1024).decode('ascii')
	if not donnees:
		print('Erreur de reception.')
	else:
		donnees = JSONtoOBJ(donnees)
		print('action requise par l\'utilisateur :' + donnees.action)
		if(donnees.action == 'connection'):
			print('identifiant = ' + donnees.login)
			print('mot de passe = ' + donnees.password)
			cur.execute("SELECT login, motDePasse FROM UTILISATEUR")
			reponse = 'failed to login.'
			for(login, motDePasse) in cur:
				if(login == donnees.login and motDePasse == donnees.password):
					reponse = 'login success !'
			n = client.send(reponse.encode("ascii"))
		elif(donnees.action == 'afficher rencontre'):
			cur.execute("SELECT nom, lieu, dateRencontre FROM RENCONTRE")
			rencontre = []
			for(nom, lieu, dateRencontre) in cur:
				rencontre.append({"nom" : nom, "lieu" : lieu, "date" : str(dateRencontre)})
			reponse = 	{
						"rencontre" : rencontre
					}
			n = client.send(json.dumps(reponse).encode("ascii"))
		else:
			reponse = donnees.upper()
			print('Envoi de : ' + reponse)
			n = client.send(reponse.encode("ascii"))
		#if(n != len(reponse):
			#print('Erreur envoi.')
		#else:
			#print('Envoi ok.')
	print('Fermeture de la connexion avec le client.')
	client.close()
print('Arret du serveur.')
serveur.close()


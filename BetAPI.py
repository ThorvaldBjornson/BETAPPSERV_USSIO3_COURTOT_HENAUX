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
conn.autocommit = False
#objet pour transformer du JSON_string en objet
class JSONtoOBJ:
	def __init__(self, data):
		self.__dict__ = json.loads(data)


#echange client-serveur
serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serveur.bind(('', 9999))
while True:
	serveur.listen(100)
	client, adresseClient = serveur.accept()
	print('Connexion de ', adresseClient)
	donnees = client.recv(1024).decode('ascii')
	if not donnees:
		print('Erreur de reception.')
	else:
		donnees = JSONtoOBJ(donnees)
		print('action requise par l\'utilisateur :' + donnees.action)
		if(donnees.action == 'connection'):
			try:
				print('identifiant = ' + donnees.login)
				print('mot de passe = ' + donnees.password)
				cur.execute("SELECT login, motDePasse FROM UTILISATEUR")
				reponse = 'failed to login.'
				for(login, motDePasse) in cur:
					if(login == donnees.login and motDePasse == donnees.password):
						reponse = 'login success !'
				n = client.send(reponse.encode("ascii"))
			except:
				print('login failed')
				message_client = 'fail'
				n = client.send(message_client.encode("ascii"))
		elif(donnees.action == 'afficher rencontre'):
			try:
				cur.execute("SELECT idRencontre, nom, lieu, dateRencontre FROM RENCONTRE")
				rencontre = []
				for(idRencontre, nom, lieu, dateRencontre) in cur:
					rencontre.append({"id" : idRencontre, "nom" : nom, "lieu" : lieu, "date" : str(dateRencontre)})
				reponse = 	{
							"rencontre" : rencontre
						}
				n = client.send(json.dumps(reponse).encode("ascii"))
			except:
				print('envoi des rencontres failed')
				message_client = 'fail'
				n = client.send(message_client.encode("ascii"))
		elif(donnees.action == 'parier'):
			try:
				cur.execute("SELECT porteMonnaie FROM PARIEUR WHERE idParieur = " + str(donnees.utilisateur))
				for(porteMonnaie) in cur:
					miseMaximum = porteMonnaie[0]
				if(float(donnees.montant) <= miseMaximum):
					cur.execute("SELECT idChallenger FROM CHALLENGER WHERE nom = \'"+ str(donnees.challenger) + "\'")
					for(idChallenger) in cur:
						challenger = idChallenger[0]
					print("INSERT INTO PARI (mise, idChallenger, idParieur) VALUES (" + str(donnees.montant) + ", " + str(challenger) + ", " + str(donnees.utilisateur) + ")")
					cur.execute("INSERT INTO PARI (mise, idChallenger, idParieur) VALUES ("+ str(donnees.montant) + ", "+ str(challenger) + ", " + str(donnees.utilisateur) + ")")
					conn.commit()
					print(cur.lastrowid)
					cur.execute("INSERT INTO RENCONTRE_PARI (idPari, idRencontre) VALUES ("+ str(cur.lastrowid) + ", "+ str(donnees.rencontre) + ")")
					cur.execute("UPDATE PARIEUR SET nombreParis = nombreParis + 1, porteMonnaie = porteMonnaie - "+ str(donnees.montant) +" WHERE idParieur = " + str(donnees.utilisateur))
					conn.commit()
					message_client = 'success'
					print(message_client)
					n = client.send(message_client.encode("ascii"))
				else:
					message_client = "fail"
					n = client.send(message_client.encode("ascii"))
			except:
				print('enregistrement du pari failed')
				message_client = 'fail'
				n = client.send(message_client.encode("ascii"))
		elif(donnees.action == 'deposer'):
			try:
				cur.execute("UPDATE PARIEUR SET porteMonnaie = porteMonnaie + "+ str(donnees.montant) + " WHERE idParieur = "+ str(donnees.utilisateur))
				conn.commit()
				print('ajout des fonds success')
				message_client = 'success'
			except:
				print('ajout des fonds failed')
				message_client = 'fail'
				n = client.send(message_client.encode("ascii"))
		elif(donnees.action == 'afficher historique'):
			try:
				cur.execute("SELECT p.resultat, r.nom FROM PARI p INNER JOIN RENCONTRE_PARI rp ON rp.idPari = p.idPari INNER JOIN RENCONTRE r ON r.idRencontre = rp.idRencontre WHERE p.resultat != '' AND idParieur = " + str(donnees.utilisateur))
				historique = []
				for(resultat, nom) in cur:
					historique.append({"resultat" : resultat, "rencontre" : nom})
				reponse = 	{
							"historique" : historique
						}
				print(json.dumps(reponse))
				n = client.send(json.dumps(reponse).encode("ascii"))
				print('envoi de l\'historique OK !')
			except:
				print('envoi de l\'historique failed')
				message_client = 'fail'
				n = client.send(message_client.encode("ascii"))
		elif(donnees.action == 'afficher fonds'):
			try:
				cur.execute("SELECT porteMonnaie FROM PARIEUR WHERE idParieur = " +str(donnees.utilisateur))
				for (porteMonnaie) in cur:
					reponse = {
							"fonds" : porteMonnaie[0]
					  	}
				n = client.send(json.dumps(reponse).encode("ascii"))
				print('envoi des fonds OK !')
			except:
				print('envoi des fonds failed')
				message_client = 'fail'
				client.send(message_client.encode("ascii"))
		elif(donnees.action == 'afficher stats'):
			try:
				cur.execute("SELECT SUM(resultat) as total FROM PARI WHERE idParieur = " + str(donnees.utilisateur))
				for(total) in cur:
					totalGain = total[0]
				cur.execute("SELECT COUNT(*) as nbVictoire FROM PARI WHERE statut = 'gagné' AND idParieur = " + str(donnees.utilisateur))
				for(nbVictoire) in cur:
					nombreVictoire = nbVictoire[0]
				cur.execute("SELECT nombreParis FROM PARIEUR WHERE idParieur = " + str(donnees.utilisateur))
				for(nombreParis) in cur:
					winRate = (nombreVictoire / nombreParis[0]) * 100
					totalParis = nombreParis[0]
				reponse = {
						"totalGain" : totalGain,
						"totalParis" : totalParis,
						"totalVictoire" : nombreVictoire,
						"Ratio" : winRate 
				  	  }
				n = client.send(json.dumps(reponse).encode("ascii"))
				print('envoi des stats OK !')
			except:
				print('envoi des stats failed')
				message_client = 'fail'
				client.send(message_client.encode('ascii'))
		elif(donnees.action == 'afficher challenger'):
			try:
				cur.execute("SELECT c.idChallenger, c.nom, c.pays FROM CHALLENGER c INNER JOIN RENCONTRE_CHALLENGER rc ON rc.idChallenger = c.idChallenger WHERE rc.idRencontre = "+ str(donnees.rencontre))
				resultat = []
				for(idChallenger, nom, pays) in cur:
					resultat.append({"id" : idChallenger, "nom" : nom, "pays" : pays})
				reponse = {
						"challengers" : resultat
				  	  }
				n = client.send(json.dumps(reponse).encode("ascii"))
			except:
				print('envoi des challengers failed')
				message_client = 'fail'
				client.send(message_client.encode('ascii'))
		else:
			print('action requise incomprise par le serveur')
			message_client = fail
			n = client.send(message_client.encode("ascii"))
	print('Fermeture de la connexion avec le client.')
	client.close()
print('Arret du serveur.')
serveur.close()

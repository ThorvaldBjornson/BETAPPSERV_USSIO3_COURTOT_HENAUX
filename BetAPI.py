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
				if("SELECT" in donnees.login.upper() or "SELECT" in donnees.password.upper() or "INSERT" in donnees.login.upper() or "INSERT" in donnees.password.upper() or "UPDATE" in donnees.login.upper() or "UPDATE" in donnees.password.upper() or "DELETE" in donnees.login.upper() or "DELETE" in donnees.password.upper() or "ALTER" in donnees.login.upper() or "ALTER" in donnees.password.upper()):
					reponse = 'failed to login.'
					n = client.send(reponse.encode("ascii"))
				else:
					print('identifiant = ' + donnees.login)
					print('mot de passe = ' + donnees.password)
					cur.execute("SELECT idUtilisateur, login, motDePasse FROM UTILISATEUR WHERE login = \'" + str(donnees.login + "\' AND motDePasse = \'" + str(donnees.password) + "\'"))
					reponse = 'failed to login.'
					for(idUtilisateur, login, motDePasse) in cur:
						if(login == donnees.login and motDePasse == donnees.password):
							role = 'parieur'
							cur.execute("SELECT idAdministrateur FROM ADMINISTRATEUR WHERE idAdministrateur = " + str(idUtilisateur))
							for(idAdministrateur) in cur:
								if(idAdministrateur[0] != ""):
									role = 'admin'
							reponse = {
									"idUtilisateur" : idUtilisateur,
									"login" : login,
									"role" : role
							  	  }
							reponse = json.dumps(reponse)
					n = client.send(reponse.encode("ascii"))
			except:
				print('login failed')
				message_client = 'fail'
				n = client.send(message_client.encode("ascii"))
		elif(donnees.action == 'register'):
			try:
				message_client = ""
				if("SELECT" in donnees.login.upper() or "SELECT" in donnees.password.upper() or "INSERT" in donnees.login.upper() or "INSERT" in donnees.password.upper() or "UPDATE" in donnees.login.upper() or "UPDATE" in donnees.password.upper() or "DELETE" in donnees.login.upper() or "DELETE" in donnees.password.upper() or "ALTER" in donnees.login.upper() or "ALTER" in donnees.password.upper()):
                                        message_client = 'failed to login.'
				else:
					cur.execute("SELECT login FROM UTILISATEUR WHERE login = \'"+str(donnees.login)+"\'")
					exist = False
					for(login) in cur:
						if login != "":
							exist = True
							break
					if exist:
						print('login existant')
						message_client = 'login existant'
					else:
						cur.execute("INSERT INTO UTILISATEUR (login, motDePasse) VALUES (\'"+ str(donnees.login)+"\', \'"+ str(donnees.password)+"\')")
						conn.commit()
						cur.execute("INSERT INTO PARIEUR (idParieur) VALUES ("+str(cur.lastrowid)+")")
						conn.commit()
						print('inscription success')
						message_client = {
									"idUtilisateur" : cur.lastrowid,
									"login" : str(donnees.login),
									"role" : 'parieur'
								 }
						message_client = json.dumps(message_client)
				n = client.send(message_client.encode("ascii"))
			except:
				print('inscription failed')
				message_client = 'fail'
				n = client.send(message_client.encode('ascii'))
		elif(donnees.action == 'ajout rencontre'):
			try:
				message_client = ''
				if("SELECT" in str(donnees.rencontre).upper() or "INSERT" in str(donnees.rencontre).upper() or "UPDATE" in str(donnees.rencontre).upper() or "DELETE" in str(donnees.rencontre).upper() or "ALTER" in str(donnees.rencontre).upper()):
					message_client = 'fail'
				elif("SELECT" in str(donnees.lieu).upper() or "INSERT" in str(donnees.lieu).upper() or "UPDATE" in str(donnees.lieu).upper() or "DELETE" in str(donnees.lieu).upper() or "ALTER" in str(donnees.lieu).upper()):
					message_client = 'fail'
				elif("SELECT" in str(donnees.date).upper() or "INSERT" in str(donnees.date).upper() or "UPDATE" in str(donnees.date).upper() or "DELETE" in str(donnees.date).upper() or "ALTER" in str(donnees.date).upper()):
					message_client = 'fail'
				elif("SELECT" in str(donnees.cote_challenger1).upper() or "INSERT" in str(donnees.cote_challenger1).upper() or "UPDATE" in str(donnees.cote_challenger1).upper() or "DELETE" in str(donnees.cote_challenger1).upper() or "ALTER" in str(donnees.cote_challenger1).upper()):
					message_client = 'fail'
				elif("SELECT" in str(donnees.cote_challenger2).upper() or "INSERT" in str(donnees.cote_challenger2).upper() or "UPDATE" in str(donnees.cote_challenger2).upper() or "DELETE" in str(donnees.cote_challenger2).upper() or "ALTER" in str(donnees.cote_challenger2).upper()):
					message_client = 'fail'
				else:
					cur.execute("INSERT INTO RENCONTRE (nom, lieu, dateRencontre, idDiscipline, idAdministrateur) VALUES (\'" + str(donnees.rencontre) +"\',\'" + str(donnees.lieu) + "\',\'" + str(donnees.date) + "\',"+ str(donnees.discipline)+", "+str(donnees.admin)+")")
					conn.commit()
					cur.execute("INSERT INTO RENCONTRE_CHALLENGER (idRencontre, idChallenger, cote) VALUES ("+str(cur.lastrowid)+", "+str(donnees.challenger1)+", "+str(donnees.cote_challenger1)+"), ("+ str(cur.lastrowid) +", "+str(donnees.challenger2)+", "+str(donnees.cote_challenger2)+")")
					conn.commit()
					print('creation de la rencontre ok')
					message_client = "success"
				n = client.send(message_client.encode("ascii"))
			except:
				print('enregistrement de la rencontre failed')
				message_client = 'fail'
				n = client.send(message_client.encode("ascii"))
		elif(donnees.action == 'afficher rencontre'):
			try:
				cur.execute("SELECT idRencontre, nom, lieu, dateRencontre FROM RENCONTRE WHERE termine = 0")
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
		elif(donnees.action == "afficher paris en cours"):
			try:
				cur.execute("SELECT p.idPari, p.mise, p.gainPotentiel, c.nom as challenger FROM PARI p INNER JOIN CHALLENGER c ON c.idChallenger = p.idChallenger WHERE p.statut = 'attente' AND p.idParieur = "+ str(donnees.utilisateur))
				resultat = []
				for(idPari, mise, gainPotentiel, challenger) in cur:
					resultat.append({"id": idPari, "mise": mise, "gainPotentiel" : gainPotentiel, "Challenger" : challenger})
				reponse = {
						"paris" : resultat
					  }
				reponse = json.dumps(reponse)
				n = client.send(reponse.encode("ascii"))
				print('envoi de la liste des paris success')
			except:
				print('envoi de la liste des paris failed')
				message_client = 'fail'
				n = client.send(message_client.encode("ascii"))
		elif(donnees.action == 'parier'):
			try:
				if("SELECT" in str(donnees.montant).upper() or "INSERT" in str(donnees.montant).upper() or "UPDATE" in str(donnees.montant).upper() or "DELETE" in str(donnees.montant).upper() or "ALTER" in str(donnees.montant).upper()):
					message_client = 'pari failed'
					n = client.send(message_client.encode("ascii"))
				else:
					cur.execute("SELECT porteMonnaie FROM PARIEUR WHERE idParieur = " + str(donnees.utilisateur))
					for(porteMonnaie) in cur:
						miseMaximum = porteMonnaie[0]
					if(float(donnees.montant) <= miseMaximum):
						cur.execute("SELECT c.idChallenger, rc.cote FROM CHALLENGER c INNER JOIN RENCONTRE_CHALLENGER rc ON rc.idChallenger = c.idChallenger WHERE c.nom = \'"+ str(donnees.challenger) + "\' AND rc.idRencontre = " + str(donnees.rencontre))
						for(idChallenger, cote) in cur:
							challenger = idChallenger
							cote = cote
						gainPotentiel = float(donnees.montant) * cote
						print("INSERT INTO PARI (mise, idChallenger, idParieur, gainPotentiel) VALUES (" + str(donnees.montant) + ", " + str(challenger) + ", " + str(donnees.utilisateur) + ", "+str(gainPotentiel)+")")
						cur.execute("INSERT INTO PARI (mise, idChallenger, idParieur, gainPotentiel) VALUES ("+ str(donnees.montant) + ", "+ str(challenger) + ", " + str(donnees.utilisateur) + ", "+str(gainPotentiel)+")")
						conn.commit()
						print(cur.lastrowid)
						cur.execute("INSERT INTO RENCONTRE_PARI (idPari, idRencontre) VALUES ("+ str(cur.lastrowid) + ", "+ str(donnees.rencontre) + ")")
						cur.execute("UPDATE PARIEUR SET nombreParis = nombreParis + 1, porteMonnaie = porteMonnaie - "+ str(donnees.montant) +" WHERE idParieur = " + str(donnees.utilisateur))
						conn.commit()
						message_client = 'success'
						print(message_client)
						n = client.send(message_client.encode("ascii"))
					else:
						print('pari failed')
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
				n = client.send(message_client.encode("ascii"))
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
					reponse = str(porteMonnaie[0])
				if(reponse == ""):
					reponse = '0'
				n = client.send(reponse.encode("ascii"))
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
		elif(donnees.action == "afficher all challenger"):
			try:
				cur.execute("SELECT idChallenger, nom FROM CHALLENGER")
				resultat = []
				for (idChallenger, nom) in cur:
					resultat.append({"id" : idChallenger, "nom": nom})
				message_client =   	{
								"challengers" : resultat
							}
				print('envoi de la liste des challengers success')
				n = client.send(json.dumps(message_client).encode("ascii"))
			except:
				print('envoi de la liste des challengers failed')
				message_client = 'fail'
				n = client.send(message_client.encode("ascii"))
		elif(donnees.action == "afficher discipline"):
			try:
				cur.execute("SELECT idDiscipline, nom FROM DISCIPLINE")
				resultat = []
				for(idDiscipline, nom) in cur:
					resultat.append({"id" : idDiscipline, "nom" : nom})
				message_client = 	{
								"disciplines" : resultat
							}
				print('envoi de la liste des disciplines success')
				n = client.send(json.dumps(message_client).encode("ascii"))
			except:
				print('envoi de la liste des disciplines failed')
				message_client = 'fail'
				n = client.send(message_client.encode("ascii"))
		elif(donnees.action == "choisir vainqueur"):
			try:
				cur.execute("UPDATE RENCONTRE SET gagnant = "+ str(donnees.challenger)+ ", termine = 1 WHERE idRencontre = " + str(donnees.rencontre))
				cur.execute("UPDATE PARI p INNER JOIN RENCONTRE_PARI rp ON p.idPari = rp.idPari INNER JOIN PARIEUR pr ON p.idParieur = pr.idParieur SET p.statut = CASE WHEN p.idChallenger = "+ str(donnees.challenger)+" THEN 'gagné' ELSE 'perdu'END,  p.resultat = CASE WHEN p.idChallenger = "+str(donnees.challenger)+" p.gainPotentiel ELSE 0 - p.mise END, pr.porteMonnaie = CASE WHEN p.idChallenger = "+str(donnees.challenger)+" THEN pr.porteMonnaie + mise + p.gainPotentiel  ELSE pr.porteMonnaie END WHERE rp.idRencontre = " + str(donnees.rencontre))
				conn.commit()
				print('enregistrement du vainqueur success')
				message_client = 'success'
				n = client.send(message_client.encode("ascii"))
			except:
				print('choix du vainqueur failed')
				message_client = 'fail'
				n = client.send(message_client.encode("ascii"))
		elif(donnees.action == "annuler rencontre"):
			try:
				cur.execute("UPDATE RENCONTRE SET termine = 1 WHERE idRencontre = "+ str(donnees.rencontre))
				cur.execute("UPDATE PARI p INNER JOIN RENCONTRE_PARI rp ON rp.idPari = p.idPari INNER JOIN PARIEUR pr ON pr.idParieur = p.idParieur SET p.statut = 'annulé', p.resultat = 0, pr.porteMonnaie = pr.porteMonnaie + p.mise WHERE rp.idRencontre = "+ str(donnees.rencontre))
				conn.commit()
				print('annulation de la rencontre OK!')
				message_client = 'success'
				n = client.send(message_client.encode("ascii"))
			except:
				print('annulation de la rencontre failed')
				message_client = 'fail'
				n = client.send(message_client.encode("ascii"))
		else:
			print('action requise incomprise par le serveur')
			message_client = 'fail'
			n = client.send(message_client.encode("ascii"))
	print('Fermeture de la connexion avec le client.')
	client.close()
print('Arret du serveur.')
serveur.close()

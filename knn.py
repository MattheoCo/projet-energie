import tkinter as tk
#label.configure(text="Cela fait "+str(valeur)+" MegaWatt")

def lecture(fichier):
    """Prend en parametre un fichier, et renvoie un tableau des lignes du fichier."""
    tableau = []
    memoire = []
    with open(fichier, 'r') as file:
        memoire = file.readlines()
    for i in range(len(memoire)):
        tableau.append(memoire[i].split(";"))
        #On ajoute au tableau le contenu de la liste dans la variable memoire.
        #Chaque ligne ajoutee est separee en une liste a chaque point virgule.
    return tableau[1::] #On ne prend pas en compte la 1ère ligne

def estBissextile(annee):
    "Prend en parametre une annee et renvoie True si elle est bissextile, False dans le cas contraire."
    return annee % 4 == 0 #Une année est bissextile si elle est multiple de 4.

def numeroJour(date):
    """Prend en parametre une chaine de caractere au format AAAA-MM-JJ. Retourne le numero du jour correspondant a cette date. Prend en compte les annees bissextiles."""
    date = date.split('-')
    #On separe notre date en une liste
    result = 0
    if estBissextile(int(date[0])) == True:
        mois = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31] #Nombre de jours dans chaque mois si l'année est bissextile
        for i in range(0, int(date[1]) - 1):
            result += int(mois[i]) #On ajoute a la variable result le nb de jours dans chaque mois precedent celui de la date
        result += int(date[2]) #On ajoute a la variable result le nb de jours ecoules durant le mois de la date
        if result > 365:
            result -= 1
    else:
        mois = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31] #Nombre de jours dans chaque mois
        for i in range(0, int(date[1]) - 1):
            result += int(mois[i])
        result += int(date[2]) #Idem que dans les lignes au dessus
    return result

from math import *

def distance(point_I, point_J):
    """Prend en parametre deux points (tuples de trois indices). Renvoie sa distance euclidienne."""
    d1 = point_I[0] - point_J[0]
    d2 = 365 - d1
    d_final = 0
    if d1 <= d2:
        d_final = d1
    else:
        d_final = d2
    #On calcule la distance reelle entre les deux jours des points
    return sqrt((d_final)**2 + (point_I[1] - point_J[1])**2 + (point_I[2] - point_J[2])**2)


def kPlusProches(k, point, donnees):
    """Prend en argument un naturel k, un tuple (representant un point), et un jeu de donnees. Renvoie une liste triee de la distance entre les k plus proches voisins du point, et les indice dans le jeu de donnees de ces distances."""
    voisins = []
    for i in range(len(donnees)):
        d = distance(point, donnees[i])
        voisins.append((d, i))
        #On cree notre liste voisins
    voisins.sort()
    print(voisins)
    print(k)
    return [voisins[j] for j in range(k)]

def PuissanceMoyenne(tri_tuples):
    """Prend en argument une liste triee en fonction de la distance dont les elements sont des tuples (distance, indice du tableau original) et renvoie la puissance electrique moyenne des k plus proches voisins."""
    tableau_original = lecture('jeuTests.csv')
    somme = 0
    for i in range(len(tri_tuples)):
        #de 0 a la longueur de la liste soit k
        somme += float(tableau_original[tri_tuples[i][1]][1])
        #On recupere dans tableau_original la puissance moyenne a l'indice present dans tri_tuples et on convertit la sortie en float
    return somme / len(tri_tuples)

def lancerTest():
    k = valeur_k.get()
    temp_moyenne = temp_moy.get()
    temp_reference = temp_ref.get()
    date = str(val_a.get()) + "-" + str(val_m.get()) + "-" + str(val_j.get())
    #On récupère le nombre de voisins et les paramètres correspondants.
    
    date = numeroJour(date)
    user_inputs = (date, float(temp_moyenne), float(temp_reference))
    #On transforme la date et on la passe dans un tuple avec les autres données
    
    readed_file = lecture("jeuTests.csv")
    #On créé notre variable qui contient notre jeu de données.
    
    for i in range (len(readed_file)):
        del readed_file[i][1]
        readed_file[i][0] = numeroJour(readed_file[i][0])
        readed_file[i][1], readed_file[i][2] = float(readed_file[i][1]), float(readed_file[i][2])
    
    list_knn = kPlusProches(k, user_inputs, readed_file)
    print(list_knn)
    return PuissanceMoyenne(list_knn)


fenetre = tk.Tk()
#===================================
#           On assigne les paramètre de la fenètre
#===================================
fenetre.iconbitmap('icone.ico')
fenetre.title('Prévision consommation électique')
fenetre.configure(bg='#988080')

#explication de la fenètre
expliquation = tk.Label(fenetre, text="Cette fenêtre permets de choisir le nombre de voisins par 'k'.", bg='#988080')
expliquation.grid(row =1, column=0, columnspan=3)

fonction = tk.Label(fenetre, text="Ainsi que les paramètres date, température moyenne, température de référence du point à vérifier.", bg='#988080')
fonction.grid(row=2, column=0, columnspan=3)

fonction = tk.Label(fenetre, text="Ensuite il vous suffira d'appuyer sur lancer pour afficher le résultat de la consommation prévue.", bg='#988080')
fonction.grid(row=3, column=0, columnspan=3)

#attribution de k
valeur_k = tk.IntVar()
valeur_k.set(0)

entree = tk.Entry(fenetre, textvariable=valeur_k, text="entrez k ici", width=30)
entree.grid(row=4, column=1)
tk.Label(text="Nombre k", bg='#89BCB6').grid(row=6, column=1)

label = tk.Label(fenetre, text="'Choisissez vôtre nombre k ici'")
label.grid(row=5, column=1)

#attribution de la température moyenne
temperature_moy = tk.Label(fenetre, text="Entrez votre température moyenne:  ", bg='#988080').grid(row=4, column=0)
temp_moy = tk.IntVar()
temp_moy.set(0)

entree_temp_moy = tk.Entry(fenetre, textvariable=temp_moy, text="", width=30)
entree_temp_moy.grid(row=5, column=0)
tk.Label(text="Température moyenne", bg='#89BCB6').grid(row=6, column=0)

#attribution de la température de réference
temperature_de_ref = tk.Label(fenetre, text="Entrez votre température de réference:  ", bg='#988080').grid(row=4, column=2)
temp_ref = tk.IntVar()
temp_ref.set(0)

entree_temp_ref = tk.Entry(fenetre, textvariable=temp_ref, text="", width=30)
entree_temp_ref.grid(row=5, column=2)
tk.Label(text="Température de reférence", bg='#89BCB6').grid(row=6, column=2)


#scale pour jours
val_j = tk.IntVar()
scale_j=tk.Scale(fenetre, orient='vertical', from_=1, to=31, resolution=1, tickinterval=1, length=100, 
      label='jours', variable = val_j).grid(row=9, column=0)



#scale pour mois
val_m = tk.IntVar()
scale_m=tk.Scale(fenetre, orient='vertical', from_=1, to=12, resolution=1, tickinterval=1, length=100, 
      label='mois', variable = val_m).grid(row=9, column=1)


#scale pour années
val_a = tk.IntVar()
scale=a=tk.Scale(fenetre, orient='vertical', from_=2012, to=2022, resolution=1, tickinterval=1, length=100, 
      label='années', variable = val_a).grid(row=9, column=2)


#appel la fonction pour lancer
tk.Label(fenetre, text="    ", bg='#988080').grid(row=14, column=1)
tk.Button(text="Lancer le test", bg='#89BCB6', command=lancerTest).grid(row=15, column=1)

tk.Label(fenetre, text="La consomation apparait ci-dessous.", bg='#988080').grid(row=16, column=1)
label = tk.Label(fenetre, text="Ce message sera remplacé par votre consomation.", bg='#988080').grid(row=17, column=1)




#===================================
#           On ferme la fenètre
#===================================
fenetre.mainloop()
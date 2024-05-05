
import random

# Listes des jours en français
jours_francais = [
    "après un jour",
    "après deux jours",
    "après trois jours",
    "après quatre jours",
    "après cinq jours",
    "après six jours",
    "après sept jours",
    "après huit jours",
    "après neuf jours",
    "après dix jours",
    "après onze jours",
    "après douze jours",
    "après treize jours",
    "après quatorze jours",
    "après quinze jours",
    "après seize jours",
    "après dix-sept jours",
    "après dix-huit jours",
    "après dix-neuf jours",
    "après vingt jours"
]

# Liste des nombres en français
nombres_francais = [
    "après 1 jour",
    "après 2 jours",
    "après 3 jours",
    "après 4 jours",
    "après 5 jours",
    "après 6 jours",
    "après 7 jours",
    "après 8 jours",
    "après 9 jours",
    "après 10 jours",
    "après 11 jours",
    "après 12 jours",
    "après 13 jours",
    "après 14 jours",
    "après 15 jours",
    "après 16 jours",
    "après 17 jours",
    "après 18 jours",
    "après 19 jours",
    "après 20 jours"
]

# Obtention d'un élément aléatoire de chaque liste




# Liste des stations
station_mapping = {
        "Sfax": "1:9", "Tunis Ville": "1:202", "Tunis": "1:202", "Aouinet": "1:1", "Sakiet Ezzit": "1:10",
        "Bou Arada": "1:100", "Jelida": "1:101", "El Aroussa": "1:102", "Sidi Ayed": "1:103", "Gaafour": "1:104",
        "El Akhouat": "1:105", "Le Krib": "1:106", "Sidi Bou Rouis": "1:107", "Trika": "1:108", "Le Sers": "1:109",
        "Sidi Salah": "1:11", "Oued Tessa": "1:110", "Les Zouarines": "1:111", "Dahmani": "1:112", "Ain Mesria": "1:113",
        "Fej Etameur": "1:114", "Oued Sarrath": "1:115", "Kalaa Khasba": "1:116", "Haidra": "1:117", "Foussana": "1:118",
        "Voie Ballastiere- El hrich": "1:119", "Dokhane": "1:12", "Bir Bourekba": "1:120", "Hammamet": "1:121",
        "Omar Khayem": "1:122", "M'Razka": "1:123", "Nabeul Voyageurs": "1:124", "M'Saken": "1:125", "Jemmal": "1:126",
        "Moknine Marchandises": "1:127", "Founi": "1:128", "Hamada": "1:129", "La Hencha": "1:13", "Beau Sejour": "1:130",
        "Menzel Bourguiba": "1:131", "Borj Cedria": "1:132", "Erriadh": "1:133", "La Goulette": "1:134", "Aguila": "1:135",
        "M'Dhilla": "1:136", "Sehib": "1:137", "Tabeddit": "1:138", "Redeyef": "1:139", "El Jem": "1:14", "Kasserine": "1:140",
        "Sbeitla": "1:141", "Zerzour": "1:142", "Jilma": "1:143", "Hajeb El Aioun": "1:144", "Sidi Saad": "1:145", "Gouraia": "1:146",
        "Jerissa PV": "1:147", "Tajerouine": "1:148", "Mahdia": "1:149", "Kerker": "1:15", "Mahdia Ezzahra": "1:150", "Borj Arif": "1:151",
        "Sidi Masaoud": "1:152", "Baghdedi": "1:154", "Charaf": "1:155", "Bekalta": "1:156", "Teboulba": "1:157", "Teboulba Zi": "1:158",
        "Moknine Voyageurs": "1:159", "Sidi Bou Goubrine": "1:16", "Moknine Griba": "1:160", "Ksar Helal": "1:161", "Ksar Helal Zi": "1:162",
        "Sayeda": "1:163", "Lamta": "1:164", "Bouhjar": "1:165", "Ksiba Bennane": "1:166", "Khnis/Bembla": "1:167", "Frina": "1:168",
        "Monastir Zi": "1:169", "Kalaa Kebira": "1:17", "La Faculte 2": "1:170", "Monastir": "1:171", "Sousse Bab Jdid": "1:172",
        "Sousse Mohamed V": "1:173", "Sousse Sud": "1:174", "Sousse Zi": "1:175", "Sahline Ville": "1:176", "Sahline Sebkha": "1:177",
        "Les Hotels Monastir": "1:178", "Aeroport Skanes Monastir": "1:179", "Sidi Bou Ali": "1:18", "Skanes": "1:180", "La Faculte": "1:181",
        "Sousse Voyageurs": "1:182", "Kalaa Sghira": "1:183", "Borj Ettoum": "1:185", "Mejez El Bab": "1:186", "Sidi M'Himech": "1:187",
        "Beja Marchandises": "1:188", "Beja Voy": "1:189", "Menzel Gare": "1:19", "Mastouta": "1:190", "Sidi Smail": "1:191", "Bou Salem": "1:192",
        "Jendouba V": "1:193", "Oued Meliz": "1:194", "Ghardimaou": "1:195", "Oued Ellil": "1:196", "Mannouba": "1:197", "Le Bardo": "1:198",
        "Cité Erraoudha": "1:199", "Ghannouch": "1:2", "Ain Rahma": "1:21", "Ichkeul": "1:210", "Tinja": "1:211", "La Pecherie": "1:212",
        "Bizerte": "1:213", "kalaa Sghira": "1:214", "Khanguet": "1:215", "Tunis-PV": "1:216", "Lorbeuss": "1:217", "Nabeul Marchandise": "1:219",
        "Bouficha": "1:22", "Mahdia Zone Touristique": "1:220", "El Ayoun": "1:221", "Magroun": "1:222", "Sidi Mtir": "1:23", "Bou Arkoub": "1:24",
        "Belli": "1:25", "Turki": "1:26", "Grombalia": "1:27", "Fondouk Jedid": "1:28", "Bir El Bey": "1:29", "Gabes": "1:3", "Hammam Chat": "1:30",
        "Tahar Sfar": "1:31", "Arret Du Stade": "1:32", "Hammam Lif": "1:33", "Bou Kornine": "1:34", "Ez-Zahra": "1:35", "Rades Mel": "1:36",
        "Rades": "1:37", "Lycee Technique Rades": "1:38", "Sidi Rezig": "1:39", "Skhira": "1:4", "Megrine": "1:40", "Megrine Ryad": "1:41",
        "Depot Farhat Hached": "1:42", "Marchandise Sousse": "1:43", "Parc Friguia": "1:44", "Ezzahra Lycée": "1:45", "M'seken Messadine": "1:46",
        "Ksar Mezouar": "1:47", "Sidi Nsir": "1:48", "Mettarcheni": "1:49", "Chaal": "1:5", "El Arima": "1:50", "Ghraiba": "1:51",
        "Mezzouna": "1:52", "El Kerma": "1:53", "Maknassy": "1:54", "Menzel Bouzaiane": "1:55", "Sened": "1:56", "Zannouch": "1:57",
        "Oued El Ksab (23/24)": "1:58", "Cheria": "1:59", "Mahares": "1:6", "Mg 28/29": "1:60", "Le Kriz": "1:61", "Degueche": "1:62",
        "Tozeur": "1:63", "Gafsa": "1:64", "El Guetar": "1:65", "Mg N1": "1:66", "Segui": "1:67", "El Fejij": "1:68", "Mg N4": "1:69",
        "Gargour": "1:7", "Metlaoui": "1:70", "Selja": "1:71", "Om El Arais": "1:72", "Maagen Bel Abbes": "1:73", "Feriana": "1:74",
        "Thelepte": "1:75", "Mekdoudech": "1:76", "Mateur": "1:77", "Mateur Sud": "1:78", "Ghezala": "1:79", "Sidi Abid": "1:8",
        "Jalta": "1:80", "Jefna": "1:81", "Sedjnane": "1:82", "El Harrech": "1:83", "Tamera": "1:84", "Les Salines": "1:85",
        "Zaafrane": "1:86", "Le Kef": "1:87", "Djebal Jelloud": "1:88", "Bir Kassa": "1:89", "Nassen": "1:90",
        "Khledia": "1:91", "Oudna": "1:92", "Cheylus": "1:93", "Bir M'Cherga": "1:94", "Depienne": "1:95", "El Ouja": "1:96",
        "Pont Du Fahs": "1:97", "Thibica": "1:98", "Tarf Echena": "1:99"
    }
inverted_mapping = {}
for key, value in station_mapping.items():
    if value not in inverted_mapping:
        inverted_mapping[value] = [key, key.lower()]
        if " " in key:  # Vérifie si le nom contient un espace
            inverted_mapping[value].append(
                key.replace(" ", "").lower())  # Ajoute le nom sans espaces et en minuscules
    else:
        inverted_mapping[value].extend([key, key.lower()])
        if " " in key:  # Vérifie si le nom contient un espace
            inverted_mapping[value].append(key.replace(" ", "").lower())

#Générer des exemples
num_examples = 1500
k=0
# with open("data/train_schedule_examples.yml", "w", encoding="utf-8") as f:
#     for _ in range(num_examples):
#         ids = list(inverted_mapping.keys())
#         selected_ids = random.sample(ids, 2)
#         departure_id, arrival_id = selected_ids
#         selected_names = random.sample(inverted_mapping[departure_id], 2)
#         selected_names1 = random.sample(inverted_mapping[arrival_id], 2)
#         from_place1, from_place2 = selected_names
#         to_place1, to_place2 = selected_names1
#         jour_aleatoire = random.choice(jours_francais)
#         nombre_aleatoire = random.choice(nombres_francais)

#         date1 = f"{random.randint(2022, 2024)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}"
#         time1 = f"{random.randint(0, 23):02d}:{random.randint(0, 59):02d}"
#         if k == 0:
#             f.write(f"- un train [demain](date) [{time1}](time) de [{from_place1}](from_place) à [{to_place2}](to_place)  ?\n")
#             f.write(f"- je veux un train de [{to_place1}](from_place) à [{from_place1}](to_place) [{nombre_aleatoire}](date) à [{time1}](time) ?\n")
#             f.write(f"- Existe-t-il un train de [{from_place2}](from_place) à [{to_place1}](to_place) [{jour_aleatoire}](date) à [{time1}](time) ?\n")
#         elif k == 1:
#             f.write(f"- Existe-t-il un train de [{from_place1}](from_place) à [{to_place1}](to_place) [demain](date) [{time1}](time) ?\n")
#             f.write(f"- est ce que il y a un train de [{to_place2}](from_place) à [{from_place1}](to_place) [{jour_aleatoire}](date) à [{time1}](time) ?\n")
#             f.write(f"- un train de [{from_place2}](from_place) à [{to_place1}](to_place) [{nombre_aleatoire}](date) [{time1}](time) ?\n")
#         elif k == 2:
#             f.write(f"- je cherche un train de [{to_place1}](from_place) à [{from_place1}](to_place) [{nombre_aleatoire}](date) à [{time1}](time) ?\n")
#             f.write(f"- je veus un train vers [{from_place2}](to_place) à partir de [{to_place1}](from_place) [maintenant](time) ?\n")
#             f.write(f"- Existe-t-il un train le [{jour_aleatoire}](date) vers [{to_place2}](to_place) à partir de [{from_place1}](from_place) à [{time1}](time) ?\n")
#         elif k == 3:
#             f.write(f"- Existe-t-il un train vers [{from_place2}](to_place) à partir de [{to_place1}](from_place)  à [{time1}](time)[{nombre_aleatoire}](date) ?\n")
#             f.write(f"- il y a un train vers [{to_place1}](to_place) à partir de [{from_place1}](from_place) [demain](date) [{time1}](time) ?\n")
#             f.write(f"- il existe un train vers [{from_place1}](to_place) à partir de [{to_place2}](from_place) [{jour_aleatoire}](date) à [{time1}](time) ?\n")
#         elif k == 4:
#             f.write(f"- Existe-t-il un train vers [{to_place2}](to_place) à partir de [{from_place1}](from_place) [{nombre_aleatoire}](date) à [{time1}](time) ?\n")
#             f.write(f"- y a t il un train vers [{from_place1}](to_place) à partir de [{to_place1}](from_place) [aujourd'hui](date) à [{time1}](time) ?\n")
#             f.write(f"- Existe-t-il un train [{time1}](time) de [{from_place2}](from_place) à [{to_place1}](to_place) [aujourd'hui](date)  ?\n")
#         elif k == 5:
#             f.write(f"- train vers [{to_place1}](to_place) à partir de [{from_place1}](from_place) [après demain](date) à [{time1}](time) ?\n")
#             f.write(f"- Existe-t-il un train de [{to_place2}](from_place) à [{from_place1}](to_place)  [{time1}](time) [après demain](date) à?\n")
#             f.write(f"- je cherche un train de [{to_place1}](from_place) à [{from_place2}](to_place) [{nombre_aleatoire}](date) à [{time1}](time) ?\n")
#         elif k== 6:
#             f.write(f"- un train de [{from_place1}](from_place) à [{to_place1}](to_place) [après demain](date) à [{time1}](time) ?\n")
#             f.write(f"- je cherche un train à [{time1}](time) de [{to_place2}](from_place) à [{from_place1}](to_place) [{nombre_aleatoire}](date)  ?\n")
#             f.write(f"- Existe-t-il un train de [{from_place2}](from_place) à [{to_place1}](to_place)  à [{time1}](time) le[{jour_aleatoire}](date) ?\n")
#         elif k == 7:
#             f.write(f"- il y a un train de [{from_place1}](from_place) à [{to_place1}](to_place) [demain](date) [{time1}](time) ?\n")
#             f.write(f"- est ce que il y a un train de [{to_place1}](from_place) à [{from_place2}](to_place) [{jour_aleatoire}](date) à [{time1}](time) ?\n")
#             f.write(f"- de [{from_place1}](from_place) à [{to_place2}](to_place) [{nombre_aleatoire}](date) [{time1}](time) ?\n")
#         elif k == 8:
#             f.write(f"- je cherche un train de [{to_place2}](from_place) à [{from_place1}](to_place) [{nombre_aleatoire}](date) à [{time1}](time) ?\n")
#             f.write(f"- est ce que il y a un train de [{to_place1}](from_place) à [{from_place2}](to_place) [{jour_aleatoire}](date) à [{time1}](time) ?\n")
#             f.write(f"- de [{from_place1}](from_place) à [{to_place1}](to_place) [{nombre_aleatoire}](date) [{time1}](time) ?\n")
#         k = (k + 1) % 9
# with open("train_schedule_examples.yml", "w", encoding="utf-8") as f:
#     for i in stations :
#         f.write(f"{i}|")








# import datetime

# # Obtention de la date actuelle
# date_actuelle = datetime.date.today()
# print("Date actuelle:", date_actuelle)

# # Obtention de l'heure actuelle
# heure_actuelle = datetime.datetime.now().strftime("%H:%M")
# print("Heure actuelle:", heure_actuelle)


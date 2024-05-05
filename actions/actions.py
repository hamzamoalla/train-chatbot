from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests
from datetime import datetime, timedelta
from typing import Text
import re
from fuzzywuzzy import process
import geocoder
from geopy.distance import geodesic
#gps
def get_current_gps_coordinates():
    g = geocoder.ip('me') # Cette fonction est utilisée pour trouver les informations actuelles en utilisant notre adresse IP
    if g.latlng is not None: # g.latlng indique si les coordonnées ont été trouvées ou non
        return g.latlng
    else:
        return None
#calcule la distance
def distance_entre_points(coord1, coord2):
    return geodesic(coord1, coord2).kilometers
# Fonction pour trouver le point le plus proche


# Fonction pour trouver le point le plus proche
def point_le_plus_proche(position, liste_de_stations):
    plus_proche = None
    distance_min = float('inf')  # Initialiser à une valeur infinie

    for station in liste_de_stations:
        nom_station, coord = list(station.items())[0]  # Convertir dict_items en list
        distance = distance_entre_points(position, coord)
        if distance < distance_min:
            distance_min = distance
            plus_proche = nom_station

    return plus_proche, distance_min
def get_place_code(place: Text) -> Text:
    # Mapping des noms de lieux aux codes spécifiques
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

    all_names = [name for names in inverted_mapping.values() for name in names]

    matched_place = process.extractOne(place, all_names, score_cutoff=80)

    if matched_place:
        # Recherche du code correspondant au nom trouvé
        for key, names in inverted_mapping.items():
            if matched_place[0] in names:
                return key
    return "pas de code"
def parse_maitenant(word):
    valid_words = ["maintenant"]
    match = process.extractOne(word.lower(), valid_words, score_cutoff=80)

    if match:
        return parse_now()
    else:
        return word
def convert_duration(duration_seconds):
        hours = duration_seconds // 3600
        minutes = (duration_seconds % 3600) // 60
        return f"{hours} heures et {minutes} minutes"
def convert_unix_time(millis):
        return datetime.fromtimestamp(millis / 1000).strftime('%Y-%m-%d %H:%M:%S')
def parse_now():
    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M")
    return date, time
def convertir_expression_date_apres(expression):
    # Définir un dictionnaire pour mapper les nombres écrits en lettres à des entiers
    mots_nombres = {
        'un': 1, 'deux': 2, 'trois': 3, 'quatre': 4, 'cinq': 5,
        'six': 6, 'sept': 7, 'huit': 8, 'neuf': 9, 'dix': 10,
        'onze': 11, 'douze': 12, 'treize': 13, 'quatorze': 14, 'quinze': 15,
        'seize': 16, 'dix-sept': 17, 'dix-huit': 18, 'dix-neuf': 19, 'vingt': 20
    }

    # Utiliser une expression régulière pour trouver le nombre dans l'expression
    match = re.search(r'\b(?:après|apres|apre)\s+(.+)\s+jours?\b', expression)
    if match:
        mot_nombre = match.group(1).strip()
        if mot_nombre in mots_nombres:
            jours = mots_nombres[mot_nombre]
            # Calculer la date actuelle + le nombre de jours
            date_future = datetime.now() + timedelta(days=jours)
            # Formater la date selon le format AAAA-MM-JJ
            date_formatee = date_future.strftime('%Y-%m-%d')
            return date_formatee
        elif mot_nombre.isdigit():
            jours = int(mot_nombre)
            # Calculer la date actuelle + le nombre de jours
            date_future = datetime.now() + timedelta(days=jours)
            # Formater la date selon le format AAAA-MM-JJ
            date_formatee = date_future.strftime('%Y-%m-%d')
            return date_formatee
        else:
            # Si le mot n'est pas dans le dictionnaire, recherchez le mot le plus proche
            mot_corrige, score = process.extractOne(mot_nombre, mots_nombres.keys())
            if score >= 80:  # Seuil de similarité
                jours = mots_nombres[mot_corrige]
                # Calculer la date actuelle + le nombre de jours
                date_future = datetime.now() + timedelta(days=jours)
                # Formater la date selon le format AAAA-MM-JJ
                date_formatee = date_future.strftime('%Y-%m-%d')
                return date_formatee
            else:
                return expression
    else:
        return expression
def convertir_ecriture_date(phrase):
    # Dictionnaire pour mapper les noms des mois aux nombres de mois
    mois_nombres = {
        'janvier': 1, 'février': 2, 'mars': 3, 'avril': 4, 'mai': 5,
        'juin': 6, 'juillet': 7, 'août': 8, 'septembre': 9, 'octobre': 10,
        'novembre': 11, 'décembre': 12
    }

    # Séparation de la phrase en mots
    mots = phrase.split()

    # Vérification de la présence du mois dans le dictionnaire et du nombre de mots
    if len(mots) == 2:
        mot_mois = mots[1].lower()
        # Vérifier si le mois est déjà correct
        if mot_mois in mois_nombres:
            # Récupération de la date, du mois et de l'année
            jour = int(mots[0])
            mois = mois_nombres[mot_mois]
            # Supposons une année actuelle pour la date
            annee = datetime.now().year

            # Création de l'objet datetime
            date_resultat = datetime(annee, mois, jour)

            # Formatage de la date selon le format AAAA-MM-JJ
            date_formatee = date_resultat.strftime('%Y-%m-%d')
            return date_formatee
        else:
            # Si le mois n'est pas trouvé dans le dictionnaire, recherchez le plus proche
            mot_corrige, score = process.extractOne(mot_mois, mois_nombres.keys())
            if score >= 80:  # Seuil de similarité
                # Récupération de la date et de l'année
                jour = int(mots[0])
                mois = mois_nombres[mot_corrige]
                annee = datetime.now().year

                # Création de l'objet datetime
                date_resultat = datetime(annee, mois, jour)

                # Formatage de la date selon le format AAAA-MM-JJ
                date_formatee = date_resultat.strftime('%Y-%m-%d')
                return date_formatee
            else:
                return phrase
    else:
        return phrase
def convertir_terme_date(terme):
    # Dictionnaire des termes connus avec leur correspondance
    termes_connus = {
        'demain': 'demain', 'après-demain': 'après-demain', 'aujourd’hui': 'aujourd’hui',
        'demainn': 'demain', 'apres-demain': 'après-demain', 'aujourd-hui': 'aujourd’hui'
    }

    # Récupérer la date d'aujourd'hui
    date_aujourd_hui = datetime.now().date()

    # Vérifier si le terme est dans les termes connus
    if terme.lower() in termes_connus:
        terme_correct = termes_connus[terme.lower()]
        # Calculer la date correspondante
        if terme_correct == 'demain':
            date_resultat = date_aujourd_hui + timedelta(days=1)
        elif terme_correct == 'après-demain':
            date_resultat = date_aujourd_hui + timedelta(days=2)
        else:  # aujourd'hui
            date_resultat = date_aujourd_hui

        # Formater la date selon le format AAAA-MM-JJ
        date_formatee = date_resultat.strftime('%Y-%m-%d')
        return date_formatee
    else:
        # Si le terme n'est pas trouvé dans les termes connus, recherchez le plus proche
        terme_corrige, score = process.extractOne(terme.lower(), termes_connus.keys())
        if score >= 80:  # Seuil de similarité
            # Calculer la date correspondante pour le terme corrigé
            if termes_connus[terme_corrige] == 'demain':
                date_resultat = date_aujourd_hui + timedelta(days=1)
            elif termes_connus[terme_corrige] == 'après-demain':
                date_resultat = date_aujourd_hui + timedelta(days=2)
            else:  # aujourd'hui
                date_resultat = date_aujourd_hui

            # Formater la date selon le format AAAA-MM-JJ
            date_formatee = date_resultat.strftime('%Y-%m-%d')
            return date_formatee
        else:
            return terme
def get_train_schedule(from_place, to_place, date, time):
    # Utiliser les codes spécifiques pour Sfax et Tunis dans l'URL de requête
    from_place_code = get_place_code(from_place)
    to_place_code = get_place_code(to_place)
    url = f"https://planner.sncft.com.tn/otp/routers/default/plan?fromPlace={from_place_code}&toPlace={to_place_code}&date={date}&time={time}"
    response = requests.get(url)
    return response.json()
def is_train_available(schedule):
    if 'plan' not in schedule:
        print("La clé 'plan' n'est pas présente dans la réponse.")
        return False
    if not schedule['plan']['itineraries']:
        return False
    return schedule['plan']['itineraries'][0]['duration'] > 0
class ActionCheckTrainAvailability(Action):
    def name(self) -> Text:
        return "action_check_train_availability"


    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        time = tracker.get_slot('time')
        from_place = tracker.get_slot('from_place')
        to_place = tracker.get_slot('to_place')
        date = tracker.get_slot('date')
        valid_words = ["maintenant"]
        match = process.extractOne(time.lower(), valid_words, score_cutoff=90)
        if match:
            date, time = parse_maitenant(time)
        else:
            date = convertir_terme_date(date)
            date = convertir_expression_date_apres(date)
            date = convertir_ecriture_date(date)
        schedule = get_train_schedule(from_place, to_place, date, time)
        if is_train_available(schedule):
            itinerary = schedule['plan']['itineraries'][0]
            duration = convert_duration(itinerary['duration'])
            transfers = itinerary['transfers']
            segments = itinerary['legs']
            message = f"Il y a un train  disponible  "
            for i, segment in enumerate(segments, start=1):
                mode = segment['mode']
                from_stop = segment['from']['name']
                to_stop = segment['to']['name']
                departure_time = convert_unix_time(segment['startTime'])
                arrival_time = convert_unix_time(segment['endTime'])
                message += f"de {from_stop} à {to_stop}, de durée : {duration},départ à {departure_time}, arrivée à {arrival_time} Transferts : {transfers}\n . Segment {i}: {mode} \n ___ from {from_place} le code est {get_place_code(from_place)} \n___ to {to_place} le code est {get_place_code(to_place)} \n___ date {date} \n___time {time}  "
            dispatcher.utter_message(text=message)
        else:
            dispatcher.utter_message(text=f"Aucun train n'est disponible à cet horaire.\n ___ from {from_place} le code est {get_place_code(from_place)} \n___ to {to_place} le code est {get_place_code(to_place)} \n___ date {date} \n___time {time}")
        return []
       
        
class ActionCheckTrainAvailabilityinaday(Action):
    def name(self) -> Text:
        return "action_check_train_availability_in_a_day"


    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        from_place = tracker.get_slot('from_place')
        to_place = tracker.get_slot('to_place')
        date = tracker.get_slot('date')
        date = convertir_terme_date(date)
        date = convertir_expression_date_apres(date)
        date = convertir_ecriture_date(date)
        time = datetime.strptime('00:00', '%H:%M')
        une_heure = timedelta(hours=1)
        ids_uniques = set()
        for m in range(24):
            message =f""
            time_str = time.strftime('%H:%M')
            schedule = get_train_schedule(from_place, to_place, date, time_str)
            if is_train_available(schedule):
                itinerary = schedule['plan']['itineraries'][0]
                duration = convert_duration(itinerary['duration'])
                segments = itinerary['legs']
                trip_id = schedule['plan']['itineraries'][0]['legs'][0]['tripId']
                if trip_id not in ids_uniques:
                    ids_uniques.add(trip_id)
                    for i, segment in enumerate(segments, start=1):
                        from_stop = segment['from']['name']
                        to_stop = segment['to']['name']
                        departure_time = convert_unix_time(segment['startTime'])
                        arrival_time = convert_unix_time(segment['endTime'])
                        message += f"Il y a un train  disponible de {from_stop} à {to_stop}, de durée : {duration},départ à {departure_time}, arrivée à {arrival_time} \n  "
                        if i>0:
                            message += f".Puis"
                    dispatcher.utter_message(text=message)
            time += une_heure
        if not ids_uniques:
            dispatcher.utter_message(text=f"Aucun action_check_train_availability_in_a_day train n'est disponible à cet horaire from {from_place}to {to_place}a la date {date}")
#de trip id {trip_id}\n ___ from {from_place} le code est {get_place_code(from_place)} \n___ to {to_place} le code est {get_place_code(to_place)} \n___ date {date} \n___time {time_str}
#        dispatcher.utter_message(text=f"from {from_place} le code est {get_place_code(from_place)}")
 #       dispatcher.utter_message(text=f"to {to_place} le code est {get_place_code(to_place)}")
  #      dispatcher.utter_message(text=f"{date}")
   #     dispatcher.utter_message(text=f"{time}")
        return []
class ActionFindNearesttrainStation(Action):

    def name(self) -> Text:
        return "action_find_nearest_train_station"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        coordinates = get_current_gps_coordinates()
        if coordinates is not None:
            stations = [
                {"Aouinet": (33.9853263, 10.0037656)},
                {"Sakiet Ezzit": (34.800716, 10.7612703)},
                {"Bou Arada": (36.3564626, 9.6269026)},
                {"Jelida": (36.371689, 9.5563711)},
                {"El Aroussa": (36.3811585, 9.4545564)},
                {"Sidi Ayed": (36.3512125, 9.3909172)},
                {"Gaafour": (36.3226555, 9.3265976)},
                {"El Akhouat": (36.2550899, 9.2549561)},
                {"Le Krib": (36.2534979, 9.1851306)},
                {"Sidi Bou Rouis": (36.1753222, 9.1250941)},
                {"Trika": (36.1324521, 9.1129085)},
                {"Le Sers": (36.0759795, 9.0232335)},
                {"Sidi Salah": (34.8580193, 10.7673434)},
                {"Oued Tessa": (36.0673285, 8.936189)},
                {"Les Zouarines": (36.0403538, 8.9140838)},
                {"Dahmani": (35.9451774, 8.828704)},
                {"Ain Mesria": (35.9121855, 8.7393168)},
                {"Fej Etameur": (35.8781647, 8.7078069)},
                {"Oued Sarrath": (35.7663546, 8.618615)},
                {"Kalaa Khasba": (35.6636728, 8.5922552)},
                {"Haidra": (35.5660212, 8.4482377)},
                {"Foussana": (35.3492711, 8.6250111)},
                {"Voie Ballastiere- El hrich": (35.2407172, 8.7477377)},
                {"Dokhane": (34.9909425, 10.7608859)},
                {"Bir Bourekba": (36.4306822, 10.5737451)},
                {"Hammamet": (36.4076404, 10.612458)},
                {"Omar Khayem": (36.4239685, 10.6689255)},
                {"M'Razka": (36.4281111, 10.6810196)},
                {"Nabeul Voyageurs": (36.4510322, 10.7351045)},
                {"M'Saken": (35.7304332, 10.6014892)},
                {"Jemmal": (35.6286111, 10.7575972)},
                {"Moknine Marchandises": (35.6279133, 10.895083)},
                {"Founi": (34.5162228, 10.0431376)},
                {"Hamada": (34.3787002, 10.117251)},
                {"La Hencha": (35.1374614, 10.7283988)},
                {"Beau Sejour": (37.151423, 9.7933841)},
                {"Menzel Bourguiba": (37.1397823, 9.8030994)},
                {"Borj Cedria": (36.7034822, 10.3974291)},
                {"Erriadh": (36.6982789, 10.4215171)},
                {"La Goulette": (36.8066846, 10.2909578)},
                {"Aguila": (34.3796334, 8.7684013)},
                {"M'Dhilla": (34.2919887, 8.72436)},
                {"Sehib": (34.2369521, 8.646821)},
                {"Tabeddit": (34.4364752, 8.2593068)},
                {"Redeyef": (34.3880084, 8.1524871)},
                {"El Jem": (35.2925658, 10.7095802)},
                {"Kasserine": (35.1674016, 8.8347042)},
                {"Sbeitla": (35.2275949, 9.1281117)},
                {"Zerzour": (35.2490918, 9.3036993)},
                {"Jilma": (35.2741441, 9.421765)},
                {"Hajeb El Aioun": (35.368141, 9.5710127)},
                {"Sidi Saad": (35.3912767, 9.7607252)},
                {"Gouraia": (35.8584398, 8.6846278)},
                {"Jerissa PV": (35.8502501, 8.6528073)},
                {"Tajerouine": (35.8519636, 8.5459635)},
                {"Mahdia": (35.5007749, 11.0642716)},
                {"Kerker": (35.4682761, 10.6597043)},
                {"Mahdia Ezzahra": (35.5000429, 11.048318)},
                {"Borj Arif": (35.5061925, 11.0303632)},
                {"Sidi Masaoud": (35.5210721, 11.0272134)},
                {"Baghdedi": (35.5695318, 11.0184244)},
                {"Charaf": (35.594883, 11.0098213)},
                {"Bekalta": (35.615241, 10.9893645)},
                {"Teboulba": (35.6377169, 10.9616318)},
                {"Teboulba Zi": (35.6337468, 10.9434955)},
                {"Moknine Voyageurs": (35.6312829, 10.9156069)},
                {"Sidi Bou Goubrine": (35.5938773, 10.6287182)},
                {"Moknine Griba": (35.6379972, 10.9069094)},
                {"Ksar Helal": (35.6451442, 10.9009117)},
                {"Ksar Helal Zi": (35.6519229, 10.8986172)},
                {"Sayeda": (35.6660635, 10.8881796)},
                {"Lamta": (35.6701908, 10.8828352)},
                {"Bouhjar": (35.6723505, 10.8676304)},
                {"Ksiba Bennane": (35.6800414, 10.8426818)},
                {"Khnis/Bembla": (35.7090448, 10.8124341)},
                {"Frina": (35.7306706, 10.8126974)},
                {"Monastir Zi": (35.7401836, 10.8204016)},
                {"Kalaa Kebira": (35.867843, 10.5534154)},
                {"La Faculte 2": (35.7613195, 10.809322)},
                {"Monastir": (35.7706263, 10.8252907)},
                {"Sousse Bab Jdid": (35.823063, 10.6415928)},
                {"Sousse Mohamed V": (35.8159939, 10.6432475)},
                {"Sousse Sud": (35.800173, 10.649924)},
                {"Sousse Zi": (35.7821012, 10.6683762)},
                {"Sahline Ville": (35.7595786, 10.7014559)},
                {"Sahline Sebkha": (35.7576841, 10.7165366)},
                {"Les Hotels Monastir": (35.7601219, 10.7448919)},
                {"Aeroport Skanes Monastir": (35.7625157, 10.754098)},
                {"Sidi Bou Ali": (35.9531545, 10.4513333)},
                {"Skanes": (35.7680658, 10.7882324)},
                {"La Faculte": (35.7596167, 10.8073597)},
                {"Sousse Voyageurs": (35.8304246, 10.6380517)},
                {"Kalaa Sghira": (35.8220139, 10.5711182)},
                {"Borj Ettoum": (36.7876599, 9.7615566)},
                {"Mejez El Bab": (36.6657253, 9.6065106)},
                {"Sidi M'Himech": (36.7825473, 9.2793081)},
                {"Beja Marchandises": (36.7387942, 9.1898576)},
                {"Beja Voy": (36.7248682, 9.1901878)},
                {"Menzel Gare": (36.0105291, 10.377545)},
                {"Mastouta": (36.6616127, 9.2090789)},
                {"Sidi Smail": (36.5955176, 9.111899)},
                {"Bou Salem": (36.6112381, 8.9688798)},
                {"Jendouba V": (36.5012361, 8.7772554)},
                {"Oued Meliz": (36.4696166, 8.5513348)},
                {"Ghardimaou": (36.4477683, 8.4372042)},
                {"Oued Ellil": (36.8358397, 10.0091068)},
                {"Mannouba": (36.8161297, 10.1011079)},
                {"Le Bardo": (36.811173, 10.1181392)},
                {"Cité Erraoudha": (36.8062597, 10.1392118)},
                {"Ghannouch": (33.9215859, 10.0769244)},
                {"Enfida": (36.1307311, 10.3836398)},
                {"Benbachir": (36.5918189, 8.905504)},
                {"Tunis Ville": (36.7947693, 10.1803806)},
                {"Tebourba": (36.8291603, 9.8443655)},
                {"El Heri": (36.7419856, 9.7016854)},
                {"Oued Zarga": (36.6732537, 9.4266499)},
                {"Jedeida": (36.8507975, 9.9334513)},
                {"Chaouat": (36.8894814, 9.944471)},
                {"Sidi Othman": (36.960039, 9.924713)},
                {"Ain Ghelal": (37.0233607, 9.8327899)},
                {"Ain Rahma": (36.2263937, 10.4269494)},
                {"Ichkeul": (37.1149215, 9.7292643)},
                {"Tinja": (37.1594962, 9.7572135)},
                {"La Pecherie": (37.2541232, 9.8394025)},
                {"Bizerte": (37.266437, 9.8639003)},
                {"kalaa Sghira": (35.8216673, 10.5708481)},
                {"Khanguet": (36.6248529, 10.4613998)},
                {"Tunis-PV": (36.7923761, 10.1887689)},
                {"Lorbeuss": (36.1007823, 8.934963)},
                {"Nabeul Marchandise": (36.4321388, 10.6939576)},
                {"Bouficha": (36.3033024, 10.451222)},
                {"Mahdia Zone Touristique": (35.4993151, 11.0626164)},
                {"El Ayoun": (34.4280017, 8.2892621)},
                {"Magroun": (34.333134, 8.3944453)},
                {"Sidi Mtir": (36.3869585, 10.5029636)},
                {"Bou Arkoub": (36.5310753, 10.5514179)},
                {"Belli": (36.5606093, 10.524965)},
                {"Turki": (36.5755004, 10.5135323)},
                {"Grombalia": (36.5963444, 10.4977219)},
                {"Fondouk Jedid": (36.6689169, 10.4467133)},
                {"Bir El Bey": (36.7102497, 10.3786432)},
                {"Gabes": (33.8842247, 10.0991946)},
                {"Hammam Chat": (36.7136003, 10.3694051)},
                {"Tahar Sfar": (36.7175239, 10.3596743)},
                {"Arret Du Stade": (36.7234436, 10.3482081)},
                {"Hammam Lif": (36.7294393, 10.3342066)},
                {"Bou Kornine": (36.7347949, 10.3239341)},
                {"Ez-Zahra": (36.7468002, 10.3070495)},
                {"Rades Mel": (36.7629769, 10.2842731)},
                {"Rades": (36.7683604, 10.269735)},
                {"Lycee Technique Rades": (36.7667869, 10.2608437)},
                {"Sidi Rezig": (36.7673336, 10.2445454)},
                {"Skhira": (34.3004318, 10.0688506)},
                {"Megrine": (36.768327, 10.2339183)},
                {"Megrine Ryad": (36.7702743, 10.2229004)},
                {"Depot Farhat Hached": (36.7840392, 10.1918987)},
                {"Marchandise Sousse": (35.7779299, 10.5772365)},
                {"Parc Friguia": (36.2043374, 10.4193379)},
                {"Ezzahra Lycée": (36.7390405, 10.3179647)},
                {"M'seken Messadine": (35.7549566, 10.5909218)},
                {"Ksar Mezouar": (36.9153999, 9.4580425)},
                {"Sidi Nsir": (36.9615341, 9.5245642)},
                {"Mettarcheni": (37.0012275, 9.6008757)},
                {"Chaal": (34.5164299, 10.3442373)},
                {"El Arima": (37.0216504, 9.6388624)},
                {"Ghraiba": (34.499659, 10.2137336)},
                {"Mezzouna": (34.5739692, 9.8418336)},
                {"El Kerma": (34.6312105, 9.7487658)},
                {"Maknassy": (34.6066931, 9.6064385)},
                {"Menzel Bouzaiane": (34.5759482, 9.4580005)},
                {"Sened": (34.5380285, 9.2535122)},
                {"Zannouch": (34.4686276, 9.0522272)},
                {"Oued El Ksab (23/24)": (34.4505774, 8.9566927)},
                {"Cheria": (34.3407875, 8.6060841)},
                {"Mahares": (34.5262626, 10.4986932)},
                {"Mg 28/29": (34.3203719, 8.5094551)},
                {"Le Kriz": (34.0331235, 8.2430399)},
                {"Degueche": (33.9868565, 8.2132722)},
                {"Tozeur": (33.9265547, 8.1357808)},
                {"Gafsa": (34.3947091, 8.8038973)},
                {"El Guetar": (34.3301217, 8.9496254)},
                {"Mg N1": (34.2252007, 9.1666819)},
                {"Segui": (34.174233, 9.4056288)},
                {"El Fejij": (34.0658562, 9.7362494)},
                {"Mg N4": (34.0112183, 9.8456117)},
                {"Gargour": (34.572812, 10.5778821)},
                {"Metlaoui": (34.3157766, 8.4164253)},
                {"Selja": (34.3853424, 8.3399541)},
                {"Om El Arais": (34.4870626, 8.2773565)},
                {"Maagen Bel Abbes": (34.7500864, 8.5195195)},
                {"Feriana": (34.9491796, 8.5681485)},
                {"Thelepte": (34.9765388, 8.5962215)},
                {"Mekdoudech": (35.0838213, 8.7266047)},
                {"Mateur": (37.0381104, 9.6844217)},
                {"Mateur Sud": (37.0367493, 9.6622766)},
                {"Ghezala": (37.0646914, 9.6021629)},
                {"Sidi Abid": (34.6954477, 10.7023059)},
                {"Jalta": (37.0740394, 9.5347362)},
                {"Jefna": (37.0426792, 9.4417664)},
                {"Sedjnane": (37.0513765, 9.2764831)},
                {"El Harrech": (37.0596772, 9.2207192)},
                {"Tamera": (37.0558225, 9.1195977)},
                {"Les Salines": (36.0777744, 8.9640175)},
                {"Zaafrane": (36.1530523, 8.8881448)},
                {"Le Kef": (36.1667329, 8.7036816)},
                {"Djebal Jelloud": (36.7727251, 10.2082258)},
                {"Bir Kassa": (36.7410751, 10.2285076)},
                {"Sfax": (34.7351507, 10.7671236)},
                {"Nassen": (36.7035756, 10.2328041)},
                {"Khledia": (36.6461424, 10.1944904)},
                {"Oudna": (36.6253599, 10.1511201)},
                {"Cheylus": (36.5554191, 10.0608556)},
                {"Bir M'Cherga": (36.5062105, 10.0218831)},
                {"Depienne": (36.4572093, 10.0235804)},
                {"El Ouja": (36.4179661, 9.9823781)},
                {"Pont Du Fahs": (36.3766759, 9.9024049)},
                {"Thibica": (36.3560495, 9.8092549)},
                {"Tarf Echena": (36.355274, 9.7173739)},
            ]
            plus_proche_lieu, distance = point_le_plus_proche(coordinates, stations)
            dispatcher.utter_message(text=f"La station la plus proche est : {plus_proche_lieu} de distance {distance}")
            #print(f"Vos coordonnées GPS actuelles sont :")
            #print(f"Latitude: {latitude}")
            #print(f"Longitude: {longitude}")
        else:
            dispatcher.utter_message(text=f"impossible de trouver votre position")

        return []

class ActionCheckTrainAvailabilitybeforetime(Action):
    def name(self) -> Text:
        return "action_check_train_availability_before_time"


    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        from_place = tracker.get_slot('from_place')
        to_place = tracker.get_slot('to_place')
        time = tracker.get_slot('time')
        date, from_time_obj = parse_maitenant("maintenant")
        to_time_obj = datetime.strptime(time, '%H:%M')
        current_time = from_time_obj
        current_time = datetime.strptime(from_time_obj, '%H:%M')
        ids_uniques = set()
        while current_time < to_time_obj:
            message = f""
            current_time1 = current_time.strftime('%H:%M')
            schedule = get_train_schedule(from_place, to_place, date, current_time1)
            if is_train_available(schedule):
                current_time += timedelta(minutes=15)
                itinerary = schedule['plan']['itineraries'][0]
                duration = convert_duration(itinerary['duration'])
                segments = itinerary['legs']
                trip_id = schedule['plan']['itineraries'][0]['legs'][0]['tripId']
                if trip_id not in ids_uniques:
                    ids_uniques.add(trip_id)
                    for i, segment in enumerate(segments, start=1):
                        from_stop = segment['from']['name']
                        to_stop = segment['to']['name']
                        departure_time = convert_unix_time(segment['startTime'])
                        arrival_time = convert_unix_time(segment['endTime'])
                        message += f"Il y a un train  disponible de {from_stop} à {to_stop}, de durée : {duration},départ à {departure_time}, arrivée à {arrival_time}  ___ from {from_place} le code est {get_place_code(from_place)} \n___ to {to_place} le code est {get_place_code(to_place)} \n___ date {date} \n___time {current_time1}  "
                    dispatcher.utter_message(text=message)
            else:
                current_time += timedelta(minutes=15)
                dispatcher.utter_message(text=f"le temps incre {current_time.strftime('%H:%M')}\n ")
        if not ids_uniques:
            dispatcher.utter_message(text=f"Aucun action_check_train_availability_before_time train n'est disponible à cet horaire.\n ___ from {from_place} le code est {get_place_code(from_place)} \n___ to {to_place} le code est {get_place_code(to_place)} \n___ date {date}\n___time {current_time.strftime('%H:%M')}\n___time {time}\n___time {current_time.strftime('%H:%M')}\n___time {current_time.strftime('%H:%M')} ")


        return []
class ActionCheckTrainAvailabilitybeforetimeinadate(Action):
    def name(self) -> Text:
        return "action_check_train_availability_before_time_in_a_date"


    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        from_place = tracker.get_slot('from_place')
        to_place = tracker.get_slot('to_place')
        time = tracker.get_slot('time')
        date = tracker.get_slot('date')
        date = convertir_terme_date(date)
        date = convertir_expression_date_apres(date)
        date = convertir_ecriture_date(date)
        time1 = datetime.now()
        heure_minute_str = time1.strftime("%H:%M")
        from_time_obj = datetime.strptime(heure_minute_str, "%H:%M")
        to_time_obj = datetime.strptime(time, '%H:%M')
        current_time = from_time_obj
        ids_uniques = set()
        while current_time < to_time_obj:
            message = f""
            current_time1 = current_time.strftime('%H:%M')
            schedule = get_train_schedule(from_place, to_place, date, current_time1)
            if is_train_available(schedule):
                current_time += timedelta(minutes=15)
                itinerary = schedule['plan']['itineraries'][0]
                duration = convert_duration(itinerary['duration'])
                segments = itinerary['legs']
                trip_id = schedule['plan']['itineraries'][0]['legs'][0]['tripId']
                if trip_id not in ids_uniques:
                    ids_uniques.add(trip_id)
                    for i, segment in enumerate(segments, start=1):
                        from_stop = segment['from']['name']
                        to_stop = segment['to']['name']
                        departure_time = convert_unix_time(segment['startTime'])
                        arrival_time = convert_unix_time(segment['endTime'])
                        message += f"Il y a un train  disponible de {from_stop} à {to_stop}, de durée : {duration},départ à {departure_time}, arrivée à {arrival_time}  ___ from {from_place} le code est {get_place_code(from_place)} \n___ to {to_place} le code est {get_place_code(to_place)} \n___ date {date} \n___time {current_time1}  "
                    dispatcher.utter_message(text=message)
            else:
                current_time += timedelta(minutes=15)
                dispatcher.utter_message(text=f"le temps incre {current_time.strftime('%H:%M')}\n ")
        if not ids_uniques:
            dispatcher.utter_message(text=f"Aucu naction_check_train_availability_before_time_in_a_date train n'est disponible à cet horaire.\n ___ from {from_place} le code est {get_place_code(from_place)} \n___ to {to_place} le code est {get_place_code(to_place)} \n___ date {date}\n___time {current_time.strftime('%H:%M')}\n___time {time}\n___time {current_time.strftime('%H:%M')} ")


        return []
class ActionChecknextTrainAvailability(Action):
    def name(self) -> Text:
        return "action_check_next_train_availability"


    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        from_place = tracker.get_slot('from_place')
        to_place = tracker.get_slot('to_place')
        date, time1 = parse_maitenant("maintenant")
        time = datetime.strptime(time1, '%H:%M')
        une_heure = timedelta(hours=1)
        ids_uniques = set()
        for m in range(24):
            message =f""
            time_str = time.strftime('%H:%M')
            schedule = get_train_schedule(from_place, to_place, date, time_str)
            if not ids_uniques:
                if is_train_available(schedule):
                    itinerary = schedule['plan']['itineraries'][0]
                    duration = convert_duration(itinerary['duration'])
                    segments = itinerary['legs']
                    trip_id = schedule['plan']['itineraries'][0]['legs'][0]['tripId']
                    if trip_id not in ids_uniques:
                        ids_uniques.add(trip_id)
                        message += f"le prochain train"
                        for i, segment in enumerate(segments, start=1):
                            from_stop = segment['from']['name']
                            to_stop = segment['to']['name']
                            departure_time = convert_unix_time(segment['startTime'])
                            arrival_time = convert_unix_time(segment['endTime'])
                            message += f"disponible de {from_stop} à {to_stop}, de durée : {duration},départ à {departure_time}, arrivée à {arrival_time} \n  "
                        dispatcher.utter_message(text=message)
            time += une_heure
        if not ids_uniques:
            dispatcher.utter_message(text=f"Aucun action_check_next_train_availability train n'est disponible à cet horaire from {from_place}to {to_place}dans ces 24 heures")

        return []
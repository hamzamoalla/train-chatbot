from geopy.distance import geodesic


# Fonction pour calculer la distance entre deux points géographiques
def distance_entre_points(coord1, coord2):
    return geodesic(coord1, coord2).kilometers


# Fonction pour trouver le point le plus proche
def point_le_plus_proche(position, liste_de_lieux):
    plus_proche = None
    distance_min = float('inf')  # Initialiser à une valeur infinie

    for lieu, coord in liste_de_lieux.items():
        distance = distance_entre_points(position, coord)
        if distance < distance_min:
            distance_min = distance
            plus_proche = lieu

    return plus_proche, distance_min


# Exemple d'utilisation
position = (36.819, 10.1658)  # Remplacer latitude et longitude par les coordonnées de la position donnée
liste_de_lieux = {
    'Lieu 1': (36.81612972,10.10110789),
    'Lieu 2': (36.79476927,10.18038057),
    # Ajouter d'autres lieux avec leurs coordonnées
}

plus_proche_lieu, distance = point_le_plus_proche(position, liste_de_lieux)
print("Le lieu le plus proche est:", plus_proche_lieu)
print("La distance jusqu'au lieu le plus proche est:", distance, "kilomètres")

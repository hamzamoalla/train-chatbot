import geocoder

def get_current_gps_coordinates():
    g = geocoder.ip('me') # Cette fonction est utilisée pour trouver les informations actuelles en utilisant notre adresse IP
    if g.latlng is not None: # g.latlng indique si les coordonnées ont été trouvées ou non
        return g.latlng
    else:
        return None

if __name__ == "__main__":
    coordinates = get_current_gps_coordinates()
    if coordinates is not None:
        latitude, longitude = coordinates
        print(f"Vos coordonnées GPS actuelles sont :")
        print(f"Latitude: {latitude}")
        print(f"Longitude: {longitude}")
    else:
        print("Impossible de récupérer vos coordonnées GPS.")

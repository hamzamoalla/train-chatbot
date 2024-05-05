from datetime import datetime, timedelta
from_time ="12:00"
to_time = "19:30"
# Convertir les chaînes de temps en objets datetime
from_time_obj = datetime.strptime(from_time, '%H:%M')
to_time_obj = datetime.strptime(to_time, '%H:%M')

# Initialiser une liste pour stocker les horaires
time_schedule = []

# Ajouter la première heure (from_time)
current_time = from_time_obj

# Tant que l'heure actuelle est inférieure à l'heure de fin (to_time), continuer la boucle
while current_time < to_time_obj:
    # Ajouter l'heure actuelle à la liste
    time_schedule.append(current_time.strftime('%H:%M'))

    # Ajouter 15 minutes à l'heure actuelle
    current_time += timedelta(minutes=30)

# Afficher l'horaire résultant
print(time_schedule)

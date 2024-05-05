import re
from fuzzywuzzy import process

def convertir_date_vers_format_standard(date):
    # Modèle de regex pour les différentes formes de date
    patterns = [
        r'(\d{4})[/-](\d{1,2})[/-](\d{1,2})',  # yyyy/mm/dd ou yyyy-mm-dd ou yyyy\mm\dd
        r'(\d{1,2})[/-](\d{1,2})[/-](\d{4})'    # dd-mm-yyyy
    ]

    # Modèle de remplacement pour la date en format standard yyyy-mm-dd
    replacement = r'\1-\2-\3'

    # Rechercher et remplacer les différentes formes de date par le format standard
    for pattern in patterns:
        date = re.sub(pattern, replacement, date)

    return date

def corriger_faute_de_frappe(date):
    # Modèle de date standard
    date_standard = r'\d{4}-\d{2}-\d{2}'

    # Rechercher une correspondance avec le modèle de date standard
    match = re.search(date_standard, date)
    if match:
        return match.group()

    # Si aucune correspondance n'est trouvée, rechercher la correspondance la plus proche
    else:
        date_corrige = process.extractOne(date, [date_standard])[0]
        return date_corrige

# Exemples d'utilisation
dates = [
    "2024/04/15", "2024-04-15", "2024\04\15", "15-04-2024",
    "2023/12/31", "2023-12-31", "2023\12\31", "31-12-2023",
    "2024/01/32", "2024-13-01", "32\01\2024", "01-13-2024"
]

for date in dates:
    date_correcte = corriger_faute_de_frappe(date)
    date_standard = convertir_date_vers_format_standard(date_correcte)
    print(f"{date} => {date_standard}")
from datetime import datetime, timedelta

# Déclarer la variable time avec l'heure 00:00
time = datetime.strptime('00:00', '%H:%M')

# Ajouter une heure
time = time + timedelta(hours=1)

# Afficher le temps actuel
print(time.strftime('%H:%M'))

import requests
import json
import os

# Création dossier stock images
os.makedirs("pokemon_images", exist_ok=True)
os.makedirs("item_images", exist_ok=True)  # Création dossier pour les images des objets

# URL pour récupérer les 18 types et les objets
types_url = "https://pokeapi.co/api/v2/type/"
items_url = "https://pokeapi.co/api/v2/item/"
berries_url = "https://pokeapi.co/api/v2/berry/"  # URL pour les baies

# Effectuer GET
response = requests.get(types_url)
items_response = requests.get(items_url)
berries_response = requests.get(berries_url)

# Vérifier si ça marche
if response.status_code == 200 and items_response.status_code == 200 and berries_response.status_code == 200:
    types_data = response.json()  # Convert en JSON
    items_data = items_response.json()
    berries_data = berries_response.json()

    # Créer un JSON 
    battle_items = {"items": []}  # Suppression des catégories combat et level-up

    # Liste des objets à récupérer
    item_names = [
        "wise-glasses", "muscle-band", "adamant-orb", "lustrous-orb", 
        "choice-band", "choice-specs", "life-orb", "metronome", "expert-belt"
    ]

    # Récupérer les objets spécifiques
    for item_name in item_names:
        item_url = f"{items_url}{item_name}/"
        item_response = requests.get(item_url)
        
        if item_response.status_code == 200:
            item_data = item_response.json()
            
            # Récupérer l'effet et garder uniquement les informations essentielles
            effect = next((entry["effect"] for entry in item_data.get("effect_entries", []) if entry["language"]["name"] in ["en", "fr"]), "N/A")
            
            item_entry = {
                "name": item_data["name"],
                "effect": effect,
            }

            battle_items["items"].append(item_entry)
        else:
            print(f"Erreur lors de la récupération de l'objet {item_name}")

    # Sauvegarde avec les données simplifiées
    with open("pokemon_battle_items_simple.json", "w") as file:
        json.dump(battle_items, file, indent=4)
    
    print("Les données des objets ont été mises à jour avec les informations simplifiées.")
else:
    print("Erreur lors de la récupération des données.")

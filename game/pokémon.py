import requests
import json
import os

# la ya 36 pokemons en tout j'ai fait 2 par types pour changer ca cest ligne 28 ["pokemon"][:2]
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
    pokemon_db = {}
    battle_items = {"items": []}  # Suppression des catégories combat et level-up
    berries_list = {"berries": []}  # Stockage des baies

    # Pour récupérer les 18 types
    for type_info in types_data["results"]:
        type_name = type_info["name"]
        type_folder = f"pokemon_images/{type_name}"  # Création dossier par type
        os.makedirs(type_folder, exist_ok=True)
        
        pokemon_db[type_name] = {"pokemons": []}
        
        type_detail = requests.get(type_info["url"]).json()
        pokemons = type_detail["pokemon"][:2]  # Pour chg le nbr de Pokémon récup
        
        for p in pokemons:
            pokemon_name = p["pokemon"]["name"]
            pokemon_entry = {"name": pokemon_name, "image": "", "evolutions": [], "stats": {}, "moves": {}}

            # Récupérer l'URL de l'espèce pour l'évolution
            species_url = f"https://pokeapi.co/api/v2/pokemon-species/{pokemon_name}/"
            species_response = requests.get(species_url)
            
            if species_response.status_code == 200:
                species_data = species_response.json()
                evolution_chain_url = species_data["evolution_chain"]["url"]

                # Récup les évolutions
                evolution_response = requests.get(evolution_chain_url)
                if evolution_response.status_code == 200:
                    evolution_data = evolution_response.json()
                    evolution_chain = []

                    evo_stage = evolution_data["chain"]
                    while evo_stage:
                        evo_name = evo_stage["species"]["name"]
                        evolution_chain.append(evo_name)
                        evo_stage = evo_stage["evolves_to"][0] if evo_stage["evolves_to"] else None

                    # Ajt lévolution
                    pokemon_entry["evolutions"] = evolution_chain

            # Récup stat et images
            pokemon_data = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}/").json()
            
            if "sprites" in pokemon_data and "front_default" in pokemon_data["sprites"]:
                image_url = pokemon_data["sprites"]["front_default"]
                image_path = f"{type_folder}/{pokemon_name}.png"
                img_response = requests.get(image_url, verify=False)
                if img_response.status_code == 200:
                    with open(image_path, "wb") as img_file:
                        img_file.write(img_response.content)
                    print(f"Image sauvegardée : {image_path}")
                pokemon_entry["image"] = image_url
            
            # Récup stats
            for stat in pokemon_data["stats"]:
                stat_name = stat["stat"]["name"]
                stat_value = stat["base_stat"]
                pokemon_entry["stats"][stat_name] = stat_value
            
            # Init du dictio moves
            pokemon_entry["moves"] = {}
            
            # Récup attaques et stats
            for move in pokemon_data["moves"][:2]:  # Limité à 2 attaques par Pokémon (modifiable)
                move_name = move["move"]["name"]
                move_data = requests.get(move["move"]["url"]).json()
                
                move_entry = {
                    "power": move_data.get("power", "N/A"),
                    "accuracy": move_data.get("accuracy", "N/A"),
                    "pp": move_data.get("pp", "N/A"),
                    "type": move_data["type"]["name"],
                    "category": move_data["damage_class"]["name"],
                    "effect": next((entry["effect"] for entry in move_data["effect_entries"] if entry["language"]["name"] == "en"), "N/A"),
                    "image": ""
                }
                
                pokemon_entry["moves"][move_name] = move_entry
            
            # Ajoute le Pokémon 
            pokemon_db[type_name]["pokemons"].append(pokemon_entry)
    
    # Récupération des objets avec stats
    for item in items_data["results"]:
        item_data = requests.get(item["url"]).json()
        item_entry = {
            "name": item_data["name"],
            "effect": next((entry["effect"] for entry in item_data.get("effect_entries", []) if entry["language"]["name"] == "en"), "N/A"),
            "image": item_data["sprites"]["default"] if "sprites" in item_data else "",
            "stats": item_data  # Ajout de toutes les stats disponibles
        }
        battle_items["items"].append(item_entry)
    
    # Sauvegarde
    with open("pokemon_types_evolutions_images.json", "w") as file:
        json.dump(pokemon_db, file, indent=4)
    with open("pokemon_battle_items_stats.json", "w") as file:
        json.dump(battle_items, file, indent=4)
    
    print("Les données ont été mises à jour avec les stats complètes des objets en anglais uniquement.")
else:
    print("Erreur lors de la récupération des données.")

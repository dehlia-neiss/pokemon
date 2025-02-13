import requests
import json
import os

# la ya 36 pokemons en tout j'ai fait 2 par types pour changer ca cest ligne 28 ["pokemon"][:2]
# Création dossier stock images
os.makedirs("pokemon_images", exist_ok=True)

# URL pour récupérer les 18 types
types_url = "https://pokeapi.co/api/v2/type/"

# Effectuer GET
response = requests.get(types_url)

# Vérifier si ça marche
if response.status_code == 200:
    types_data = response.json()  # Convert en JSON
    
    # Créer un JSON 
    pokemon_db = {}

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

            # Récupérer l'URL de l'espèce pour accéder à l'évolution
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

            # Récupération des statistiques et images
            pokemon_data = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}/").json()
            
            if "sprites" in pokemon_data and "front_default" in pokemon_data["sprites"]:
                image_url = pokemon_data["sprites"]["front_default"]
                image_path = f"{type_folder}/{pokemon_name}.png"
                img_response = requests.get(image_url)
                if img_response.status_code == 200:
                    with open(image_path, "wb") as img_file:
                        img_file.write(img_response.content)
                    print(f"Image sauvegardée : {image_path}")
                pokemon_entry["image"] = image_url
            
            # Récupération des stats
            for stat in pokemon_data["stats"]:
                stat_name = stat["stat"]["name"]
                stat_value = stat["base_stat"]
                pokemon_entry["stats"][stat_name] = stat_value
            
            # Initialisation du dictionnaire moves
            pokemon_entry["moves"] = {}
            
            # Récupération des attaques et stats des attaques
            for move in pokemon_data["moves"][:2]:  # Limité à 2 attaques par Pokémon (modifiable)
                move_name = move["move"]["name"]
                move_data = requests.get(move["move"]["url"]).json()
                
                move_entry = {
                    "power": move_data.get("power", "N/A"),
                    "accuracy": move_data.get("accuracy", "N/A"),
                    "pp": move_data.get("pp", "N/A"),
                    "type": move_data["type"]["name"],
                    "category": move_data["damage_class"]["name"],
                    "effect": move_data["effect_entries"][0]["effect"] if move_data["effect_entries"] else "N/A",
                    "image": ""
                }
                
                # Téléchargement de l'image d'attaque (si dispo)
                if "sprites" in move_data:
                    move_image_url = move_data["sprites"].get("default", "")
                    if move_image_url:
                        move_image_path = f"{type_folder}/{move_name}.png"
                        img_response = requests.get(move_image_url)
                        if img_response.status_code == 200:
                            with open(move_image_path, "wb") as img_file:
                                img_file.write(img_response.content)
                            print(f"Image d'attaque sauvegardée : {move_image_path}")
                        move_entry["image"] = move_image_url
                
                pokemon_entry["moves"][move_name] = move_entry
            
            # Ajoute le Pokémon 
            pokemon_db[type_name]["pokemons"].append(pokemon_entry)

    # Sauvegarde dans un JSON
    with open("pokemon_types_evolutions_images.json", "w") as file:
        json.dump(pokemon_db, file, indent=4)

    print("Les données avec images et stats ont été sauvegardées dans 'pokemon_types_evolutions_images.json'")

else:
    print("Erreur lors de la récupération des types :", response.status_code)

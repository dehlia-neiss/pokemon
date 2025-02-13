import requests
import json
import os

# la ya 36 pokemons en tout j'ai fait 2 par types pour changer ca cest ligne 28 ["pokemon"][:2]
# Création du dossier pour stocker les images
os.makedirs("pokemon_images", exist_ok=True)
os.makedirs("item_images", exist_ok=True)  # Dossier pour stocker les images des objets

# URL pour récupérer les 18 types et les objets
types_url = "https://pokeapi.co/api/v2/type/"
items_url = "https://pokeapi.co/api/v2/item/"

# Effectuer GET pour récupérer les types et les objets
response = requests.get(types_url)
items_response = requests.get(items_url)

# Vérifier si les requêtes sont réussies
if response.status_code == 200 and items_response.status_code == 200:
    types_data = response.json()  # Convertir en JSON
    items_data = items_response.json()

    # Dictionnaire pour stocker les Pokémon et leurs informations
    pokemon_db = {}
    battle_items = {"combat_items": [], "level_up_items": []}

    # Pour récupérer les types de Pokémon
    for type_info in types_data["results"]:
        type_name = type_info["name"]
        type_folder = f"pokemon_images/{type_name}"  # Création d'un dossier par type
        os.makedirs(type_folder, exist_ok=True)

        pokemon_db[type_name] = {"pokemons": []}

        type_detail = requests.get(type_info["url"]).json()
        pokemons = type_detail["pokemon"][:2]  # Limité à 2 Pokémon par type pour l'exemple

        for p in pokemons:
            pokemon_name = p["pokemon"]["name"]
            pokemon_entry = {"name": pokemon_name, "image": "", "evolutions": [], "stats": {}, "moves": {}}

            # Récupérer l'URL de l'espèce pour accéder à l'évolution
            species_url = f"https://pokeapi.co/api/v2/pokemon-species/{pokemon_name}/"
            species_response = requests.get(species_url)

            if species_response.status_code == 200:
                species_data = species_response.json()
                evolution_chain_url = species_data["evolution_chain"]["url"]

                # Récupérer les évolutions
                evolution_response = requests.get(evolution_chain_url)
                if evolution_response.status_code == 200:
                    evolution_data = evolution_response.json()
                    evolution_chain = []

                    evo_stage = evolution_data["chain"]
                    while evo_stage:
                        evo_name = evo_stage["species"]["name"]
                        evolution_chain.append(evo_name)
                        evo_stage = evo_stage["evolves_to"][0] if evo_stage["evolves_to"] else None

                    # Ajouter les évolutions
                    pokemon_entry["evolutions"] = evolution_chain

            # Récupération des statistiques et images
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

                pokemon_entry["moves"][move_name] = move_entry

            # Ajouter le Pokémon
            pokemon_db[type_name]["pokemons"].append(pokemon_entry)

    # Récupération des objets utiles pour les combats et level-up
    for item in items_data["results"]:  # On garde tous les objets
        item_data = requests.get(item["url"]).json()
        category = item_data["category"]["name"]
        item_entry = {"name": item_data["name"], "effect": item_data["effect_entries"][0]["effect"] if item_data["effect_entries"] else "N/A"}

        # Ajouter des objets utiles en combat et level-up
        if "battle" in category:
            battle_items["combat_items"].append(item_entry)
        elif "level-up" in category:
            battle_items["level_up_items"].append(item_entry)

        # Récupérer les images des objets (si disponibles)
        if "sprites" in item_data and "default" in item_data["sprites"]:
            item_image_url = item_data["sprites"]["default"]
            item_image_path = f"item_images/{item_data['name']}.png"
            item_img_response = requests.get(item_image_url, verify=False)
            if item_img_response.status_code == 200:
                with open(item_image_path, "wb") as item_img_file:
                    item_img_file.write(item_img_response.content)
                print(f"Image de l'objet sauvegardée : {item_image_path}")
            item_entry["image"] = item_image_url

    # Sauvegarde des données Pokémon et objets
    with open("pokemon_types_evolutions_images.json", "w") as file:
        json.dump(pokemon_db, file, indent=4)

    # Sauvegarde des objets utiles
    with open("pokemon_battle_items.json", "w") as file:
        json.dump(battle_items, file, indent=4)

    print("Les données avec images et stats ont été sauvegardées dans 'pokemon_types_evolutions_images.json'")
    print("Les objets utiles ont été sauvegardés dans 'pokemon_battle_items.json'")

else:
    print("Erreur lors de la récupération des types ou objets:", response.status_code, items_response.status_code)

import requests
import json
import os
#la ya 2 poke par type soit 36 pour changer ca c ligne 31
# Création du dossier principal pour stocker les images
os.makedirs("pokemon_images", exist_ok=True)

# URL pour récup les 18 type
types_url = "https://pokeapi.co/api/v2/type/"

# appel GET
response = requests.get(types_url)

# Vérifie si ca marche
if response.status_code == 200:
    types_data = response.json()  # Convert en JSON
    
    # Créer un JSON
    pokemon_db = {}

    # Pour récup les 18 types
    for type_info in types_data["results"]:
        type_name = type_info["name"]
        pokemon_db[type_name] = {"pokemons": []}

        # Création du dossier chaque type
        type_folder = f"pokemon_images/{type_name}"
        os.makedirs(type_folder, exist_ok=True)
        
        type_detail = requests.get(type_info["url"]).json()
        pokemons = type_detail["pokemon"][:2]  # Modifie pour changer le nmbr de Poké
        
        for p in pokemons:
            pokemon_name = p["pokemon"]["name"]
            pokemon_entry = {"name": pokemon_name, "sprites": {}, "evolutions": [], "moves": {}}

            # Création du dossier pour chaque Pokémon
            pokemon_folder = f"{type_folder}/{pokemon_name}"
            os.makedirs(pokemon_folder, exist_ok=True)

            # Récupére l'URL de l'espèce 
            species_url = f"https://pokeapi.co/api/v2/pokemon-species/{pokemon_name}/"
            species_response = requests.get(species_url)
            
            if species_response.status_code == 200:
                species_data = species_response.json()
                evolution_chain_url = species_data["evolution_chain"]["url"]

                # Récup les evolution
                evolution_response = requests.get(evolution_chain_url)
                if evolution_response.status_code == 200:
                    evolution_data = evolution_response.json()
                    evolution_chain = []

                    evo_stage = evolution_data["chain"]
                    while evo_stage:
                        evo_name = evo_stage["species"]["name"]
                        evolution_chain.append(evo_name)
                        evo_stage = evo_stage["evolves_to"][0] if evo_stage["evolves_to"] else None

                    #
                    pokemon_entry["evolutions"] = evolution_chain

                    # Télécharge image du Pokémon et évol
                    for evo in evolution_chain:
                        evo_data = requests.get(f"https://pokeapi.co/api/v2/pokemon/{evo}/").json()
                        if "sprites" in evo_data:
                            sprites = evo_data["sprites"]

                            # Liste ls images à recp
                            sprite_types = {
                                "front_default": sprites.get("front_default"),
                                "back_default": sprites.get("back_default"),
                                "front_shiny": sprites.get("front_shiny"),
                                "back_shiny": sprites.get("back_shiny"),
                                "front_female": sprites.get("front_female"),
                                "back_female": sprites.get("back_female"),
                                "front_shiny_female": sprites.get("front_shiny_female"),
                                "back_shiny_female": sprites.get("back_shiny_female")
                            }

                            # Télécharge + save les img
                            for key, url in sprite_types.items():
                                if url:
                                    img_response = requests.get(url)
                                    if img_response.status_code == 200:
                                        file_path = f"{type_folder}/{evo}/{key}.png"
                                        os.makedirs(os.path.dirname(file_path), exist_ok=True)
                                        with open(file_path, "wb") as img_file:
                                            img_file.write(img_response.content)
                                        print(f"Image sauvegardée : {file_path}")

                                        # Ajout l'URL 
                                        if evo == pokemon_name:
                                            pokemon_entry["sprites"][key] = url 
                                            moves = evo_data.get("moves", [])[:5]  # Modifier ce chiffre pour récupérer plus d'attaques
                    #pour les attaq
                    for move in moves:
                        move_name = move["move"]["name"]
                        move_url = move["move"]["url"]

                        #request pour récup l'attaque
                        move_response = requests.get(move_url)
                        if move_response.status_code == 200:
                            move_data = move_response.json()

                            move_entry = {"name": move_name, "image": None}

                            #
                            if "type" in move_data:
                                move_type = move_data["type"]["name"]
                                move_icon_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/types/{move_type}.png"

                                move_folder = f"{type_folder}/{pokemon_name}/moves"
                                os.makedirs(move_folder, exist_ok=True)
                                move_file_path = f"{move_folder}/{move_name}.png"

                                img_response = requests.get(move_icon_url)
                                if img_response.status_code == 200:
                                    with open(move_file_path, "wb") as img_file:
                                        img_file.write(img_response.content)
                                    print(f"Image de l'attaque sauvegardée : {move_file_path}")

                                    move_entry["image"] = move_icon_url

                            # Ajouter l'attaque au JSON
                            pokemon_entry["moves"][move_name] = move_entry
            # Ajoute le Pokémon a la lsite
            pokemon_db[type_name]["pokemons"].append(pokemon_entry)

    # Save dans un JSON
    with open("pokemon_types_evolutions_sprites.json", "w") as file:
        json.dump(pokemon_db, file, indent=4)

    print("Les données avec images et sprites ont été sauvegardées dans 'pokemon_types_evolutions_sprites.json'")

else:
    print("Erreur lors de la récupération des types :", response.status_code)

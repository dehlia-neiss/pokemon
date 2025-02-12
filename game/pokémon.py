import requests
import json
import os

# Création d'un dossier pour stocker les images
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
        pokemon_db[type_name] = {"pokemons": []}
        
        type_detail = requests.get(type_info["url"]).json()
        pokemons = type_detail["pokemon"][:2]  # Pour changer le nombre de Pokémon récupérés
        
        for p in pokemons:
            pokemon_name = p["pokemon"]["name"]
            pokemon_entry = {"name": pokemon_name, "image": "", "evolutions": []}

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

                    # Ajouter l'évolution à l'entrée du Pokémon
                    pokemon_entry["evolutions"] = evolution_chain

                    # Télécharger les images des Pokémon et de leurs évolutions
                    for evo in evolution_chain:
                        evo_data = requests.get(f"https://pokeapi.co/api/v2/pokemon/{evo}/").json()
                        if "sprites" in evo_data and "front_default" in evo_data["sprites"]:
                            evo_image_url = evo_data["sprites"]["front_default"]
                            image_path = f"pokemon_images/{evo}.png"
                            
                            # Télécharger et enregistrer l'image
                            img_response = requests.get(evo_image_url)
                            if img_response.status_code == 200:
                                with open(image_path, "wb") as img_file:
                                    img_file.write(img_response.content)
                                print(f"Image sauvegardée pour {evo} -> {image_path}")
                            
                            # Sauvegarder l'URL de l'image
                            if evo == pokemon_name:
                                pokemon_entry["image"] = evo_image_url

            # Ajouter le Pokémon à la base de données
            pokemon_db[type_name]["pokemons"].append(pokemon_entry)

    # Sauvegarder les données dans un fichier JSON
    with open("pokemon_types_evolutions_images.json", "w") as file:
        json.dump(pokemon_db, file, indent=4)

    print("Les données avec images ont été sauvegardées dans 'pokemon_types_evolutions_images.json'")

else:
    print("Erreur lors de la récupération des types :", response.status_code)

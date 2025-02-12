import requests
import json

# URL pour récupérer les 18 type
types_url = "https://pokeapi.co/api/v2/type/"

# Effectuer GET
response = requests.get(types_url)

# Vérifier si sa marche
if response.status_code == 200:
    types_data = response.json()  # Convert en JSON
    
    # Créer un JSON 
    pokemon_db = {}

    # pour recup les 18 types
    for type_info in types_data["results"]:
        type_name = type_info["name"]
        pokemon_db[type_name] = {"pokemons": [], "evolutions": []}
        
        type_detail = requests.get(type_info["url"]).json()
        pokemons = type_detail["pokemon"][:2]  # pour changer le nombre
        
        for p in pokemons:
            pokemon_name = p["pokemon"]["name"]
            pokemon_db[type_name]["pokemons"].append(pokemon_name)

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
                        evolution_chain.append(evo_stage["species"]["name"])
                        evo_stage = evo_stage["evolves_to"][0] if evo_stage["evolves_to"] else None

                    # evolution dans la liste
                    pokemon_db[type_name]["evolutions"].append(evolution_chain)

    # pour save dans le json
    with open("pokemon_types_evolutions.json", "w") as file:
        json.dump(pokemon_db, file, indent=4)

    print("Les données des types et évolutions ont été sauvegardées dans 'pokemon_types_evolutions.json'")

else:
    print("Erreur lors de la récupération des types :", response.status_code)

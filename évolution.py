import json
import os
import random
import pygame

# Fonction pour charger les données du Pokémon depuis le fichier JSON
def charger_pokemon(nom_pokemon):
    if os.path.exists('pokemon_saves.json'):
        with open('pokemon_saves.json', 'r') as file:
            data = json.load(file)
        return data.get(nom_pokemon, None)
    return None

# Fonction pour sauvegarder les données du Pokémon après chaque victoire
def sauvegarder_pokemon(nom_pokemon, pokemon_data):
    if os.path.exists('pokemon_saves.json'):
        with open('pokemon_saves.json', 'r') as file:
            data = json.load(file)
    else:
        data = {}

    data[nom_pokemon] = pokemon_data
    with open('pokemon_saves.json', 'w') as file:
        json.dump(data, file, indent=4)

# Fonction qui gère l'évolution du Pokémon
def verifier_evolution(pokemon_data):
    if pokemon_data["victoires"] >= 3:
        pokemon_data["victoires"] = 0  # Réinitialiser le compteur de victoires
        pokemon_data["nom"] = pokemon_data["evolue_a"]  # Changer le nom du Pokémon (évolution)
        # Mise à jour des stats (pour l'exemple, on augmente juste l'attaque et la défense)
        pokemon_data["stats"]["attaque"] += 20
        pokemon_data["stats"]["defense"] += 20
        pokemon_data["sprite"] = f"{pokemon_data['nom'].lower()}.png"  # Changer le sprite du Pokémon évolué
        print(f"{pokemon_data['nom']} a évolué en {pokemon_data['evolue_a']}!")
    
    return pokemon_data

# Fonction qui gère la victoire d'un combat
def victoire_combat(nom_pokemon):
    pokemon_data = charger_pokemon(nom_pokemon)
    if pokemon_data:
        pokemon_data["victoires"] += 1  # Ajouter une victoire
        pokemon_data = verifier_evolution(pokemon_data)  # Vérifier si le Pokémon évolue
        sauvegarder_pokemon(nom_pokemon, pokemon_data)  # Sauvegarder les données du Pokémon
    else:
        print(f"Le Pokémon {nom_pokemon} n'a pas été trouvé.")

# Exemple d'appel après une victoire
victoire_combat("Pikachu")

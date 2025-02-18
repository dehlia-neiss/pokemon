import json
import os
import pygame

# Charger les données du Pokémon depuis le fichier pokedex.json
def load_pokemon_from_pokedex(pokemon_name):
    if os.path.exists('pokedex.json'):
        with open('pokedex.json', 'r') as file:
            data = json.load(file)
        return data.get(pokemon_name, None)  # Récupérer les données du Pokémon par son nom
    return None

# Sauvegarder les données modifiées du Pokémon dans le fichier pokemon_saves.json
def save_pokemon(pokemon_name, pokemon_data):
    if os.path.exists('sauvegarde.json'):
        with open('sauvegarde.json', 'r') as file:
            data = json.load(file)
    else:
        data = {}

    data[pokemon_name] = pokemon_data
    with open('sauvegarde.json', 'w') as file:
        json.dump(data, file, indent=4)

# Gérer l’évolution du Pokémon (niveau 5)
def check_evolution(pokemon_data):
    if pokemon_data["level"] >= 5:  # Si le niveau est >= 5, évolution
        pokemon_data["victories"] = 0  # Réinitialiser les victoires
        pokemon_data["name"] = pokemon_data["evolves_to"]  # Changer le nom du Pokémon après évolution
        # Mise à jour des stats après évolution
        pokemon_data["stats"]["attack"] += 20
        pokemon_data["stats"]["defense"] += 20
        pokemon_data["sprite"] = f"{pokemon_data['name'].lower()}.png"  # Nouveau sprite après évolution
        print(f"{pokemon_data['name']} evolved into {pokemon_data['evolves_to']}!")
    
    return pokemon_data

# Fonction appelée après une victoire en combat
def victory_battle(pokemon_name):
    pokemon_data = load_pokemon_from_pokedex(pokemon_name)  # Charger les données depuis pokedex.json
    if pokemon_data:
        pokemon_data["victories"] += 1  # Ajouter une victoire
        pokemon_data = check_evolution(pokemon_data)  # Vérifier si Pokémon doit évoluer
        save_pokemon(pokemon_name, pokemon_data)  # Sauvegarder les données du Pokémon modifié
    else:
        print(f"The Pokémon {pokemon_name} was not found in the Pokédex.")

# Classe représentant un Pokémon
class Pokemon:
    def __init__(self, name, level, species, stats, evolves_to=None):
        self.name = name
        self.level = level
        self.species = species
        self.stats = stats
        self.evolves_to = evolves_to
        self.is_evolved = False

    # Méthode pour simuler une victoire en combat
    def win_battle(self):
        self.level += 1  # Augmenter le niveau du Pokémon après une victoire
        print(f"{self.name} won a battle and is now at level {self.level}.")

# Simuler l’évolution de Bulbasaur
bulbasaur_data = load_pokemon_from_pokedex("abra")  # Charger les données de Bulbasaur depuis pokedex.json
if bulbasaur_data:
    victory_battle("abra")  # Simuler une victoire
else:
    print("Bulbasaur was not found in the Pokédex.")

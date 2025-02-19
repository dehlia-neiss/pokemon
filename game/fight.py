
import random
import json
import random
import os

# Tableau des multiplicateurs de type
TYPE_MULTIPLIERS = {
    "normal": {"roche": 0.5, "spectre": 0, "acier": 0.5},
    "plante": {"eau": 2, "feu": 0.5, "plante": 0.5, "poison": 0.5, "sol": 2, "vol": 0.5},
    "feu": {"plante": 2, "eau": 0.5, "feu": 0.5, "glace": 2, "insecte": 2, "acier": 2, "roche": 0.5, "dragon": 0.5},
    "eau": {"feu": 2, "plante": 0.5, "eau": 0.5, "sol": 2, "roche": 2, "dragon": 0.5},
    "electrik": {"eau": 2, "electrik": 0.5, "sol": 0, "vol": 2, "dragon": 0.5},
    "glace": {"plante": 2, "feu": 0.5, "eau": 0.5, "glace": 0.5, "sol": 2, "vol": 2, "dragon": 2, "acier": 0.5},
    "combat": {"normal": 2, "glace": 2, "roche": 2, "tenebres": 2, "acier": 2, "poison": 0.5, "vol": 0.5, "psy": 0.5, "spectre": 0, "fee": 0.5},
    # Ajout d'autres types si nécessaire
}

class Pokemon:
    def __init__(self, life, name, attack, defense, element, moves, special_attack=50, special_defense=50, possessed_object=None):
        self.life = life
        self.max_life = life
        self.level = 1  # Niveau par défaut à 1
        self.name = name
        self.attack = attack
        self.defense = defense
        self.special_attack = special_attack
        self.special_defense = special_defense
        self.element = element  # Type du Pokémon
        self.moves = moves  # Attaques du Pokémon
        self.possessed_object = possessed_object  # Objet tenu par le Pokémon
        self.pokeballs = 1  # Ajout de pokéballs pour la capture

class Combat:
    def __init__(self, fighter1, fighter2):
        self.fighter1 = fighter1
        self.fighter2 = fighter2
        self.player_turn = True

    def get_type_multiplier(self, move_type, defender_type):
        return TYPE_MULTIPLIERS.get(move_type, {}).get(defender_type, 1)

    def second_modifier(self, attacker):
        if attacker.possessed_object == "orbe de vie":
            return 1.3
        elif attacker.possessed_object == "moi d'abord":
            return 1.5
        elif attacker.possessed_object == "metronome":
            return 1.1  # Supposition d'un bonus progressif
        return 1

    def third_modifier(self, defender, attack_effectiveness):
        sfr = 0.75 if defender.element == "solide roc" else 1
        eb = 1.2 if defender.element == "ceinture pro" else 1
        tl = 2 if defender.element == "lentiteintée" and attack_effectiveness < 1 else 1
        return sfr * eb * tl

    def calculate_damage(self, move, attacker, defender):
        power = move["power"]
        spe_att = attacker.special_attack
        spe_def = defender.special_defense
        type_multiplier = self.get_type_multiplier(move["type"], defender.element)
        cc = 1.5 if random.random() < 0.1 else 1  # Chance de coup critique
        STAB = 1.5 if move["type"] == attacker.element else 1
        r = random.randint(85, 100)  # Facteur de variation des dégâts
        mod2 = self.second_modifier(attacker)
        mod3 = self.third_modifier(defender, type_multiplier)

        damage = ((((attacker.level * 2 / 5 + 2) * power * spe_att / 50) / spe_def) + 2) * cc * r / 100 * STAB * type_multiplier * mod2 * mod3
        damage = max(1, int(damage))
        defender.life = max(0, defender.life - damage)
        return damage

    def capture_pokemon(self, player, wild_pokemon):
        if wild_pokemon.life <= (wild_pokemon.max_life * 0.2) and player.pokeballs > 0:
            player.pokeballs -= 1
            print(f"{wild_pokemon.name} a été capturé !")

            # Charger l'ancienne sauvegarde si elle existe
            save_file = "sauvegarde.json"
            if os.path.exists(save_file):
                with open(save_file, "r") as f:
                    try:
                        saved_data = json.load(f)
                    except json.JSONDecodeError:
                        saved_data = {"captured_pokemon": []}
            else:
                saved_data = {"captured_pokemon": []}

            # Ajouter le Pokémon capturé
            captured_pokemon = {
                "name": wild_pokemon.name,
                "life": wild_pokemon.life,
                "max_life": wild_pokemon.max_life,
                "attack": wild_pokemon.attack,
                "defense": wild_pokemon.defense,
                "special-attack": wild_pokemon.special_attack,
                "special-defense": wild_pokemon.special_defense,
                "element": wild_pokemon.element,
                "moves": wild_pokemon.moves
            }
            saved_data["captured_pokemon"].append(captured_pokemon)

            # Enregistrer dans le fichier sauvegarde.json
            with open(save_file, "w") as f:
                json.dump(saved_data, f, indent=4)

            return True  # Capture réussie
        return False  # Capture échouée

    def choose_pokemon(pokedex):
        print("Choisissez un Pokémon parmi ceux disponibles:")
        all_pokemon = []
        
        # Créer une liste de Pokémon avec leur type
        for type_name, type_category in pokedex.items():
            for pokemon in type_category["pokemons"]:
                all_pokemon.append((pokemon, type_name))  # Stocke aussi le type

        # Afficher les Pokémon avec leur type
        for i, (pokemon, poke_type) in enumerate(all_pokemon, 1):
            print(f"{i}. {pokemon['name']} ({poke_type})")  # Utilise poke_type au lieu de pokemon['type']

        # Sécurisation de l'entrée utilisateur
        while True:
            try:
                choice = int(input("Entrez le numéro du Pokémon: ")) - 1
                if 0 <= choice < len(all_pokemon):
                    return all_pokemon[choice]  # Retourne le Pokémon et son type
                else:
                    print("Veuillez entrer un nombre valide.")
            except ValueError:
                print("Entrée invalide, veuillez entrer un numéro.")

    def choose_attack(self, attacker, defender):
        print(f"{attacker.name} HP: {attacker.life} | {defender.name} HP: {defender.life}")
        print("Actions disponibles :")
        print("0. Tenter une capture")  # Option pour capturer

        moves = list(attacker.moves.keys())
        for i, move in enumerate(moves, 1):
            print(f"{i}. {move} (Power: {attacker.moves[move]['power']}, Accuracy: {attacker.moves[move]['accuracy']})")

        while True:
            try:
                choice = int(input("Entrez le numéro de votre action: "))
                if choice == 0:
                    if self.capture_pokemon(attacker, defender):
                        return "captured"  # Retourne "captured" pour arrêter le combat
                    else:
                        print("La capture a échoué !")
                        return "failed"
                elif 1 <= choice <= len(moves):
                    selected_move = moves[choice - 1]
                    damage = self.calculate_damage(attacker.moves[selected_move], attacker, defender)
                    print(f"{attacker.name} utilise {selected_move} et inflige {damage} dégâts à {defender.name}!")
                    return "attack"
                else:
                    print("Choix invalide, essayez encore.")
            except ValueError:
                print("Entrée invalide, veuillez entrer un numéro.")

    def attack(self):
        while self.fighter1.life > 0 and self.fighter2.life > 0:
            if self.player_turn:
                action_result = self.choose_attack(self.fighter1, self.fighter2)
                if action_result == "captured":  # Arrêter le combat en cas de capture
                    print(f"{self.fighter2.name} a été capturé ! Fin du combat.")
                    return  
            else:
                self.choose_attack(self.fighter2, self.fighter1)

            self.player_turn = not self.player_turn

        winner = self.fighter1 if self.fighter1.life > 0 else self.fighter2
        print(f"{winner.name} gagne le combat!")
    
    def find_pokemon_type(pokedex, pokemon_name):
        """Trouve le type d'un Pokémon à partir du JSON."""
        for type_name, type_data in pokedex.items():
            for pokemon in type_data["pokemons"]:
                if pokemon["name"] == pokemon_name:
                    return type_name  # Retourne le type trouvé
        return "normal" 

if __name__ == "__main__":
    with open("pokedex.json", "r") as f:
        pokedex = json.load(f)

    # Choix du premier Pokémon
    print("Bienvenue dans le monde des Pokémon !")
    p1_data, p1_type = Combat.choose_pokemon(pokedex)

    # Choix du deuxième Pokémon aléatoire
    all_pokemon = []
    for type_category in pokedex.values():
        all_pokemon.extend(type_category["pokemons"])  # Récupérer tous les Pokémon
    p2_data, p2_type = random.choice([(p, t) for t, v in pokedex.items() for p in v["pokemons"]])  # Sélection aléatoire parmi tous les Pokémon

      # Récupère le Pokémon ET son type
    

    p1 = Pokemon(
        life=p1_data["stats"]["hp"], 
        attack=p1_data["stats"]["attack"], 
        defense=p1_data["stats"]["defense"], 
        special_attack=p1_data["stats"]["special-attack"], 
        special_defense=p1_data["stats"]["special-defense"], 
        name=p1_data["name"], 
        element=p1_type,  # Utilisation du type trouvé
        moves=p1_data["moves"]
    )

    p2 = Pokemon(
        life=p2_data["stats"]["hp"], 
        attack=p2_data["stats"]["attack"], 
        defense=p2_data["stats"]["defense"], 
        special_attack=p2_data["stats"]["special-attack"], 
        special_defense=p2_data["stats"]["special-defense"], 
        name=p2_data["name"], 
        element=p2_type,  # Utilisation du type trouvé
        moves=p2_data["moves"]
    )
            
    combat = Combat(p1, p2)
    combat.attack()
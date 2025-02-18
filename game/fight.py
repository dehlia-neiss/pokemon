import json
import random
class Pokemon:
    def __init__(self, life, name, attack, defense, element, moves, possessed_object=None):
        self.life = life
        self.level = 1  # Default level is 1
        self.name = name
        self.attack = attack
        self.defense = defense
        self.special_attack = 50  # Default special attack
        self.special_defense = 50  # Default special defense
        self.element = element  # Type of the Pokémon
        self.moves = moves  # Pokémon's moves
        self.possessed_object = possessed_object  # Held item (optional)

    def get_item_modifier(self):
        # This method returns the multiplier based on the held item
        item_effects = {
            "wise-glasses": 1.1,  # Increase power of special moves by 10%
            "muscle-band": 1.1,   # Increase power of physical moves by 10%
            "adamant-orb": 1.2,   # Increase dragon- and steel-type moves' power
            "lustrous-orb": 1.2,  # Increase dragon- and water-type moves' power
            "choice-band": 1.5,   # Increase Attack by 50%, restrict to one move
            "choice-specs": 1.5,  # Increase Special Attack by 50%, restrict to one move
            "life-orb": 1.3,      # Increase damage by 30%, but lose 10% HP per move
            "metronome": 1.1,     # Increase power of consecutive same moves by 10%
            "expert-belt": 1.2    # Increase power of super-effective moves by 20%
        }

        if self.possessed_object in item_effects:
            return item_effects[self.possessed_object]
        return 1  # Default modifier (no item or item not in the list)

class Combat:
    def __init__(self, fighter1, fighter2):
        self.fighter1 = fighter1
        self.fighter2 = fighter2
        self.player_turn = True

    def second_modifier(self, pokemon):
        # Modifier for specific held items
        if pokemon.possessed_object == "orbe de vie":
            return 1.3
        elif pokemon.possessed_object == "moi d'abord":
            return 1.5
        elif pokemon.possessed_object == "metronome":
            mod2 = 1
            for _ in range(3):  # Simulate a combo of consecutive moves
                mod2 += 0.1
            return mod2
        return 1

    def third_modifier(self, attacker, defender, move_effectiveness):
        # Custom modifiers for specific situations
        sfr = 0.75 if defender.element == "solide roc" else 1
        eb = 1.2 if attacker.possessed_object == "ceinture pro" else 1
        tl = 2 if attacker.possessed_object == "lentiteintée" and move_effectiveness == "peu efficace" else 1
        return sfr * eb * tl

    def calculate_damage(self, move, attacker, defender):
        power = move["power"]
        spe_att = attacker.special_attack
        spe_def = defender.special_defense
        mod1 = 1
        mod2 = self.second_modifier(attacker)
        mod3 = self.third_modifier(attacker, defender, "normal")  # Placeholder for effectiveness
        cc = 1.5 if random.random() < 0.1 else 1  # Critical hit chance
        STAB = 1.5 if move["type"] == attacker.element else 1
        element1, element2 = 1, 1  # Elemental affinity factors (to be added)
        r = random.randint(85, 100)  # Random damage variation
        
        # Apply item modifier
        item_modifier = attacker.get_item_modifier()
        
        damage = (((((attacker.level * 2 / 5 + 2) * power * spe_att / 50) / spe_def) * mod1) + 2) * cc * mod2 * r / 100 * STAB * element1 * element2 * mod3 * item_modifier
        
        # For Life Orb, apply HP drain after calculating damage
        if attacker.possessed_object == "life-orb":
            attacker.life -= int(attacker.life * 0.10)
        
        # Ensure damage is at least 1, and the opponent's HP doesn't go below 0
        damage = max(1, int(damage))
        defender.life = max(0, defender.life - damage)
        return damage

    def choose_attack(self, attacker, defender):
        print(f"{attacker.name} HP: {attacker.life} | {defender.name} HP: {defender.life}")
        print(f"Choose an attack for {attacker.name}:")
        moves = list(attacker.moves.keys())
        for i, move in enumerate(moves, 1):
            print(f"{i}. {move} (Power: {attacker.moves[move]['power']}, Accuracy: {attacker.moves[move]['accuracy']})")
        
        while True:
            try:
                choice = int(input("Enter the number of the attack: ")) - 1
                if 0 <= choice < len(moves):
                    selected_move = moves[choice]
                    damage = self.calculate_damage(attacker.moves[selected_move], attacker, defender)
                    print(f"{attacker.name} used {selected_move} and dealt {damage} damage to {defender.name}!")
                    return f"{attacker.name} HP: {attacker.life} | {defender.name} HP: {defender.life}"
                else:
                    print("Invalid choice, please choose a number from the list.")
            except ValueError:
                print("Please enter a valid number.")

    def attack(self):
        while self.fighter1.life > 0 and self.fighter2.life > 0:
            if self.player_turn:
                self.choose_attack(self.fighter1, self.fighter2)
            else:
                self.choose_attack(self.fighter2, self.fighter1)
            self.player_turn = not self.player_turn
        winner = self.fighter1 if self.fighter1.life > 0 else self.fighter2
        print(f"{winner.name} wins the battle!")

def choose_pokemon(pokedex):
    print("Choose your Pokémon:")
    all_pokemons = []

    # Debugging the structure of pokedex
    print("Pokedex structure:", pokedex)

    for category in pokedex.values():
        # Debugging each category
        print("Category data:", category)
        
        if "pokemons" in category:
            all_pokemons.extend(category["pokemons"])
        else:
            print("No 'pokemons' key found in category:", category)

    for i, p in enumerate(all_pokemons, 1):
        print(f"{i}. {p['name']}")

    choice = int(input("Enter the number of your Pokémon: ")) - 1
    if 0 <= choice < len(all_pokemons):
        p_data = all_pokemons[choice]
        return Pokemon(
            life=p_data["stats"]["hp"], 
            name=p_data["name"], 
            attack=p_data["stats"]["attack"],
            defense=p_data["stats"]["defense"], 
            element="normal",  # Here you can change the element dynamically, if needed
            moves=p_data["moves"]
        )
    return None

def capture_pokemon(self, wild_pokemon):
    if wild_pokemon.life / wild_pokemon.max_life <= 0.05 and self.pokeballs > 0:
        self.pokeballs -= 1
        print(f"{wild_pokemon.name} has been captured!")
        return True
    print("Capture failed! Either the Pokémon has too much health or you have no Pokéballs left.")
    return False

if __name__ == "__main__":
    with open("pokedex.json", "r") as f:
        pokedex = json.load(f)
    
    p1 = choose_pokemon(pokedex)
    p2 = choose_pokemon(pokedex)
    
    if p1 and p2:
        combat = Combat(p1, p2)
        combat.attack()
    else:
        print("Invalid Pokémon selection.")
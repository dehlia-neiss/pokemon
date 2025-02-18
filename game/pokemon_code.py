# Pokémon class to handle basic data, stats, and evolution
class Pokemon:
    def __init__(self, name, level, species, stats, evolution_method=None):
        self.name = name
        self.level = level
        self.species = species
        self.stats = stats  # This is a dict of stats like HP, Attack, Defense, etc.
        self.evolution_method = evolution_method
        self.is_evolved = False

    def calculate_stats(self):
        # Stats calculation method (simplified formula)
        self.stats['HP'] = (self.level * 2) + 10
        self.stats['Attack'] = self.level * 1.5
        self.stats['Defense'] = self.level * 1.2
        self.stats['Speed'] = self.level * 1.1

    def evolve(self):
        if not self.is_evolved and self.evolution_method:
            if self.evolution_method(self):
                self.species = self.evolution_method(self)['evolution']
                self.is_evolved = True
                print(f'{self.name} evolved into {self.species}!')

# Example of simple evolution logic
def evolution_method(pokemon):
    if pokemon.level >= 16:  # Example: evolves at level 16
        return {'evolution': f'{pokemon.name} evolved!'}
    return None

# Pokémon data (example)
pikachu = Pokemon('Pikachu', 10, 'Pikachu', {'HP': 10, 'Attack': 15, 'Defense': 10, 'Speed': 20}, evolution_method)

pikachu.calculate_stats()
print(pikachu.stats)
pikachu.evolve()

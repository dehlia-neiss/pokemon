import pygame
import requests
import json

with open("pokemon_types_evolutions.json", "w") as file:
        json.dump( file, indent=4)

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pokédex")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

font = pygame.font.Font(None, 36)

def load_pokemon_image(url):
    response = requests.get(url)
    if response.status_code == 200:
        with open("temp_pokemon.png", "wb") as file:
            file.write(response.content)
        return pygame.image.load("temp_pokemon.png")
    return None

def display_pokemon_details(pokemon):
    screen.fill(WHITE)
    name_text = font.render(pokemon["name"].capitalize(), True, BLACK)
    screen.blit(name_text, (20, 20))
    
    image = load_pokemon_image(pokemon["image"]) if "image" in pokemon else None
    if image:
        screen.blit(pygame.transform.scale(image, (120, 120)), (20, 60))
    
    stats_text = font.render(f"HP: {pokemon['stats']['hp']} ATK: {pokemon['stats']['attack']}", True, BLACK)
    screen.blit(stats_text, (20, 200))
    
    pygame.display.flip()

running = True
pokemon_index = 0
while running:
    screen.fill(WHITE)
    current_pokemon = pokedex_data["pokemon"][pokemon_index]
    
    text = font.render(f"{pokemon_index + 1}. {current_pokemon['name'].capitalize()}", True, BLACK)
    screen.blit(text, (20, 20))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                pokemon_index = (pokemon_index + 1) % len(pokedex_data["pokemon"])
            elif event.key == pygame.K_LEFT:
                pokemon_index = (pokemon_index - 1) % len(pokedex_data["pokemon"])
            elif event.key == pygame.K_RETURN:
                display_pokemon_details(current_pokemon)
    
    pygame.display.flip()

pygame.quit()

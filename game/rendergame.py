import pygame
import requests
import io

# Initialisation de Pygame
pygame.init()

# Paramètres de la fenêtre
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Combat Pokémon")

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
BLUE = (0, 100, 255)
YELLOW = (255, 223, 0)

# Chargement de la police pixelisée
pygame.font.init()
font = pygame.font.Font(None, 24)  # Remplace "None" par le chemin d'une police pixelisée si tu en as une

# Fonction pour charger un sprite Pokémon
def load_pokemon_sprite(pokemon_id, scale=(128, 128)):
    url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{pokemon_id}.png"
    response = requests.get(url)
    if response.status_code == 200:
        image_data = io.BytesIO(response.content)
        image = pygame.image.load(image_data).convert_alpha()
        return pygame.transform.scale(image, scale)
    return pygame.Surface(scale)  # Surface vide si erreur

# Charger les Pokémon (Bulbizarre et Salamèche en exemple)
player_pokemon = load_pokemon_sprite(1)  # Bulbizarre
enemy_pokemon = load_pokemon_sprite(4)  # Salamèche

# Charger un fond de combat
battle_bg = pygame.image.load("fond.png")  # Ajoute une image de fond Pokémon

# Positions des Pokémon
player_pos = (100, 350)
enemy_pos = (500, 100)

# Boîtes d'interface
dialogue_box = pygame.Rect(50, 450, 700, 100)  # Zone de dialogue
menu_box = pygame.Rect(400, 450, 350, 100)  # Zone du menu d'attaques

# Attaques du Pokémon
attacks = ["Flamethrower", "Thunderbolt", "Ice Beam", "Solar Beam"]
selected_attack = 0  # Indice de l'attaque sélectionnée
confirming = False  # True si on est en train de confirmer l'attaque

# Boucle de jeu
running = True
while running:
    screen.fill(WHITE)
    
    # Affichage du fond de combat
    screen.blit(battle_bg, (0, 0))

    # Affichage des Pokémon
    screen.blit(player_pokemon, player_pos)
    screen.blit(enemy_pokemon, enemy_pos)

    # Dessiner la boîte de dialogue
    pygame.draw.rect(screen, WHITE, dialogue_box)
    pygame.draw.rect(screen, BLACK, dialogue_box, 3)

    # Texte dans la boîte de dialogue
    dialogue_text = font.render("Que doit faire Bulbizarre ?", True, BLACK)
    screen.blit(dialogue_text, (dialogue_box.x + 20, dialogue_box.y + 20))

    # Affichage des attaques si dans le menu
    if confirming:
        confirm_text = font.render("Confirmer ? (Entrée) / Annuler (Retour)", True, WHITE)
        screen.blit(confirm_text, (100, 560))
    else:
        # Dessiner la boîte du menu d'attaque
        pygame.draw.rect(screen, GRAY, menu_box)
        pygame.draw.rect(screen, BLACK, menu_box, 3)

        # Affichage des attaques
        for i, attack in enumerate(attacks):
            color = YELLOW if i == selected_attack else WHITE
            attack_text = font.render(attack, True, color)
            screen.blit(attack_text, (menu_box.x + 20, menu_box.y + 10 + i * 40))

    pygame.display.update()

    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN and not confirming:
                selected_attack = (selected_attack + 1) % len(attacks)
            elif event.key == pygame.K_UP and not confirming:
                selected_attack = (selected_attack - 1) % len(attacks)
            elif event.key == pygame.K_RETURN:
                if confirming:
                    print(f"{attacks[selected_attack]} utilisé !")  # Remplace par l'attaque réelle
                    confirming = False
                else:
                    confirming = True
            elif event.key == pygame.K_BACKSPACE:
                confirming = False

pygame.quit()

import pygame
import json
import os

# Initialisation de Pygame
pygame.init()

# Configuration de la fenêtre
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Menu.py")

# Charger et jouer la musique rétro Pokémon
pygame.mixer.init()
pygame.mixer.music.load("assets_menu/music/pokemon_theme.mp3")  # Remplace avec ton fichier audio
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)  # Joue en boucle

# Couleurs et polices
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
TRANSPARENT_GRAY = (50, 50, 50, 150)
FONT = pygame.font.Font(None, 36)
FONT_HOVER = pygame.font.Font(None, 48)  # Police agrandie pour effet hover

# Charger une image de fond
background = pygame.image.load("assets_menu/image/background.jpeg")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

def charger_partie():
    if os.path.exists("sauvegarde.json"):
        with open("sauvegarde.json", "r") as f:
            return json.load(f)
    return {"joueur": None, "pokemons": []}

def sauvegarder_partie(partie):
    with open("sauvegarde.json", "w") as f:
        json.dump(partie, f, indent=4)

def generer_menu_options():
    partie = charger_partie()
    options = []
    if partie["joueur"]:
        options.append("Continuer la partie")
    options.append("Nouvelle partie")
    options.append("Ajouter un Pokémon")
    options.append("Pokédex")
    options.append("Quitter le jeu")
    return options

def draw_text(text, x, y, font, color=WHITE):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def draw_menu(menu_options, selected_option):
    screen.blit(background, (0, 0))
    
    # Dessiner un rectangle semi-transparent pour le menu
    menu_surface = pygame.Surface((400, 300), pygame.SRCALPHA)
    menu_surface.fill(TRANSPARENT_GRAY)
    screen.blit(menu_surface, (200, 150))
    
    # Affichage des options du menu avec effet hover (zoom sur texte sélectionné)
    draw_text("Menu Pokémon", 320, 170, FONT)
    for i, option in enumerate(menu_options):
        color = WHITE if i != selected_option else (255, 255, 0)  # Jaune pour l'option sélectionnée
        font = FONT if i != selected_option else FONT_HOVER
        draw_text(f"{i+1}. {option}", 250, 220 + i * 50, font, color)

def main():
    selected_option = 0
    menu_options = generer_menu_options()
    running = True
    
    while running:
        screen.fill(BLACK)
        draw_menu(menu_options, selected_option)
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(menu_options)
                elif event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(menu_options)
                elif event.key == pygame.K_RETURN:
                    if menu_options[selected_option] == "Continuer la partie":
                        print("Chargement de la partie existante...")
                    elif menu_options[selected_option] == "Nouvelle partie":
                        partie = {"joueur": input("Entrez votre nom d'entraîneur : "), "pokemons": []}
                        sauvegarder_partie(partie)
                        menu_options = generer_menu_options()
                    elif menu_options[selected_option] == "Ajouter un Pokémon":
                        pokemon = input("Entrez le nom du Pokémon : ")
                        partie = charger_partie()
                        partie["pokemons"].append(pokemon)
                        sauvegarder_partie(partie)
                    elif menu_options[selected_option] == "Pokédex":
                        partie = charger_partie()
                        print("\n--- Votre Pokédex ---")
                        for i, pkm in enumerate(partie["pokemons"], 1):
                            print(f"{i}. {pkm}")
                    elif menu_options[selected_option] == "Quitter le jeu":
                        running = False
    
    pygame.quit()

if __name__ == "__main__":
    main()

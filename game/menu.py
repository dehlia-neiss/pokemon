import pygame

# Initialisation de Pygame
pygame.init()

# Configuration de la fenêtre
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Menu Pokémon")

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

# Police d'écriture
pygame.font.init()
FONT = pygame.font.Font(None, 50)

# Options du menu
menu_options = ["Continuer la partie", "Nouvelle partie", "Pokédex", "Quitter"]
selected_index = 0

def draw_menu():
    SCREEN.fill(WHITE)
    for i, option in enumerate(menu_options):
        color = YELLOW if i == selected_index else BLACK
        text = FONT.render(option, True, color)
        SCREEN.blit(text, (WIDTH // 3, 200 + i * 60))
    pygame.display.flip()

def main():
    global selected_index
    running = True
    
    while running:
        draw_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected_index = (selected_index + 1) % len(menu_options)
                elif event.key == pygame.K_UP:
                    selected_index = (selected_index - 1) % len(menu_options)
                elif event.key == pygame.K_RETURN:
                    if menu_options[selected_index] == "Quitter":
                        running = False
                    elif menu_options[selected_index] == "Nouvelle partie":
                        print("Lancement d'une nouvelle partie...")
                    elif menu_options[selected_index] == "Continuer la partie":
                        print("Chargement de la sauvegarde...")
                    elif menu_options[selected_index] == "Pokédex":
                        print("Affichage du Pokédex...")
    
    pygame.quit()

if __name__ == "__main__":
    main()


import pygame
import pygame_menu
import game
from enums.algorithm import Algorithm

# Constants
COLOR_BACKGROUND = (128, 128, 0)
FPS = 60.0
MENU_BACKGROUND_COLOR = (240, 230, 140)
MENU_TITLE_COLOR = (154, 205, 50)
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
WINDOW_SCALE = 0.75
pygame.display.init()
INFO = pygame.display.Info()
TILE_SIZE = int(INFO.current_h * 0.035)
WINDOW_SIZE = (13 * TILE_SIZE, 13 * TILE_SIZE)
surface = pygame.display.set_mode(WINDOW_SIZE)

# Global Variables
player_alg = Algorithm.PLAYER
en1_alg = Algorithm.ENEMY
en2_alg = Algorithm.ENEMY
en3_alg = Algorithm.ENEMY

def set_enemy_alg(index, algorithm):
    global en1_alg, en2_alg, en3_alg
    if index == 1:
        en1_alg = algorithm
    elif index == 2:
        en2_alg = algorithm
    elif index == 3:
        en3_alg = algorithm

def run_game():
    game.game_init(surface, en1_alg, en2_alg, en3_alg, TILE_SIZE)

def create_play_menu(theme):
    play_menu = pygame_menu.Menu(theme=theme, height=int(WINDOW_SIZE[1] * WINDOW_SCALE), width=int(WINDOW_SIZE[0] * WINDOW_SCALE), title='Play menu')
    play_menu.add.button('Start', run_game)
    play_menu.add.button('Options', create_options_menu(theme))
    return play_menu

def create_options_menu(theme):
    options_menu = pygame_menu.Menu(theme=theme, height=int(WINDOW_SIZE[1] * WINDOW_SCALE), width=int(WINDOW_SIZE[0] * WINDOW_SCALE), title='Options')
    options_menu.add.selector("Character 1", [("Player", Algorithm.PLAYER)])
    for i in range(1, 4):
        options_menu.add.selector(f"Character {i+1}", [("Enemy", Algorithm.ENEMY), ("None", Algorithm.NONE)], onchange=lambda _, alg: set_enemy_alg(i, alg))
    return options_menu

def create_main_menu(theme):
    main_menu = pygame_menu.Menu(theme=theme, height=int(WINDOW_SIZE[1] * WINDOW_SCALE), width=int(WINDOW_SIZE[0] * WINDOW_SCALE), onclose=pygame_menu.events.EXIT, title='Main menu')
    main_menu.add.button('Play', create_play_menu(theme))
    main_menu.add.button('Quit', pygame_menu.events.EXIT)
    return main_menu

def main_background():
    global surface
    surface.fill(COLOR_BACKGROUND)

def main():
    pygame.init()
    pygame.display.set_caption('Bomberman')
    clock = pygame.time.Clock()
    theme = pygame_menu.Theme(selection_color=COLOR_WHITE, widget_font=pygame_menu.font.FONT_BEBAS, title_font_size=TILE_SIZE, title_font_color=COLOR_BLACK, widget_font_color=COLOR_BLACK, widget_font_size=int(TILE_SIZE * 0.7), background_color=MENU_BACKGROUND_COLOR, title_background_color=MENU_TITLE_COLOR)
    main_menu = create_main_menu(theme)
    running = True

    while running:
        main_background()
        clock.tick(FPS)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        if main_menu.is_enabled():
            main_menu.mainloop(surface, main_background)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()


import pygame
from pygame.locals import *
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, RED, WHITE, BLUE
from checkers.game import Game
from minimax.algo import minimax
from minimax.algorithm import alpha_beta_minimax

# Constants
FPS = 60
BACKGROUND_COLOR = (139, 69, 19)  # Brown color for the wooden background
BUTTON_COLOR = (255, 223, 0)      # Gold color for buttons
BUTTON_HOVER_COLOR = (255, 255, 102)  # Lighter gold for hover effect
TEXT_COLOR = (0, 0, 0)            # Black color for text
SHADOW_COLOR = (100, 100, 100)    # Shadow color for buttons

pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Checkers")
BUTTON_FONT = pygame.font.SysFont("comicsans", 40)
TITLE_FONT = pygame.font.SysFont("comicsans", 50)
BUTTON_WIDTH, BUTTON_HEIGHT = 200, 80

# Load the background image
background_image = pygame.transform.scale(pygame.image.load('background.jpg'), (WIDTH, HEIGHT))

def get_row_col_from_mouse(pos):
    x, y = pos
    return y // SQUARE_SIZE, x // SQUARE_SIZE

def draw_text_center(text, font, color, surface, center, shadow=False):
    if shadow:
        shadow_color = (0, 0, 0)  # Black shadow
        shadow_offset = (3, 3)    # Offset for the shadow
        shadow_text = font.render(text, True, shadow_color)
        shadow_rect = shadow_text.get_rect(center=(center[0] + shadow_offset[0], center[1] + shadow_offset[1]))
        surface.blit(shadow_text, shadow_rect)
    
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect(center=center)
    surface.blit(textobj, textrect)

def draw_button(button_rect, text, hover):
    color = BUTTON_HOVER_COLOR if hover else BUTTON_COLOR
    pygame.draw.rect(WIN, SHADOW_COLOR, button_rect.inflate(10, 10), border_radius=10)
    pygame.draw.rect(WIN, color, button_rect, border_radius=10)
    draw_text_center(text, BUTTON_FONT, TEXT_COLOR, WIN, button_rect.center)

def draw_opening_screen():
    WIN.blit(background_image, (0, 0))  # Draw the background image
    

    # Draw start button
    start_button_rect = pygame.Rect(WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT - BUTTON_HEIGHT - 50, BUTTON_WIDTH, BUTTON_HEIGHT)
    draw_button(start_button_rect, 'Start', False)

    pygame.display.update()
    return start_button_rect

def draw_difficulty_screen():
    WIN.fill(BACKGROUND_COLOR)
    draw_text_center('DIFFICULTY LEVEL', TITLE_FONT, TEXT_COLOR, WIN, (WIDTH // 2, HEIGHT // 4))

    # Draw difficulty level buttons
    buttons = []
    for i, text in enumerate(['Easy', 'Medium', 'Hard']):
        button_rect = pygame.Rect(WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT // 2 + i * (BUTTON_HEIGHT + 20), BUTTON_WIDTH, BUTTON_HEIGHT)
        buttons.append((button_rect, text))
        draw_button(button_rect, text, False)

    pygame.display.update()
    return buttons

def main():
    run = True
    clock = pygame.time.Clock()
    opening_screen = True
    difficulty_selected = False
    buttons = []

    while run:
        clock.tick(FPS)

        if opening_screen:
            button_rect = draw_opening_screen()
        else:
            if not buttons:
                buttons = draw_difficulty_screen()

        for event in pygame.event.get():
            if event.type == QUIT:
                run = False
            elif event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if opening_screen and button_rect.collidepoint(pos):
                    opening_screen = False
                elif not opening_screen:
                    for button_rect, text in buttons:
                        if button_rect.collidepoint(pos):
                            difficulty_selected = True
                            if text == 'Easy':
                                print("Easy mode selected")
                                game_loop('Easy')
                                opening_screen = True  # Reset to opening screen for next game
                            elif text == 'Medium':
                                print("Medium mode selected")
                                game_loop('Medium')
                                opening_screen = True  # Reset to opening screen for next game
                            elif text == 'Hard':
                                print("Hard mode selected")
                                game_loop('Hard')
                                opening_screen = True  # Reset to opening screen for next game

        if not opening_screen:
            for button_rect, text in buttons:
                hover = button_rect.collidepoint(pygame.mouse.get_pos())
                draw_button(button_rect, text, hover)

        pygame.display.update()

    pygame.quit()

def game_loop(difficulty):
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)

    while run:
        clock.tick(FPS)
        
        if game.turn == WHITE:

            print("AI's Turn")
            if difficulty == 'Easy':
                print("using minimax")
                value, new_board = minimax(game.get_board(), 2, True, game)
                game.ai_move(new_board) 
            elif difficulty == 'Medium':
                print("using alpha beta pruning")
                value, new_board = alpha_beta_minimax(game.get_board(), 3, float('-inf'), float('inf'), True, game)
                game.ai_move(new_board) 
            else:
                print("using fuzzy")
                game.ai_fuzzy_move()
           
           
        if game.winner() is not None:
            print(game.winner())
            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False  # Exit the game loop
                main()  # Return to main screen after game ends

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                print(f"Mouse clicked at ({row}, {col})")
                game.select(row, col)
                if game.winner() is not None:
                    pygame.time.delay(1000)  # Delay before resetting
                    game.restart()
                    return

        game.update()
        game.draw_valid_moves(game.valid_moves)

    main()  # Return to main screen after game ends

main()

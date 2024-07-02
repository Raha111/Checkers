import pygame
from pygame.locals import *
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, RED, WHITE, BLUE
from checkers.game import Game
from minimax.algo import minimax
from minimax.algorithm import alpha_beta_minimax
from minimax.genetic_algorithm import genetic_algorithm, get_optimized_evaluation_function
from minimax.ga_minimax import GA_minimax
from PIL import Image
import imageio
import numpy as np

# Constants
FPS = 60
BACKGROUND_COLOR = (139, 69, 19)
BACKGROUND_COLORR = (255, 255, 255)
BUTTON_COLOR = (255, 223, 0)
BUTTON_HOVER_COLOR = (255, 255, 102)
TEXT_COLOR = (0, 0, 0)
SHADOW_COLOR = (100, 100, 100)

pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Checkers")
BUTTON_FONT = pygame.font.SysFont("comicsans", 40)
TITLE_FONT = pygame.font.SysFont("comicsans", 50)
BUTTON_WIDTH, BUTTON_HEIGHT = 200, 80

background_image = pygame.transform.scale(pygame.image.load('background.jpg'), (WIDTH, HEIGHT))

def get_row_col_from_mouse(pos):
    x, y = pos
    return y // SQUARE_SIZE, x // SQUARE_SIZE

def draw_text_center(text, font, color, surface, center, shadow=False):
    if shadow:
        shadow_color = (0, 0, 0)
        shadow_offset = (3, 3)
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
    WIN.blit(background_image, (0, 0))
    start_button_rect = pygame.Rect(WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT - BUTTON_HEIGHT - 50, BUTTON_WIDTH, BUTTON_HEIGHT)
    draw_button(start_button_rect, 'Start', False)
    pygame.display.update()
    return start_button_rect

def draw_difficulty_screen():
    WIN.fill(BACKGROUND_COLOR)
    draw_text_center('DIFFICULTY LEVEL', TITLE_FONT, TEXT_COLOR, WIN, (WIDTH // 2, HEIGHT // 4))
    buttons = []
    for i, text in enumerate(['Easy', 'Medium', 'Hard', 'Very Hard']):
        button_rect = pygame.Rect(WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT // 2 + i * (BUTTON_HEIGHT + 20), BUTTON_WIDTH, BUTTON_HEIGHT)
        buttons.append((button_rect, text))
        draw_button(button_rect, text, False)
    how_to_play_button_rect = pygame.Rect(WIDTH - 230, HEIGHT - 100, 200, 60)
    draw_button(how_to_play_button_rect, 'How to Play', False)
    pygame.display.update()
    return buttons, how_to_play_button_rect



def draw_instructions_screen():
    WIN.fill(BACKGROUND_COLOR)
    instructions_text = [
        "How to Play Checkers:",
        "1. Move your pieces diagonally forward to",
        "   an adjacent empty square.",
        "2. Capture opponent's pieces by jumping",
        "   over them.",
        "3. Reach the opponent's back row to",
        "   crown your piece and gain King's powers."
    ]
    text_start_y = HEIGHT // 4
    for i, line in enumerate(instructions_text):
        draw_text_center(line, BUTTON_FONT, TEXT_COLOR, WIN, (WIDTH // 2, text_start_y + i * 40))
    
    close_button_rect = pygame.Rect(WIDTH - 60, 20, 40, 40)
    pygame.draw.rect(WIN, BUTTON_COLOR, close_button_rect)
    draw_text_center('X', BUTTON_FONT, TEXT_COLOR, WIN, close_button_rect.center)
    pygame.display.update()
    return close_button_rect

def load_gif(filename):
    gif = imageio.get_reader(filename)
    return [np.array(frame) for frame in gif]

def resize_gif_frames(gif_frames, new_size=(WIDTH, HEIGHT)):
    return [pygame.image.fromstring(Image.fromarray(frame).resize(new_size, resample=Image.BILINEAR).tobytes(), new_size, 'RGB') for frame in gif_frames]

def draw_winner_screen(winner, gif_filename):
    WIN.fill(BACKGROUND_COLORR)
    winner_text = "You lose!!!" if winner == "WHITE" else "You win!!!" if winner == "RED" else "Unknown"

    gif_frames = resize_gif_frames(load_gif(gif_filename), (WIDTH, HEIGHT))
    frame_index, num_frames, clock, running = 0, len(gif_frames), pygame.time.Clock(), True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if how_to_play_button_rect.collidepoint(pos):
                    draw_instructions_screen()

        WIN.blit(gif_frames[frame_index], (0, HEIGHT // 50))
        draw_text_center(winner_text, TITLE_FONT, TEXT_COLOR, WIN, (WIDTH // 2, HEIGHT // 10), shadow=True)
        pygame.display.flip()
        frame_index = (frame_index + 1) % num_frames
        clock.tick(FPS)

    pygame.quit()

def main():
    run, clock, screen_state, buttons, how_to_play_button_rect = True, pygame.time.Clock(), 'opening', [], None

    while run:
        clock.tick(FPS)
        if screen_state == 'opening':
            button_rect = draw_opening_screen()
        elif screen_state == 'difficulty':
            buttons, how_to_play_button_rect = draw_difficulty_screen()
            screen_state = 'difficulty_screen'
        elif screen_state == 'instructions':
            close_button_rect = draw_instructions_screen()

        for event in pygame.event.get():
            if event.type == QUIT:
                run = False
            elif event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if screen_state == 'opening' and button_rect.collidepoint(pos):
                    screen_state = 'difficulty'
                elif screen_state == 'difficulty_screen':
                    for button_rect, text in buttons:
                        if button_rect.collidepoint(pos):
                            game_loop(text)
                            screen_state = 'difficulty'
                    if how_to_play_button_rect.collidepoint(pos):
                        screen_state = 'instructions'
                elif screen_state == 'instructions' and close_button_rect.collidepoint(pos):
                    screen_state = 'difficulty'

        if screen_state == 'difficulty_screen':
            for button_rect, text in buttons:
                draw_button(button_rect, text, button_rect.collidepoint(pygame.mouse.get_pos()))

        pygame.display.update()

    pygame.quit()

def game_loop(difficulty):
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)

    optimized_params = genetic_algorithm()  # Optimize evaluation function parameters
    optimized_evaluation_function = get_optimized_evaluation_function(optimized_params)

    while run:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if game.turn == RED:  # Player's turn
                    pos = pygame.mouse.get_pos()
                    row, col = get_row_col_from_mouse(pos)
                    print(f"Mouse clicked at ({row}, {col})")
                    game.select(row, col)
                    if game.winner() is not None:
                        draw_winner_screen(game.winner())
                        pygame.time.delay(2000)
                        game.reset()  # Reset the game after displaying winner
                        continue  # Continue to next iteration of the loop

        if game.turn == WHITE and game.winner() is None:
            print("AI's Turn")
            if difficulty == 'Easy':
                print("using minimax")
                value, new_board = minimax(game.get_board(), 2, True, game)
                game.ai_move(new_board)
            elif difficulty == 'Medium':
                print("using alpha beta pruning")
                value, new_board = alpha_beta_minimax(game.get_board(), 3, float('-inf'), float('inf'), True, game)
                game.ai_move(new_board)
            elif difficulty == 'Hard':
                print("using fuzzy")
                game.ai_fuzzy_move()
            elif difficulty == 'Very Hard':
                print("using hybrid genetic and minimax algorithm")
                value, new_board = GA_minimax(game.get_board(), 4, True, float('-inf'), float('inf'), game, optimized_evaluation_function)
                game.ai_move(new_board)
                
        if game.winner():
            draw_winner_screen(game.winner(), "winner.gif")
            run = False
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                main()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                row, col = get_row_col_from_mouse(pygame.mouse.get_pos())
                game.select(row, col)
                if game.winner():
                    draw_winner_screen(game.winner(), "winner.gif")
                    pygame.time.delay(10000)
                    game.reset()
                    return    

        game.update()  # Update the game state and display
        game.draw_valid_moves(game.valid_moves)
        pygame.display.update()  # Update the display

    main()

if __name__ == "__main__":
    main()

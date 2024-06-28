import pygame
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE,RED
from checkers.game import Game
from minimax.algo import minimax
from minimax.algorithm import alpha_beta_minimax
from checkers.constants import RED, WHITE, BLUE, SQUARE_SIZE

FPS = 60
pygame.init()

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Checkers")

def get_row_col_from_mouse(pos):
    x,y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row,col


def main():
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)

    while run:
        clock.tick(FPS)
        '''
        if game.turn == WHITE:
            #value, new_board = minimax(game.get_board(), 4, WHITE, game)#depth=4 higher depth->better ai but longer to run
            value, new_board = alpha_beta_minimax(game.get_board(), 4, float('-inf'), float('inf'), True, game)
            game.ai_move(new_board)   
            
        '''
        if game.winner() != None:
            print(game.winner())
            run = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                print(f"Mouse clicked at ({row}, {col})")
                game.select(row,col)

        game.update()

        game.draw_valid_moves(game.valid_moves)
    
    pygame.quit()

main()
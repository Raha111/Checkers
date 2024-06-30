# fuzzy_ai.py
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
from checkers.board import Board

RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREY = (128, 128, 128)

# Fuzzy variables
piece_type = ctrl.Antecedent(np.arange(0, 11, 1), 'piece_type')
piece_position = ctrl.Antecedent(np.arange(0, 11, 1), 'piece_position')
board_evaluation = ctrl.Antecedent(np.arange(0, 11, 1), 'board_evaluation')
move_strength = ctrl.Consequent(np.arange(0, 11, 1), 'move_strength')

# Define membership functions
piece_type['soldier'] = fuzz.trimf(piece_type.universe, [0, 3, 6])
piece_type['queen'] = fuzz.trimf(piece_type.universe, [4, 6, 8])
piece_type['king'] = fuzz.trimf(piece_type.universe, [7, 9, 10])

piece_position['front'] = fuzz.trimf(piece_position.universe, [0, 3, 6])
piece_position['middle'] = fuzz.trimf(piece_position.universe, [4, 6, 8])
piece_position['back'] = fuzz.trimf(piece_position.universe, [7, 9, 10])

board_evaluation['weak'] = fuzz.trimf(board_evaluation.universe, [0, 3, 6])
board_evaluation['strong'] = fuzz.trimf(board_evaluation.universe, [4, 6, 10])

move_strength['weak'] = fuzz.trimf(move_strength.universe, [0, 3, 6])
move_strength['strong'] = fuzz.trimf(move_strength.universe, [4, 6, 10])

# Define fuzzy rules
rule1 = ctrl.Rule(piece_type['king'] & board_evaluation['strong'], move_strength['weak'])
rule2 = ctrl.Rule(piece_type['soldier'] & piece_position['front'], move_strength['strong'])
rule3 = ctrl.Rule(piece_type['queen'] & board_evaluation['weak'], move_strength['strong'])

# Create fuzzy control system
move_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
move_simulation = ctrl.ControlSystemSimulation(move_ctrl)

# Function to calculate fuzzy move strength
def calculate_fuzzy_move(board, row, col):
    piece = board.get_piece(row, col)
    if piece:
        piece_type_value = 7 if piece.type == 'king' else (4 if piece.type == 'queen' else 1)  # Example piece type values
        piece_position_value = 5  # Example piece position value calculation
        board_evaluation_value = board.evaluate_board()  # Example board evaluation (to be implemented in Board class)
        
        # Set inputs to fuzzy simulation
        move_simulation.input['piece_type'] = piece_type_value
        move_simulation.input['piece_position'] = piece_position_value
        move_simulation.input['board_evaluation'] = board_evaluation_value
        
        # Compute fuzzy output
        move_simulation.compute()
        
        # Return defuzzified move strength
        return move_simulation.output['move_strength']
    return 0

# Function to determine best move using fuzzy logic
def determine_best_fuzzy_move(board):
    best_move = None
    best_strength = -1
    
    for row in range(len(board)):
        for col in range(len(board[row])):
            piece = board[row][col]
            if piece is not None and piece.color == WHITE:  # Assuming AI controls WHITE pieces
                strength = calculate_fuzzy_move(board, row, col)
                if strength > best_strength:
                    best_strength = strength
                    best_move = (row, col)
    
    return best_move

# Example usage:
if __name__ == '__main__':
    # Example board and piece coordinates
    board = Board()
    best_move = determine_best_fuzzy_move(board)
    print(f"Best fuzzy move: {best_move}")

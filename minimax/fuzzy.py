import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
from checkers.board import Board  # Assuming Board class from your game implementation

# Constants for colors
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREY = (128, 128, 128)
ROWS, COLS = 9, 9  # Example board size, adjust as per your game

# Fuzzy variables
piece_value = ctrl.Antecedent(np.arange(0, 11, 1), 'piece_value')
mobility = ctrl.Antecedent(np.arange(0, 11, 1), 'mobility')
threat_level = ctrl.Antecedent(np.arange(0, 11, 1), 'threat_level')
control_key_areas = ctrl.Antecedent(np.arange(0, 11, 1), 'control_key_areas')
game_phase = ctrl.Antecedent(np.arange(0, 11, 1), 'game_phase')
aggressiveness = ctrl.Antecedent(np.arange(0, 11, 1), 'aggressiveness')
piece_support = ctrl.Antecedent(np.arange(0, 11, 1), 'piece_support')
move_direction = ctrl.Antecedent(np.arange(0, 11, 1), 'move_direction')
move_strength = ctrl.Consequent(np.arange(0, 101, 1), 'move_strength')

# Define membership functions with sufficient overlap
piece_value['very_low'] = fuzz.trimf(piece_value.universe, [0, 1, 3])
piece_value['low'] = fuzz.trimf(piece_value.universe, [2, 4, 6])
piece_value['medium'] = fuzz.trimf(piece_value.universe, [5, 7, 9])
piece_value['high'] = fuzz.trimf(piece_value.universe, [8, 10, 10])
piece_value['very_high'] = fuzz.trimf(piece_value.universe, [9, 10, 10])

mobility['very_low'] = fuzz.trimf(mobility.universe, [0, 1, 3])
mobility['low'] = fuzz.trimf(mobility.universe, [2, 4, 6])
mobility['medium'] = fuzz.trimf(mobility.universe, [5, 7, 9])
mobility['high'] = fuzz.trimf(mobility.universe, [8, 10, 10])
mobility['very_high'] = fuzz.trimf(mobility.universe, [9, 10, 10])

threat_level['very_low'] = fuzz.trimf(threat_level.universe, [0, 1, 3])
threat_level['low'] = fuzz.trimf(threat_level.universe, [2, 4, 6])
threat_level['medium'] = fuzz.trimf(threat_level.universe, [5, 7, 9])
threat_level['high'] = fuzz.trimf(threat_level.universe, [8, 10, 10])
threat_level['very_high'] = fuzz.trimf(threat_level.universe, [9, 10, 10])

control_key_areas['very_low'] = fuzz.trimf(control_key_areas.universe, [0, 1, 3])
control_key_areas['low'] = fuzz.trimf(control_key_areas.universe, [2, 4, 6])
control_key_areas['medium'] = fuzz.trimf(control_key_areas.universe, [5, 7, 9])
control_key_areas['high'] = fuzz.trimf(control_key_areas.universe, [8, 10, 10])
control_key_areas['very_high'] = fuzz.trimf(control_key_areas.universe, [9, 10, 10])

game_phase['very_early'] = fuzz.trimf(game_phase.universe, [0, 1, 3])
game_phase['early'] = fuzz.trimf(game_phase.universe, [2, 4, 6])
game_phase['midgame'] = fuzz.trimf(game_phase.universe, [5, 7, 9])
game_phase['late'] = fuzz.trimf(game_phase.universe, [8, 10, 10])
game_phase['endgame'] = fuzz.trimf(game_phase.universe, [9, 10, 10])

aggressiveness['very_low'] = fuzz.trimf(aggressiveness.universe, [0, 1, 3])
aggressiveness['low'] = fuzz.trimf(aggressiveness.universe, [2, 4, 6])
aggressiveness['medium'] = fuzz.trimf(aggressiveness.universe, [5, 7, 9])
aggressiveness['high'] = fuzz.trimf(aggressiveness.universe, [8, 10, 10])
aggressiveness['very_high'] = fuzz.trimf(aggressiveness.universe, [9, 10, 10])

piece_support['very_low'] = fuzz.trimf(piece_support.universe, [0, 1, 3])
piece_support['low'] = fuzz.trimf(piece_support.universe, [2, 4, 6])
piece_support['medium'] = fuzz.trimf(piece_support.universe, [5, 7, 9])
piece_support['high'] = fuzz.trimf(piece_support.universe, [8, 10, 10])
piece_support['very_high'] = fuzz.trimf(piece_support.universe, [9, 10, 10])

move_direction['east'] = fuzz.trimf(move_direction.universe, [0, 1, 3])
move_direction['north'] = fuzz.trimf(move_direction.universe, [2, 4, 6])
move_direction['south'] = fuzz.trimf(move_direction.universe, [5, 7, 9])
move_direction['west'] = fuzz.trimf(move_direction.universe, [8, 10, 10])

move_strength['very_weak'] = fuzz.trimf(move_strength.universe, [0, 15, 30])
move_strength['weak'] = fuzz.trimf(move_strength.universe, [20, 35, 50])
move_strength['medium'] = fuzz.trimf(move_strength.universe, [45, 60, 75])
move_strength['strong'] = fuzz.trimf(move_strength.universe, [70, 85, 100])
move_strength['very_strong'] = fuzz.trimf(move_strength.universe, [90, 100, 100])

# Define aggressive fuzzy rules
rule1 = ctrl.Rule(aggressiveness['very_high'] & piece_value['high'], move_strength['very_strong'])
rule2 = ctrl.Rule(threat_level['high'] & aggressiveness['medium'], move_strength['strong'])
rule3 = ctrl.Rule(aggressiveness['high'] & control_key_areas['high'], move_strength['strong'])
rule4 = ctrl.Rule(game_phase['endgame'] & piece_value['high'], move_strength['strong'])
rule5 = ctrl.Rule(threat_level['very_high'] & mobility['high'], move_strength['very_strong'])
rule6 = ctrl.Rule(aggressiveness['very_high'] & game_phase['midgame'], move_strength['very_strong'])
rule7 = ctrl.Rule(piece_support['very_high'] & control_key_areas['high'], move_strength['very_strong'])
rule8 = ctrl.Rule(aggressiveness['high'] & mobility['high'], move_strength['strong'])
rule9 = ctrl.Rule(game_phase['endgame'] & control_key_areas['very_high'], move_strength['strong'])
rule10 = ctrl.Rule(aggressiveness['very_high'] & piece_value['medium'], move_strength['very_strong'])

# Create fuzzy control system
move_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10])
move_simulation = ctrl.ControlSystemSimulation(move_ctrl)

# Function to calculate fuzzy move strength
def calculate_fuzzy_move(board, row, col):
    piece = board.get_piece(row, col)
    if piece and piece.color == WHITE:  # Assuming AI controls WHITE pieces
        # Example piece value calculations
        piece_value_value = 7 if piece.type == 'king' else (4 if piece.type == 'queen' else 1)
        # Example mobility, threat level, control key areas, game phase, aggressiveness, piece support values
        mobility_value = 5
        threat_level_value = 3
        control_key_areas_value = 5
        game_phase_value = 5
        aggressiveness_value = 6
        piece_support_value = 4
        
        # Set inputs to fuzzy simulation
        move_simulation.input['piece_value'] = piece_value_value
        move_simulation.input['mobility'] = mobility_value
        move_simulation.input['threat_level'] = threat_level_value
        move_simulation.input['control_key_areas'] = control_key_areas_value
        move_simulation.input['game_phase'] = game_phase_value
        move_simulation.input['aggressiveness'] = aggressiveness_value
        move_simulation.input['piece_support'] = piece_support_value
        
        # Compute fuzzy output
        try:
            move_simulation.compute()
            move_strength = move_simulation.output['move_strength']
        except ValueError as e:
            print(f"Error in fuzzy computation: {e}")
            move_strength = 0  # Assign a default value or handle the error appropriately

        return move_strength
    return 0

# Function to determine best move using fuzzy logic
def determine_best_fuzzy_move(board):
    best_move = None
    best_strength = -1
    
    for row in range(ROWS):
        for col in range(COLS):
            piece = board.get_piece(row, col)
            if piece and piece.color == WHITE:  # Assuming AI controls WHITE pieces
                strength = calculate_fuzzy_move(board, row, col)
                if strength > best_strength:
                    best_strength = strength
                    best_move = (row, col)
    
    return best_move

# Example usage
if __name__ == '__main__':
    # Example board and piece coordinates
    board = Board()  # Instantiate your Board class with initial setup
    # Assuming your Board class has methods like get_piece, evaluate, etc.
    
    # Determine the best move using fuzzy logic
    best_move = determine_best_fuzzy_move(board)
    print(f"Best fuzzy move: {best_move}")
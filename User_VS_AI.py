import numpy as np
import pygame
import sys
import math
import random

ROW_COUNT = 6
COLUMN_COUNT = 7

GREY = (117, 108, 108)
WHITE = (255, 255, 255)
PINK = (255, 153, 204)
BLUE = (0, 153, 153)
BLACK = (0, 0, 0)

PLAYER_TURN = 0
AI_TURN = 1

EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2

WINDOW_LENGTH = 4

# Define the Evolutionary Algorithm parameters
POPULATION_SIZE = 10
GENERATIONS = 5
MUTATION_RATE = 0.1

# Create a class to represent an individual in the population
class Individual:
    def __init__(self, col):
        self.col = col
        self.fitness = 0

# Evaluate the fitness of an individual
def evaluate_individual(individual, board, piece):
    temp_board = board.copy()
    if is_valid_location(temp_board, individual.col):
        row = get_next_open_row(temp_board, individual.col)
        drop_piece(temp_board, row, individual.col, piece)
        individual.fitness = score_position(temp_board, piece)

# Create the initial population
def create_population():
    population = []
    for _ in range(POPULATION_SIZE):
        individual = Individual(random.choice(location_valid_gets(board)))
        population.append(individual)
    return population

# Select the fittest individuals for reproduction
def selection(population):
    population.sort(key=lambda x: x.fitness, reverse=True)
    return population[:POPULATION_SIZE // 2]

# Generate a new individual by crossing over two parents
def crossover(parent1, parent2):
    if random.random() < 0.5:
        return Individual(parent1.col)
    else:
        return Individual(parent2.col)

# Mutate an individual with a chance of MUTATION_RATE
def mutate(individual):
    if random.random() < MUTATION_RATE:
        individual.col = random.choice(location_valid_gets(board))

# Create a new generation
def create_new_generation(population):
    new_population = []
    fittest_individuals = selection(population)
    for _ in range(POPULATION_SIZE):
        parent1 = random.choice(fittest_individuals)
        parent2 = random.choice(fittest_individuals)
        child = crossover(parent1, parent2)
        mutate(child)
        new_population.append(child)
    return new_population

# Evolutionary Algorithm
def evolutionary_algorithm(board, piece):
    population = create_population()
    for individual in population:
        evaluate_individual(individual, board, piece)

    for _ in range(GENERATIONS):
        population = create_new_generation(population)
        for individual in population:
            evaluate_individual(individual, board, piece)

    best_individual = max(population, key=lambda x: x.fitness)
    return best_individual.col


def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == EMPTY

def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == EMPTY:
            return r

def print_board(board):
    print(np.flip(board, 0))

def winning_move(board, piece):
    # Check horizontal for win
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if (
                board[r][c] == piece
                and board[r][c + 1] == piece
                and board[r][c + 2] == piece
                and board[r][c + 3] == piece
            ):
                return True

    # Check vertical for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if (
                board[r][c] == piece
                and board[r + 1][c] == piece
                and board[r + 2][c] == piece
                and board[r + 3][c] == piece
            ):
                return True

    # Check positive diagonal
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if (
                board[r][c] == piece
                and board[r + 1][c + 1] == piece
                and board[r + 2][c + 2] == piece
                and board[r + 3][c + 3] == piece
            ):
                return True

    # Check negative diagonal
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if (
                board[r][c] == piece
                and board[r - 1][c + 1] == piece
                and board[r - 2][c + 2] == piece
                and board[r - 3][c + 3] == piece
            ):
                return True

    return False

# AI
def evaluate_window(window, piece):
    score = 0
    opp_piece = PLAYER_PIECE
    if piece == PLAYER_PIECE:
        opp_piece = AI_PIECE

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 2

    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 4

    return score

def score_position(board, piece):
    score = 0

    # Score center column
    center_array = [int(i) for i in list(board[:, COLUMN_COUNT // 2])]
    center_count = center_array.count(piece)
    score += center_count * 3

    # Score Horizontal
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(COLUMN_COUNT - 3):
            window = row_array[c:c + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # Score Vertical
    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(ROW_COUNT - 3):
            window = col_array[r:r + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # Score positive sloped diagonal
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r + i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    # Score negative sloped diagonal
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r + 3 - i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    return score

def is_terminal_node(board):
    return (
        winning_move(board, PLAYER_PIECE)
        or winning_move(board, AI_PIECE)
        or len(location_valid_gets(board)) == 0
    )

# Alpha-beta pruning
def minimax(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = location_valid_gets(board)
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI_PIECE):
                return (None, 100000000000000)
            elif winning_move(board, PLAYER_PIECE):
                return (None, -10000000000000)
            else:  # Game is over, no more valid moves
                return (None, 0)
        else:  # Depth is zero
            return (None, score_position(board, AI_PIECE))
    if maximizingPlayer:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AI_PIECE)
            new_score = minimax(b_copy, depth - 1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value

    else:  # Minimizing player
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, PLAYER_PIECE)
            new_score = minimax(b_copy, depth - 1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value

def location_valid_gets(board):
    valid_locations = []
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations

def pick_best_move(board, piece):
    valid_locations = location_valid_gets(board)
    best_score = -10000
    best_col = random.choice(valid_locations)
    for col in valid_locations:
        row = get_next_open_row(board, col)
        temp_board = board.copy()
        drop_piece(temp_board, row, col, piece)
        score = score_position(temp_board, piece)
        if score > best_score:
            best_score = score
            best_col = col

    return best_col

def is_board_filled(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == EMPTY:
                return False
    return True

def draw_board(board):
    background = pygame.image.load("C:/Users/zuhai/Desktop/Final Project/Woodentexture.jpg")
    background = pygame.transform.scale(background, (width, height))
    screen.blit(background, (0, 100))
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.circle(screen, WHITE, (c * SQUARESIZE + SQUARESIZE // 2, r * SQUARESIZE + SQUARESIZE + SQUARESIZE // 2), RADIUS)
            pygame.draw.circle(screen, BLACK, (c * SQUARESIZE + SQUARESIZE // 2, r * SQUARESIZE + SQUARESIZE + SQUARESIZE // 2), RADIUS, 1)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == PLAYER_PIECE:
                pygame.draw.circle(screen, PINK, (c * SQUARESIZE + SQUARESIZE // 2, height - r * SQUARESIZE - SQUARESIZE // 2), RADIUS)
                pygame.draw.circle(screen, BLACK, (c * SQUARESIZE + SQUARESIZE // 2, height - r * SQUARESIZE - SQUARESIZE // 2), RADIUS, 1)
            elif board[r][c] == AI_PIECE:
                pygame.draw.circle(screen, BLUE, (c * SQUARESIZE + SQUARESIZE // 2, height - r * SQUARESIZE - SQUARESIZE // 2), RADIUS)
                pygame.draw.circle(screen, BLACK, (c * SQUARESIZE + SQUARESIZE // 2, height - r * SQUARESIZE - SQUARESIZE // 2), RADIUS, 1)

    pygame.display.update()

board = create_board()
print_board(board)
game_over = False

# -----------------GUI---------------------
pygame.init()

SQUARESIZE = 100
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE

size = (width, height)
RADIUS = int(SQUARESIZE / 2 - 5)
screen = pygame.display.set_mode(size)
myfont = pygame.font.SysFont("opensans", 75)
pygame.display.update()
algorithm_choice = input("Welcome! Please choose the algorithm: (1) Minimax with Alpha-Beta Pruning, (2) Evolutionary Algorithm: ")

if algorithm_choice == '1':
    depth = int(input("Please enter the depth for the Minimax algorithm 1-Easy, 2- Medium, 3- Hard, 4-Semi Pro, 5-Impossible: "))
    algorithm_name = "Minimax with Alpha-Beta Pruning (Depth: {})".format(depth)
else:
    algorithm_name = "Evolutionary Algorithm"

turns = random.randint(PLAYER_TURN, AI_TURN)

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            posx = event.pos[0]
            if turns == PLAYER_TURN:
                pygame.draw.circle(screen, PINK, (posx, int(SQUARESIZE / 2)), RADIUS)

        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))

            # Player 1 Input
            if turns == PLAYER_TURN:
                posx = event.pos[0]
                col = int(math.floor(posx / SQUARESIZE))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, PLAYER_PIECE)

                    if winning_move(board, PLAYER_PIECE):
                        label = myfont.render("You won!", 1, PINK)
                        screen.blit(label, (230, 30))
                        game_over = True
                    elif is_board_filled(board):
                        label = myfont.render("Game is drawn", 1, WHITE)
                        screen.blit(label, (230, 30))
                        game_over = True
                        

                    print_board(board)
                    draw_board(board)

                    turns += 1
                    turns = turns % 2

    # AI Input
    if turns == AI_TURN and not game_over:
        if algorithm_choice == '1':
            # Minimax with alpha-beta pruning
            col, minimax_score = minimax(board, depth, -math.inf, math.inf, True)
        else:
            # Evolutionary algorithm
            col = evolutionary_algorithm(board, AI_PIECE)

        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, AI_PIECE)

            if winning_move(board, AI_PIECE):
                label = myfont.render("AI wins", 1, BLUE)
                screen.blit(label, (40, 10))
                game_over = True
            elif is_board_filled(board):
                    label = myfont.render("Game is drawn", 1, WHITE)
                    screen.blit(label, (230, 30))
                    game_over = True
                    
            print_board(board)
            draw_board(board)

            turns += 1
            turns = turns % 2

    if game_over:
        pygame.time.wait(3000)

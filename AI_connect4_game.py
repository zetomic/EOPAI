import numpy as np
import random
import pygame
import sys
import math

GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

total_rows = 6
total_columns = 7

PLAYER_TURN = 0
AI_TURN = 1

emt = 0
piece_drop_player = 1
piece_drop_ai = 2

WINDOW_LENGTH = 4


def BOARD_CREATE():
    game_board = np.zeros((total_rows, total_columns))
    return game_board


def piece_drop(game_board, row, col, piece):
    game_board[row][col] = piece


def valid_is_location(game_board, col):
    return game_board[total_rows - 1][col] == 0


def get_next_open_row(game_board, col):
    for r in range(total_rows):
        if game_board[r][col] == 0:
            return r


def board_print(game_board):
    print(np.flip(game_board, 0))


def winning_move(game_board, piece):
    # horizontal locations to win
    for c in range(total_columns - 3):
        for r in range(total_rows):
            if game_board[r][c] == piece and game_board[r][c + 1] == piece and game_board[r][c + 2] == piece and game_board[r][
                c + 3] == piece:
                return True

    # vertical locations to win
    for c in range(total_columns):
        for r in range(total_rows - 3):
            if game_board[r][c] == piece and game_board[r + 1][c] == piece and game_board[r + 2][c] == piece and game_board[r + 3][
                c] == piece:
                return True

    #  positive diaganols to win
    for c in range(total_columns - 3):
        for r in range(total_rows - 3):
            if game_board[r][c] == piece and game_board[r + 1][c + 1] == piece and game_board[r + 2][c + 2] == piece and game_board[r + 3][
                c + 3] == piece:
                return True

    #  negative diaganols to win
    for c in range(total_columns - 3):
        for r in range(3, total_rows):
            if game_board[r][c] == piece and game_board[r - 1][c + 1] == piece and game_board[r - 2][c + 2] == piece and game_board[r - 3][
                c + 3] == piece:
                return True

#AI
def evaluate_window(window, piece):
    score = 0
    opp_piece = piece_drop_player
    if piece == piece_drop_player:
        opp_piece = piece_drop_ai

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(emt) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(emt) == 2:
        score += 2

    if window.count(opp_piece) == 3 and window.count(emt) == 1:
        score -= 4

    return score


def score_position(game_board, piece):
    score = 0

    ## Score center column
    center_array = [int(i) for i in list(game_board[:, total_columns // 2])]
    center_count = center_array.count(piece)
    score += center_count * 3

    ## Score Horizontal
    for r in range(total_rows):
        row_array = [int(i) for i in list(game_board[r, :])]
        for c in range(total_columns - 3):
            window = row_array[c:c + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    ## Score Vertical
    for c in range(total_columns):
        col_array = [int(i) for i in list(game_board[:, c])]
        for r in range(total_rows - 3):
            window = col_array[r:r + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    ## Score posiive sloped diagonal
    for r in range(total_rows - 3):
        for c in range(total_columns - 3):
            window = [game_board[r + i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    for r in range(total_rows - 3):
        for c in range(total_columns - 3):
            window = [game_board[r + 3 - i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    return score


def node_terminal_is(game_board):
    return winning_move(game_board, piece_drop_player) or winning_move(game_board, piece_drop_ai) or len(location_valid_gets(game_board)) == 0

#alpha beta pruning
def minimax(game_board, depth, alpha, beta, maximizingPlayer):
    valid_locations = location_valid_gets(game_board)
    is_terminal = node_terminal_is(game_board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(game_board, piece_drop_ai):
                return (None, 100000000000000)
            elif winning_move(game_board, piece_drop_player):
                return (None, -10000000000000)
            else:  # Game is over, no more valid moves
                return (None, 0)
        else:  # Depth is zero
            return (None, score_position(game_board, piece_drop_ai))
    if maximizingPlayer:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(game_board, col)
            b_copy = game_board.copy()
            piece_drop(b_copy, row, col, piece_drop_ai)
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
            row = get_next_open_row(game_board, col)
            b_copy = game_board.copy()
            piece_drop(b_copy, row, col, piece_drop_player)
            new_score = minimax(b_copy, depth - 1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value


def location_valid_gets(game_board):
    valid_locations = []
    for col in range(total_columns):
        if valid_is_location(game_board, col):
            valid_locations.append(col)
    return valid_locations


def pick_best_move(game_board, piece):
    valid_locations = location_valid_gets(game_board)
    best_score = -10000
    best_col = random.choice(valid_locations)
    for col in valid_locations:
        row = get_next_open_row(game_board, col)
        temp_board = game_board.copy()
        piece_drop(temp_board, row, col, piece)
        score = score_position(temp_board, piece)
        if score > best_score:
            best_score = score
            best_col = col

    return best_col


def board_draw(game_board):
    for c in range(total_columns):
        for r in range(total_rows):
            pygame.draw.rect(screen_window, GREEN, (c * SIZE_SQAURE, r * SIZE_SQAURE + SIZE_SQAURE , SIZE_SQAURE, SIZE_SQAURE))
            pygame.draw.circle(screen_window, BLACK, ( int(c * SIZE_SQAURE + SIZE_SQAURE / 2), int(r * SIZE_SQAURE + SIZE_SQAURE + SIZE_SQAURE / 2)), radii)

    for c in range(total_columns):
        for r in range(total_rows):
            if game_board[r][c] == piece_drop_player:
                pygame.draw.circle(screen_window, RED, (
                int(c * SIZE_SQAURE + SIZE_SQAURE / 2), height - int(r * SIZE_SQAURE + SIZE_SQAURE / 2)), radii)
            elif game_board[r][c] == piece_drop_ai:
                pygame.draw.circle(screen_window, BLUE, (
                int(c * SIZE_SQAURE + SIZE_SQAURE / 2), height - int(r * SIZE_SQAURE + SIZE_SQAURE / 2)), radii)
    pygame.display.update()


game_board = BOARD_CREATE()
board_print(game_board)
game_over = False

pygame.init()

SIZE_SQAURE = 100

width = (total_columns * SIZE_SQAURE)
height = (total_rows + 1) * SIZE_SQAURE

size = (width, height)

radii = int(SIZE_SQAURE / 2 - 10)

screen_window = pygame.display.set_mode(size)
board_draw(game_board)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 75)

turns = random.randint(PLAYER_TURN, AI_TURN)

while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen_window, BLACK, (0, 0, width, SIZE_SQAURE))
            posx = event.pos[0]
            if turns == PLAYER_TURN:
                pygame.draw.circle(screen_window, RED, (posx, int(SIZE_SQAURE / 2)), radii)

        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen_window, BLACK, (0, 0, width, SIZE_SQAURE))

            #Player Input
            if turns == PLAYER_TURN:
                posx = event.pos[0]
                col = int(math.floor(posx / SIZE_SQAURE))

                if valid_is_location(game_board, col):
                    row = get_next_open_row(game_board, col)
                    piece_drop(game_board, row, col, piece_drop_player)

                    if winning_move(game_board, piece_drop_player):
                        label = myfont.render("Player wins!!", 1, RED)
                        screen_window.blit(label, (40, 10))
                        game_over = True

                    turns += 1
                    turns = turns % 2

                    board_print(game_board)
                    board_draw(game_board)

    #  AI Input
    if turns == AI_TURN and not game_over:


        col, minimax_score = minimax(game_board, 5, -math.inf, math.inf, True)

        if valid_is_location(game_board, col):

            row = get_next_open_row(game_board, col)
            piece_drop(game_board, row, col, piece_drop_ai)

            if winning_move(game_board, piece_drop_ai):
                label = myfont.render("AI wins", 1, BLUE)
                screen_window.blit(label, (40, 10))
                game_over = True

            board_print(game_board)
            board_draw(game_board)

            turns += 1
            turns = turns % 2

    if game_over:
        pygame.time.wait(6000)
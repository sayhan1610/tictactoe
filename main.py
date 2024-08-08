import pygame
import sys
import numpy as np
import time

pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
LINE_WIDTH = 15
WIN_LINE_WIDTH = 15
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = SQUARE_SIZE // 4
FONT = pygame.font.SysFont(None, 60)

# Colors
BG_COLOR = (0, 0, 0)          # Black
LINE_COLOR = (255, 255, 255)   # White
CIRCLE_COLOR = (255, 182, 193) # Baby Pink
CROSS_COLOR = (0, 255, 255)    # Cyan
WIN_COLOR = (255, 255, 0)      # Yellow
TEXT_COLOR = (255, 255, 255)   # White

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT + 100))
pygame.display.set_caption('Tic Tac Toe')
screen.fill(BG_COLOR)

# Board
board = np.zeros((BOARD_ROWS, BOARD_COLS))

# Functions
def draw_lines():
    for row in range(1, BOARD_ROWS):
        pygame.draw.line(screen, LINE_COLOR, (0, row * SQUARE_SIZE), (WIDTH, row * SQUARE_SIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (row * SQUARE_SIZE, 0), (row * SQUARE_SIZE, HEIGHT), LINE_WIDTH)

def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 1:
                pygame.draw.circle(screen, CIRCLE_COLOR, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif board[row][col] == 2:
                pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE),
                                 (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE),
                                 (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), CROSS_WIDTH)

def mark_square(row, col, player):
    board[row][col] = player

def available_square(row, col):
    return board[row][col] == 0

def is_board_full():
    return np.all(board != 0)

def check_win(player):
    # Vertical, Horizontal & Diagonal Win Check
    for col in range(BOARD_COLS):
        if np.all(board[:, col] == player):
            draw_vertical_winning_line(col, player)
            return True
    for row in range(BOARD_ROWS):
        if np.all(board[row, :] == player):
            draw_horizontal_winning_line(row, player)
            return True
    if np.all(np.diag(board) == player):
        draw_desc_diagonal(player)
        return True
    if np.all(np.diag(np.fliplr(board)) == player):
        draw_asc_diagonal(player)
        return True
    return False

def draw_vertical_winning_line(col, player):
    posX = col * SQUARE_SIZE + SQUARE_SIZE // 2
    pygame.draw.line(screen, WIN_COLOR, (posX, 15), (posX, HEIGHT - 15), WIN_LINE_WIDTH)

def draw_horizontal_winning_line(row, player):
    posY = row * SQUARE_SIZE + SQUARE_SIZE // 2
    pygame.draw.line(screen, WIN_COLOR, (15, posY), (WIDTH - 15, posY), WIN_LINE_WIDTH)

def draw_asc_diagonal(player):
    pygame.draw.line(screen, WIN_COLOR, (15, HEIGHT - 15), (WIDTH - 15, 15), WIN_LINE_WIDTH)

def draw_desc_diagonal(player):
    pygame.draw.line(screen, WIN_COLOR, (15, 15), (WIDTH - 15, HEIGHT - 15), WIN_LINE_WIDTH)

def draw_turn_label(player, game_over):
    if game_over:
        if player == 0:
            turn_text = "It's a Tie!"
        else:
            turn_text = f"Player {player} Wins!"
    else:
        turn_text = "Player 1's (O) Turn" if player == 1 else "Player 2's (X) Turn"
    
    label = FONT.render(turn_text, True, TEXT_COLOR)
    screen.fill(BG_COLOR, (0, HEIGHT, WIDTH, 100))  # Clear previous label
    screen.blit(label, (WIDTH // 2 - label.get_width() // 2, HEIGHT + 20))

def restart():
    screen.fill(BG_COLOR)
    draw_lines()
    board.fill(0)

draw_lines()

# Variables
player = 1
game_over = False

# Main loop
while True:
    draw_turn_label(player, game_over)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouseX = event.pos[0]
            mouseY = event.pos[1]

            clicked_row = mouseY // SQUARE_SIZE
            clicked_col = mouseX // SQUARE_SIZE

            if available_square(clicked_row, clicked_col):
                mark_square(clicked_row, clicked_col, player)
                draw_figures()
                if check_win(player):
                    pygame.display.update()  # Update the display to show the win line
                    game_over = True
                elif is_board_full():
                    game_over = True
                    player = 0  # Use 0 to indicate a tie
                else:
                    player = 3 - player  # Switch between 1 (O) and 2 (X)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart()
                player = 1
                game_over = False

    pygame.display.update()

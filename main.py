import pygame
import sys
import numpy as np
import random
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
ICON_SIZE = 30
BUTTON_WIDTH, BUTTON_HEIGHT = 400, 60
CPU_MOVE_DELAY = 50  # Delay in milliseconds for CPU moves

# Default Settings
sound_on = True
theme_color = (0, 0, 0)          # Default Black

# Colors
BG_COLOR = (0, 0, 0)  # Default Background Color (Black)
LINE_COLOR = (255, 255, 255)     # White
CIRCLE_COLOR = (255, 182, 193)   # Baby Pink
CROSS_COLOR = (0, 255, 255)      # Cyan
WIN_COLOR = (255, 255, 0)        # Yellow
TEXT_COLOR = (255, 255, 255)     # White
BUTTON_COLOR = (128, 128, 128)   # Gray
BUTTON_HOVER_COLOR = (170, 170, 170)  # Lighter Gray
BUTTON_BORDER_COLOR = (255, 255, 255) # White

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT + 100))
pygame.display.set_caption('Tic Tac Toe')

# Load and scale reload icon
reload_icon = pygame.image.load("reload_icon.png")  # Replace with the path to your reload icon
reload_icon = pygame.transform.scale(reload_icon, (ICON_SIZE, ICON_SIZE))

# Load sounds
bg_music = pygame.mixer.Sound('audio/bg_music.mp3')
game_start_sound = pygame.mixer.Sound('audio/game_start.mp3')
game_win_sound = pygame.mixer.Sound('audio/game_win.mp3')
move_sounds = [pygame.mixer.Sound(f'audio/move{i}.mp3') for i in range(1, 5)]

# Play background music
bg_music.play(loops=-1) if sound_on else None

# Game states
HOME = "home"
INSTRUCTIONS = "instructions"
SETTINGS = "settings"
GAME = "game"
game_state = HOME
cpu_mode = False

# Global variable for winning lines
winning_lines = []

# Board
board = np.zeros((BOARD_ROWS, BOARD_COLS))

# Functions for the game
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
    global winning_lines
    winning_lines = []  # Reset winning lines each time
    # Vertical, Horizontal & Diagonal Win Check
    for col in range(BOARD_COLS):
        if np.all(board[:, col] == player):
            winning_lines.append(('vertical', col))
    for row in range(BOARD_ROWS):
        if np.all(board[row, :] == player):
            winning_lines.append(('horizontal', row))
    if np.all(np.diag(board) == player):
        winning_lines.append('desc_diagonal')
    if np.all(np.diag(np.fliplr(board)) == player):
        winning_lines.append('asc_diagonal')
    return len(winning_lines) > 0

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

def draw_winning_lines():
    for line in winning_lines:
        if line[0] == 'vertical':
            draw_vertical_winning_line(line[1], player)
        elif line[0] == 'horizontal':
            draw_horizontal_winning_line(line[1], player)
        elif line == 'desc_diagonal':
            draw_desc_diagonal(player)
        elif line == 'asc_diagonal':
            draw_asc_diagonal(player)

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
    return label.get_width() // 2

def restart():
    global winning_lines
    screen.fill(BG_COLOR)
    draw_lines()
    board.fill(0)
    winning_lines = []

def draw_restart_button(turn_label_width):
    button_x = (WIDTH // 2) + turn_label_width + 20  # Position it beside the turn label
    button_rect = pygame.Rect(button_x, HEIGHT + 25, ICON_SIZE, ICON_SIZE)
    screen.blit(reload_icon, (button_x, HEIGHT + 25))
    return button_rect

def draw_home_page():
    screen.fill(BG_COLOR)
    title = FONT.render("Tic Tac Toe", True, TEXT_COLOR)
    pvp_button = draw_button("Player vs Player", HEIGHT // 2 - 50)
    pvcpu_button = draw_button("Player vs CPU", HEIGHT // 2)
    instructions_button = draw_button("Instructions", HEIGHT // 2 + 100)
    settings_button = draw_button("Settings", HEIGHT // 2 + 150)
    
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 4))
    return (pvp_button, pvcpu_button, instructions_button, settings_button)

def draw_instructions_page():
    screen.fill(BG_COLOR)
    instructions = [
        "Instructions:",
        "1. The game is played on a 3x3 grid.",
        "2. Player 1 is O and Player 2 is X.",
        "3. Players take turns to place their mark on the grid.",
        "4. The first player to get 3 marks in a row wins!",
        "5. Rows, columns, and diagonals count.",
        "Press 'H' to go back to the Home page."
    ]
    
    y_offset = 50
    for line in instructions:
        instruction_text = FONT.render(line, True, TEXT_COLOR)
        screen.blit(instruction_text, (WIDTH // 2 - instruction_text.get_width() // 2, y_offset))
        y_offset += 50

def draw_settings_page():
    screen.fill(BG_COLOR)
    title = FONT.render("Settings", True, TEXT_COLOR)
    sound_button = draw_button("Sound: On" if sound_on else "Sound: Off", HEIGHT // 2 - 50)
    theme_button = draw_button("Change Theme", HEIGHT // 2)
    back_button = draw_button("Back", HEIGHT // 2 + 100)
    
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 4))
    return (sound_button, theme_button, back_button)

def draw_button(text, y_position):
    button_rect = pygame.Rect(WIDTH // 2 - BUTTON_WIDTH // 2, y_position, BUTTON_WIDTH, BUTTON_HEIGHT)
    pygame.draw.rect(screen, BUTTON_COLOR, button_rect)
    pygame.draw.rect(screen, BUTTON_BORDER_COLOR, button_rect, 2)
    button_text = FONT.render(text, True, TEXT_COLOR)
    screen.blit(button_text, (button_rect.x + BUTTON_WIDTH // 2 - button_text.get_width() // 2, button_rect.y + BUTTON_HEIGHT // 2 - button_text.get_height() // 2))
    return button_rect

def minimax(board, depth, alpha, beta, maximizing_player):
    if check_win(2):
        return 1
    elif check_win(1):
        return -1
    elif is_board_full():
        return 0

    if maximizing_player:
        max_eval = -np.inf
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if available_square(row, col):
                    board[row][col] = 2
                    eval = minimax(board, depth + 1, alpha, beta, False)
                    board[row][col] = 0
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
        return max_eval
    else:
        min_eval = np.inf
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if available_square(row, col):
                    board[row][col] = 1
                    eval = minimax(board, depth + 1, alpha, beta, True)
                    board[row][col] = 0
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
        return min_eval

def ai_move():
    best_move = None
    best_value = -np.inf
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if available_square(row, col):
                board[row][col] = 2
                move_value = minimax(board, 0, -np.inf, np.inf, False)
                board[row][col] = 0
                if move_value > best_value:
                    best_value = move_value
                    best_move = (row, col)

    if best_move:
        mark_square(best_move[0], best_move[1], 2)
        if sound_on:
            random.choice(move_sounds).play()
        draw_figures()
        time.sleep(CPU_MOVE_DELAY)
        return check_win(2)
    return False

# Main loop
player = 1
game_over = False
while True:
    if game_state == HOME:
        pvp_button_rect, pvcpu_button_rect, instructions_button_rect, settings_button_rect = draw_home_page()
    elif game_state == INSTRUCTIONS:
        draw_instructions_page()
    elif game_state == SETTINGS:
        sound_button_rect, theme_button_rect, back_button_rect = draw_settings_page()
    elif game_state == GAME:
        turn_label_width = draw_turn_label(player, game_over)
        restart_button = draw_restart_button(turn_label_width)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if game_state == HOME:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pvp_button_rect.collidepoint(event.pos):
                    game_start_sound.play() if sound_on else None
                    game_state = GAME
                    cpu_mode = False
                    restart()
                elif pvcpu_button_rect.collidepoint(event.pos):
                    game_start_sound.play() if sound_on else None
                    game_state = GAME
                    cpu_mode = True
                    restart()
                elif instructions_button_rect.collidepoint(event.pos):
                    game_state = INSTRUCTIONS
                elif settings_button_rect.collidepoint(event.pos):
                    game_state = SETTINGS

        elif game_state == INSTRUCTIONS:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_h:
                game_state = HOME

        elif game_state == SETTINGS:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if sound_button_rect.collidepoint(event.pos):
                    sound_on = not sound_on
                    if sound_on:
                        bg_music.play(loops=-1)
                    else:
                        bg_music.stop()
                elif theme_button_rect.collidepoint(event.pos):
                    # Change theme colors
                    if BG_COLOR == (0, 0, 0):
                        BG_COLOR = (255, 255, 255)  # White
                        LINE_COLOR = (0, 0, 0)      # Black
                        CIRCLE_COLOR = (0, 0, 255)  # Blue
                        CROSS_COLOR = (255, 0, 0)   # Red
                        WIN_COLOR = (0, 255, 0)     # Green
                    else:
                        BG_COLOR = (0, 0, 0)        # Black
                        LINE_COLOR = (255, 255, 255) # White
                        CIRCLE_COLOR = (255, 182, 193) # Baby Pink
                        CROSS_COLOR = (0, 255, 255) # Cyan
                        WIN_COLOR = (255, 255, 0)   # Yellow
                elif back_button_rect.collidepoint(event.pos):
                    game_state = HOME

        elif game_state == GAME:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = event.pos
                
                if restart_button.collidepoint(mouseX, mouseY):
                    restart()
                    player = 1
                    game_state = GAME
                    game_over = False

                if not game_over and not (cpu_mode and player == 2):
                    clicked_row = mouseY // SQUARE_SIZE
                    clicked_col = mouseX // SQUARE_SIZE

                    if clicked_row < BOARD_ROWS and available_square(clicked_row, clicked_col):
                        mark_square(clicked_row, clicked_col, player)
                        if sound_on:
                            random.choice(move_sounds).play()
                        draw_figures()
                        if check_win(player):
                            game_win_sound.play() if sound_on else None
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
                elif event.key == pygame.K_h:
                    game_state = HOME

            # Button hover effect
            if restart_button.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(screen, BUTTON_HOVER_COLOR, restart_button)
                screen.blit(reload_icon, (restart_button.x, restart_button.y))

            # CPU move logic
            if cpu_mode and player == 2 and not game_over:
                print("CPU is making a move...")
                if ai_move():
                    game_over = True
                else:
                    player = 1

    if game_over:
        draw_winning_lines()

    pygame.display.update()

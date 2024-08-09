# MIT License
# Copyright (c) 2024 Sayhan16160
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


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
difficulty_level = 10            # Default difficulty level is 10

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

# Particle class
class Particle:
    def __init__(self, x, y, color, speed, angle):
        self.x = x
        self.y = y
        self.color = color
        self.speed = speed
        self.angle = angle
        self.life = 100  # Particle life in frames

    def update(self):
        self.x += self.speed * np.cos(self.angle)
        self.y += self.speed * np.sin(self.angle)
        self.life -= 2  # Decrease life
        self.speed *= 0.95  # Slow down over time

    def draw(self, screen):
        if self.life > 0:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 5)

# Adding the particle effect on victory
def create_particles(x, y, color, num_particles=30):
    particles = []
    for _ in range(num_particles):
        angle = random.uniform(0, 2 * np.pi)
        speed = random.uniform(2, 7)
        particles.append(Particle(x, y, color, speed, angle))
    return particles

def update_particles():
    for particle in particles:
        particle.update()
        particle.draw(screen)

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
    global particles
    for line in winning_lines:
        if line[0] == 'vertical':
            draw_vertical_winning_line(line[1], player)
            particles = create_particles(line[1] * SQUARE_SIZE + SQUARE_SIZE // 2, HEIGHT // 2, WIN_COLOR)
        elif line[0] == 'horizontal':
            draw_horizontal_winning_line(line[1], player)
            particles = create_particles(WIDTH // 2, line[1] * SQUARE_SIZE + SQUARE_SIZE // 2, WIN_COLOR)
        elif line == 'desc_diagonal':
            draw_desc_diagonal(player)
            particles = create_particles(WIDTH // 2, HEIGHT // 2, WIN_COLOR)
        elif line == 'asc_diagonal':
            draw_asc_diagonal(player)
            particles = create_particles(WIDTH // 2, HEIGHT // 2, WIN_COLOR)

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
    global winning_lines, particles
    screen.fill(BG_COLOR)
    draw_lines()
    board.fill(0)
    winning_lines = []
    particles = []

def draw_restart_button(turn_label_width):
    button_x = (WIDTH // 2) + turn_label_width + 20  # Position it beside the turn label
    button_rect = pygame.Rect(button_x, HEIGHT + 25, ICON_SIZE, ICON_SIZE)
    screen.blit(reload_icon, (button_x, HEIGHT + 25))
    return button_rect

def draw_home_page():
    screen.fill(BG_COLOR)
    title = FONT.render("Tic Tac Toe", True, TEXT_COLOR)
    title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 4))
    screen.blit(title, title_rect)

    buttons = [
        ("Player vs Player", (WIDTH // 2, HEIGHT // 2 - 50)),
        ("Player vs CPU", (WIDTH // 2, HEIGHT // 2 + 50)),
        ("Settings", (WIDTH // 2, HEIGHT // 2 + 150)),
        ("Instructions", (WIDTH // 2, HEIGHT // 2 + 250))
    ]
    
    button_rects = []
    for text, pos in buttons:
        rect = draw_button(text, pos)
        button_rects.append(rect)

    return button_rects

def draw_button(text, position):
    button_rect = pygame.Rect(0, 0, BUTTON_WIDTH, BUTTON_HEIGHT)
    button_rect.center = position
    
    pygame.draw.rect(screen, BUTTON_COLOR, button_rect, border_radius=5)
    pygame.draw.rect(screen, BUTTON_BORDER_COLOR, button_rect, 2, border_radius=5)
    
    label = FONT.render(text, True, TEXT_COLOR)
    label_rect = label.get_rect(center=position)
    screen.blit(label, label_rect)
    
    return button_rect

def draw_instructions_page():
    screen.fill(BG_COLOR)
    instructions = [
        "How to Play:",
        "1. Player 1 is O and Player 2 is X.",
        "2. Players take turns to place their symbol on the grid.",
        "3. The first player to align 3 symbols vertically, horizontally, or diagonally wins.",
        "4. If the grid is filled and no one wins, the game is a tie.",
        "5. In CPU mode, the CPU makes the second move as Player 2 (X).",
        "6. You can adjust the difficulty level in the settings.",
    ]
    y_offset = HEIGHT // 4
    for line in instructions:
        instruction_text = FONT.render(line, True, TEXT_COLOR)
        screen.blit(instruction_text, (WIDTH // 2 - instruction_text.get_width() // 2, y_offset))
        y_offset += 40
    
    back_button = draw_button("Back", (WIDTH // 2, HEIGHT // 2 + 250))
    
    return back_button

def draw_settings_page():
    global sound_on, theme_color, difficulty_level
    
    screen.fill(BG_COLOR)
    settings = [
        f"Sound: {'On' if sound_on else 'Off'}",
        f"Difficulty Level: {difficulty_level}",
        f"Theme Color: {'Black' if theme_color == (0, 0, 0) else 'Blue'}",
    ]
    
    button_rects = []
    y_offset = HEIGHT // 4
    
    for line in settings:
        setting_text = FONT.render(line, True, TEXT_COLOR)
        screen.blit(setting_text, (WIDTH // 2 - setting_text.get_width() // 2, y_offset))
        y_offset += 40

    buttons = [
        ("Toggle Sound", (WIDTH // 2, HEIGHT // 2)),
        ("Difficulty Level", (WIDTH // 2, HEIGHT // 2 + 100)),
        ("Theme Color", (WIDTH // 2, HEIGHT // 2 + 200)),
        ("Back", (WIDTH // 2, HEIGHT // 2 + 300))
    ]
    
    for text, pos in buttons:
        rect = draw_button(text, pos)
        button_rects.append(rect)
    
    return button_rects

def cpu_turn():
    # Easy difficulty: Random move
    if difficulty_level <= 3:
        available = [(r, c) for r in range(BOARD_ROWS) for c in range(BOARD_COLS) if available_square(r, c)]
        return random.choice(available)

    # Medium difficulty: Prioritize blocking or winning
    if difficulty_level <= 6:
        for r in range(BOARD_ROWS):
            for c in range(BOARD_COLS):
                if available_square(r, c):
                    # Check if the CPU can win
                    board[r][c] = 2
                    if check_win(2):
                        return (r, c)
                    # Check if the player can win
                    board[r][c] = 1
                    if check_win(1):
                        return (r, c)
                    board[r][c] = 0
        return random.choice(available)

    # Hard difficulty: Optimal move
    if difficulty_level <= 9:
        best_score = -float('inf')
        best_move = None
        for r in range(BOARD_ROWS):
            for c in range(BOARD_COLS):
                if available_square(r, c):
                    board[r][c] = 2
                    score = minimax(board, False)
                    board[r][c] = 0
                    if score > best_score:
                        best_score = score
                        best_move = (r, c)
        return best_move

    # Impossible difficulty (same as before)
    return minimax_best_move()

def minimax(board, is_maximizing):
    if check_win(2):
        return 1
    elif check_win(1):
        return -1
    elif is_board_full():
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for r in range(BOARD_ROWS):
            for c in range(BOARD_COLS):
                if available_square(r, c):
                    board[r][c] = 2
                    score = minimax(board, False)
                    board[r][c] = 0
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for r in range(BOARD_ROWS):
            for c in range(BOARD_COLS):
                if available_square(r, c):
                    board[r][c] = 1
                    score = minimax(board, True)
                    board[r][c] = 0
                    best_score = min(score, best_score)
        return best_score

def minimax_best_move():
    best_score = -float('inf')
    best_move = None
    for r in range(BOARD_ROWS):
        for c in range(BOARD_COLS):
            if available_square(r, c):
                board[r][c] = 2
                score = minimax(board, False)
                board[r][c] = 0
                if score > best_score:
                    best_score = score
                    best_move = (r, c)
    return best_move

# Main loop
player = 1
game_over = False
particles = []
cpu_turn_pending = False  # Indicates if the CPU move is pending

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over and game_state == GAME:
            mouseX = event.pos[0]
            mouseY = event.pos[1]
            clicked_row = int(mouseY // SQUARE_SIZE)
            clicked_col = int(mouseX // SQUARE_SIZE)

            if available_square(clicked_row, clicked_col):
                mark_square(clicked_row, clicked_col, player)
                if sound_on:
                    move_sounds[player - 1].play()

                if check_win(player):
                    game_over = True
                    draw_winning_lines()
                    if sound_on:
                        game_win_sound.play()
                elif is_board_full():
                    game_over = True

                player = 2 if player == 1 else 1

        elif event.type == pygame.MOUSEBUTTONDOWN and game_state == HOME:
            mouseX, mouseY = event.pos
            for idx, rect in enumerate(home_buttons):
                if rect.collidepoint(mouseX, mouseY):
                    if idx == 0:
                        game_state = GAME
                    elif idx == 1:
                        game_state = GAME
                        cpu_mode = True
                    elif idx == 2:
                        game_state = SETTINGS
                    elif idx == 3:
                        game_state = INSTRUCTIONS
                    restart()

        elif event.type == pygame.MOUSEBUTTONDOWN and game_state == INSTRUCTIONS:
            mouseX, mouseY = event.pos
            if instructions_back_button.collidepoint(mouseX, mouseY):
                game_state = HOME

        elif event.type == pygame.MOUSEBUTTONDOWN and game_state == SETTINGS:
            mouseX, mouseY = event.pos
            for idx, rect in enumerate(settings_buttons):
                if rect.collidepoint(mouseX, mouseY):
                    if idx == 0:
                        sound_on = not sound_on
                        if sound_on:
                            bg_music.play(loops=-1)
                        else:
                            bg_music.stop()
                    elif idx == 1:
                        difficulty_level += 1
                        if difficulty_level > 10:
                            difficulty_level = 1
                    elif idx == 2:
                        if theme_color == (0, 0, 0):
                            theme_color = (0, 0, 255)  # Blue
                        else:
                            theme_color = (0, 0, 0)  # Black
                    elif idx == 3:
                        game_state = HOME
                    restart()

        elif event.type == pygame.MOUSEBUTTONDOWN and game_state == GAME:
            if restart_button_rect and restart_button_rect.collidepoint(event.pos):
                restart()
                game_over = False
                player = 1
                cpu_turn_pending = False

    if game_state == GAME:
        if cpu_mode and player == 2 and not game_over:
            cpu_turn_pending = True

    screen.fill(BG_COLOR)
    if game_state == HOME:
        home_buttons = draw_home_page()
    elif game_state == INSTRUCTIONS:
        instructions_back_button = draw_instructions_page()
    elif game_state == SETTINGS:
        settings_buttons = draw_settings_page()
    elif game_state == GAME:
        draw_lines()
        draw_figures()

        if cpu_mode and player == 2 and not game_over and cpu_turn_pending:
            pygame.time.wait(500)  # Adds a delay to mimic thinking
            move = cpu_turn()
            mark_square(move[0], move[1], 2)
            if sound_on:
                move_sounds[1].play()

            if check_win(2):
                game_over = True
                draw_winning_lines()
                if sound_on:
                    game_win_sound.play()
            elif is_board_full():
                game_over = True

            player = 1
            cpu_turn_pending = False

        if game_over:
            restart_button_rect = draw_button("Restart", (WIDTH // 2, HEIGHT // 2 + 50))

    pygame.display.update()

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
theme_color = (0, 0, 0)  # Default Black

# Colors
BG_COLOR = (0, 0, 0)  # Default Background Color (Black)
LINE_COLOR = (255, 255, 255)  # White
CIRCLE_COLOR = (255, 182, 193)  # Baby Pink
CROSS_COLOR = (0, 255, 255)  # Cyan
WIN_COLOR = (255, 255, 0)  # Yellow
TEXT_COLOR = (255, 255, 255)  # White
BUTTON_COLOR = (128, 128, 128)  # Gray
BUTTON_HOVER_COLOR = (170, 170, 170)  # Lighter Gray
BUTTON_BORDER_COLOR = (255, 255, 255)  # White

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
if sound_on:
    bg_music.play(loops=-1)

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

def draw_button(text, x, y, width, height, action=None):
    button_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(screen, BUTTON_COLOR, button_rect)
    pygame.draw.rect(screen, BUTTON_BORDER_COLOR, button_rect, 3)  # White border
    label = FONT.render(text, True, TEXT_COLOR)
    screen.blit(label, (x + (width - label.get_width()) // 2, y + (height - label.get_height()) // 2))
    return button_rect, action

def draw_home_screen():
    screen.fill(BG_COLOR)
    pygame.display.set_caption('Tic Tac Toe')

    # Draw game title
    title = FONT.render("Tic Tac Toe", True, TEXT_COLOR)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 4 - title.get_height() // 2))

    # Draw buttons
    buttons = []
    buttons.append(draw_button("1 Player", WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT // 2 - BUTTON_HEIGHT * 1.5, BUTTON_WIDTH, BUTTON_HEIGHT, lambda: start_game(cpu=True)))
    buttons.append(draw_button("2 Players", WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT // 2, BUTTON_WIDTH, BUTTON_HEIGHT, lambda: start_game(cpu=False)))
    buttons.append(draw_button("Instructions", WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT // 2 + BUTTON_HEIGHT * 2.5, BUTTON_WIDTH, BUTTON_HEIGHT, lambda: switch_state(INSTRUCTIONS)))
    buttons.append(draw_button("Settings", WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT // 2 + BUTTON_HEIGHT * 4, BUTTON_WIDTH, BUTTON_HEIGHT, lambda: switch_state(SETTINGS)))
    
    pygame.display.update()
    return buttons

def draw_instructions_screen():
    screen.fill(BG_COLOR)
    title = FONT.render("Instructions", True, TEXT_COLOR)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 4 - title.get_height() // 2))

    instructions = [
        "1. The game is played on a 3x3 grid.",
        "2. Player 1 is O and Player 2 (or CPU) is X.",
        "3. The first player to align 3 symbols vertically, horizontally,",
        "   or diagonally wins the game.",
        "4. If all 9 squares are filled without a winner, it's a tie."
    ]

    for i, line in enumerate(instructions):
        label = FONT.render(line, True, TEXT_COLOR)
        screen.blit(label, (WIDTH // 2 - label.get_width() // 2, HEIGHT // 2 - 50 + i * 40))

    buttons = []
    buttons.append(draw_button("Back", WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT // 2 + 100, BUTTON_WIDTH, BUTTON_HEIGHT, lambda: switch_state(HOME)))
    
    pygame.display.update()
    return buttons

def draw_settings_screen():
    screen.fill(BG_COLOR)
    title = FONT.render("Settings", True, TEXT_COLOR)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 4 - title.get_height() // 2))

    settings = [
        "Toggle Sound",
        "Change Theme Color"
    ]

    buttons = []
    for i, setting in enumerate(settings):
        buttons.append(draw_button(setting, WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT // 2 - 50 + i * 100, BUTTON_WIDTH, BUTTON_HEIGHT, None))

    buttons.append(draw_button("Back", WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT // 2 + 200, BUTTON_WIDTH, BUTTON_HEIGHT, lambda: switch_state(HOME)))
    
    pygame.display.update()
    return buttons

def switch_state(state):
    global game_state
    game_state = state
    if game_state == HOME:
        draw_home_screen()
    elif game_state == INSTRUCTIONS:
        draw_instructions_screen()
    elif game_state == SETTINGS:
        draw_settings_screen()
    elif game_state == GAME:
        restart()  # Start a new game

def start_game(cpu):
    global cpu_mode, player, game_over
    cpu_mode = cpu
    player = 1
    game_over = False
    switch_state(GAME)
    pygame.mixer.Sound.play(game_start_sound) if sound_on else None

# Main loop
player = 1
game_over = False
particles = []
buttons = draw_home_screen()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if game_state == HOME or game_state == INSTRUCTIONS or game_state == SETTINGS:
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button_rect, action in buttons:
                    if button_rect.collidepoint(event.pos) and action:
                        action()
        elif game_state == GAME:
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                mouseX = event.pos[0]
                mouseY = event.pos[1]

                clicked_row = int(mouseY // SQUARE_SIZE)
                clicked_col = int(mouseX // SQUARE_SIZE)

                if available_square(clicked_row, clicked_col):
                    mark_square(clicked_row, clicked_col, player)
                    draw_figures()
                    if check_win(player):
                        draw_winning_lines()
                        game_over = True
                        pygame.mixer.Sound.play(game_win_sound) if sound_on else None
                    else:
                        player = player % 2 + 1  # Switch to the other player
                        pygame.mixer.Sound.play(random.choice(move_sounds)) if sound_on else None
                        draw_turn_label(player, game_over)
                    pygame.display.update()

                    if game_over or is_board_full():
                        player = 0 if is_board_full() else player  # Set player to 0 in case of a tie
                        draw_turn_label(player, game_over)
                        restart_button_rect = draw_restart_button(turn_label_width)
                        pygame.display.update()

            elif event.type == pygame.MOUSEBUTTONDOWN and game_over:
                if restart_button_rect.collidepoint(event.pos):
                    restart()
                    player = 1
                    game_over = False
                    draw_turn_label(player, game_over)
                    pygame.display.update()

    if game_state == GAME:
        update_particles()
        pygame.display.update()
    pygame.display.update()

pygame.quit()
sys.exit()

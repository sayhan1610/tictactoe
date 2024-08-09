import pygame
import sys
import random

pygame.init()

# Game Constants
WIDTH, HEIGHT = 600, 600
SQUARE_SIZE = WIDTH // 3
LINE_WIDTH = 15
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = SQUARE_SIZE // 4
WIN_LINE_WIDTH = 15
PARTICLE_COUNT = 20
PARTICLE_SPEED = 5
HOME = 0
INSTRUCTIONS = 1
SETTINGS = 2
GAME = 3
CPU_MOVE_DELAY = 500  # milliseconds

# Colors
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)
PARTICLE_COLOR = (255, 255, 255)

# Font
FONT = pygame.font.SysFont(None, 60)

# Initialize game variables
board = [[0 for _ in range(3)] for _ in range(3)]
particles = []
player = 1
game_over = False
sound_on = True
cpu_mode = False
game_state = HOME
restart_button_rect = None

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic Tac Toe')

# Load sounds
move_sounds = [
    pygame.mixer.Sound('audio/move1.mp3'),
    pygame.mixer.Sound('audio/move2.mp3'),
    pygame.mixer.Sound('audio/move3.mp3'),
    pygame.mixer.Sound('audio/move4.mp3')
]
game_win_sound = pygame.mixer.Sound('audio/game_win.mp3')

def draw_lines():
    # Drawing the lines on the board
    for i in range(1, 3):
        pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE * i), (WIDTH, SQUARE_SIZE * i), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE * i, 0), (SQUARE_SIZE * i, HEIGHT), LINE_WIDTH)

def draw_figures():
    for row in range(3):
        for col in range(3):
            if board[row][col] == 1:
                pygame.draw.circle(screen, CIRCLE_COLOR, (int(col * SQUARE_SIZE + SQUARE_SIZE // 2), int(row * SQUARE_SIZE + SQUARE_SIZE // 2)), CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif board[row][col] == 2:
                pygame.draw.line(screen, CROSS_COLOR, 
                                 (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE),
                                 (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE),
                                 CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR, 
                                 (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE),
                                 (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE),
                                 CROSS_WIDTH)

def available_square(row, col):
    return board[row][col] == 0

def mark_square(row, col, player):
    board[row][col] = player

def check_win(player):
    # Check for winning combinations
    for col in range(3):
        if board[0][col] == player and board[1][col] == player and board[2][col] == player:
            draw_vertical_winning_line(col, player)
            return True

    for row in range(3):
        if board[row][0] == player and board[row][1] == player and board[row][2] == player:
            draw_horizontal_winning_line(row, player)
            return True

    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        draw_desc_diagonal(player)
        return True

    if board[2][0] == player and board[1][1] == player and board[0][2] == player:
        draw_asc_diagonal(player)
        return True

    return False

def draw_vertical_winning_line(col, player):
    posX = col * SQUARE_SIZE + SQUARE_SIZE // 2
    color = CIRCLE_COLOR if player == 1 else CROSS_COLOR
    pygame.draw.line(screen, color, (posX, 15), (posX, HEIGHT - 15), WIN_LINE_WIDTH)

def draw_horizontal_winning_line(row, player):
    posY = row * SQUARE_SIZE + SQUARE_SIZE // 2
    color = CIRCLE_COLOR if player == 1 else CROSS_COLOR
    pygame.draw.line(screen, color, (15, posY), (WIDTH - 15, posY), WIN_LINE_WIDTH)

def draw_asc_diagonal(player):
    color = CIRCLE_COLOR if player == 1 else CROSS_COLOR
    pygame.draw.line(screen, color, (15, HEIGHT - 15), (WIDTH - 15, 15), WIN_LINE_WIDTH)

def draw_desc_diagonal(player):
    color = CIRCLE_COLOR if player == 1 else CROSS_COLOR
    pygame.draw.line(screen, color, (15, 15), (WIDTH - 15, HEIGHT - 15), WIN_LINE_WIDTH)

def restart():
    global board, particles, player, game_over
    screen.fill(BG_COLOR)
    draw_lines()
    player = 1
    game_over = False
    board = [[0 for _ in range(3)] for _ in range(3)]
    particles = []

def update_particles():
    for particle in particles[:]:
        particle[0] += particle[2]
        particle[1] += particle[3]
        particle[2] *= 0.95  # Damping
        particle[3] *= 0.95  # Damping
        particle[3] += 0.5  # Gravity
        if particle[0] > WIDTH or particle[0] < 0 or particle[1] > HEIGHT or particle[1] < 0:
            particles.remove(particle)
        else:
            pygame.draw.circle(screen, PARTICLE_COLOR, (int(particle[0]), int(particle[1])), 3)

def create_particles(x, y):
    for _ in range(PARTICLE_COUNT):
        particles.append([x, y, random.uniform(-PARTICLE_SPEED, PARTICLE_SPEED), random.uniform(-PARTICLE_SPEED, PARTICLE_SPEED)])

def draw_turn_label(player, game_over):
    label = "Player 1" if player == 1 else "Player 2"
    if game_over:
        label = "Game Over"
    text = FONT.render(label, True, (255, 255, 255))
    text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2 + SQUARE_SIZE*1.5))
    screen.blit(text, text_rect)
    return text_rect.width

def draw_restart_button(turn_label_width):
    restart_label = "Restart"
    text = FONT.render(restart_label, True, (255, 255, 255))
    text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2 + SQUARE_SIZE*2))
    pygame.draw.rect(screen, BG_COLOR, text_rect.inflate(20, 10))
    screen.blit(text, text_rect)
    return text_rect

# Implement the Home, Instructions, and Settings screens similarly
def draw_home():
    # Placeholder implementation for the Home screen
    screen.fill(BG_COLOR)
    play_button = pygame.Rect(WIDTH // 4, HEIGHT // 4, WIDTH // 2, 100)
    instructions_button = pygame.Rect(WIDTH // 4, HEIGHT // 2, WIDTH // 2, 100)
    settings_button = pygame.Rect(WIDTH // 4, 3 * HEIGHT // 4, WIDTH // 2, 100)
    pygame.draw.rect(screen, (100, 100, 100), play_button)
    pygame.draw.rect(screen, (100, 100, 100), instructions_button)
    pygame.draw.rect(screen, (100, 100, 100), settings_button)
    return play_button, instructions_button, settings_button

def draw_instructions():
    # Placeholder implementation for the Instructions screen
    screen.fill(BG_COLOR)
    back_button = pygame.Rect(WIDTH // 4, 3 * HEIGHT // 4, WIDTH // 2, 100)
    pygame.draw.rect(screen, (100, 100, 100), back_button)
    return back_button

def draw_settings():
    # Placeholder implementation for the Settings screen
    screen.fill(BG_COLOR)
    sound_button = pygame.Rect(WIDTH // 4, HEIGHT // 4, WIDTH // 2, 100)
    color_button = pygame.Rect(WIDTH // 4, HEIGHT // 2, WIDTH // 2, 100)
    pygame.draw.rect(screen, (100, 100, 100), sound_button)
    pygame.draw.rect(screen, (100, 100, 100), color_button)
    return sound_button, color_button

def handle_home_click(pos):
    global game_state
    if play_button.collidepoint(pos):
        game_state = GAME
        restart()
    elif instructions_button.collidepoint(pos):
        game_state = INSTRUCTIONS
    elif settings_button.collidepoint(pos):
        game_state = SETTINGS

def handle_instructions_click(pos):
    global game_state
    if back_button.collidepoint(pos):
        game_state = HOME

def handle_settings_click(pos):
    global sound_on, cpu_mode
    if sound_button.collidepoint(pos):
        sound_on = not sound_on
    elif color_button.collidepoint(pos):
        cpu_mode = not cpu_mode

player = 1
game_over = False
particles = []
restart_button_rect = None

while True:
    if game_state == HOME:
        play_button, instructions_button, settings_button = draw_home()

    elif game_state == INSTRUCTIONS:
        back_button = draw_instructions()

    elif game_state == SETTINGS:
        sound_button, color_button = draw_settings()

    elif game_state == GAME:
        draw_turn_label(player, game_over)
        draw_figures()
        draw_winning_lines()
        update_particles()

        if game_over and not cpu_mode:
            turn_label_width = draw_turn_label(0, game_over)
            restart_button_rect = draw_restart_button(turn_label_width)  # Define the button

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if game_state in [INSTRUCTIONS, SETTINGS]:
                    game_state = HOME
                elif game_state == GAME:
                    game_state = HOME  # Or we could implement a pause feature
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos

            if game_state == HOME:
                handle_home_click(pos)
            elif game_state == INSTRUCTIONS:
                handle_instructions_click(pos)
            elif game_state == SETTINGS:
                handle_settings_click(pos)
            elif game_state == GAME and not game_over:
                if event.button == 1:
                    row = pos[1] // SQUARE_SIZE
                    col = pos[0] // SQUARE_SIZE

                    if available_square(row, col):
                        if sound_on:
                            move_sounds[random.randint(0, 3)].play()
                        mark_square(row, col, player)
                        if check_win(player):
                            game_over = True
                            game_win_sound.play() if sound_on else None
                        player = 2 if player == 1 else 1

                    if player == 2 and cpu_mode and not game_over:
                        pygame.time.wait(CPU_MOVE_DELAY)
                        cpu_move()
                        if check_win(2):
                            game_over = True
                            game_win_sound.play() if sound_on else None
                        player = 1

                # Restart button
                if game_over and restart_button_rect is not None:
                    if restart_button_rect.collidepoint(pos):
                        restart()
                        player = 1
                        game_over = False
                        restart_button_rect = None  # Reset button rect

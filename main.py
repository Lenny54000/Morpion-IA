import pygame
import sys
import random

# Initialisation de pygame
pygame.init()

# Couleurs
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Paramètres de la fenêtre
WINDOW_SIZE = 300
GRID_SIZE = WINDOW_SIZE // 3
LINE_WIDTH = 5

# Initialisation de la fenêtre
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE + 50))  # Ajouter de l'espace pour le bouton
pygame.display.set_caption("Morpion (Tic Tac Toe)")

# Polices de texte
font = pygame.font.SysFont(None, 48)

# Variables globales
board = [[" " for _ in range(3)] for _ in range(3)]
current_player = random.choice(["X", "O"])
result_message = ""
use_delay = True  # Indique si on utilise le délai d'une seconde entre les coups des bots

# Fonction pour dessiner la grille
def draw_grid():
    for i in range(1, 3):
        pygame.draw.line(screen, BLACK, (i * GRID_SIZE, 0), (i * GRID_SIZE, WINDOW_SIZE), LINE_WIDTH)
        pygame.draw.line(screen, BLACK, (0, i * GRID_SIZE), (WINDOW_SIZE, i * GRID_SIZE), LINE_WIDTH)

# Fonction pour dessiner les symboles
def draw_symbols(board):
    for i in range(3):
        for j in range(3):
            symbol = board[i][j]
            if symbol == "X":
                draw_x(i, j)
            elif symbol == "O":
                draw_o(i, j)

def draw_x(row, col):
    x_offset = col * GRID_SIZE
    y_offset = row * GRID_SIZE
    pygame.draw.line(screen, BLUE, (x_offset + 20, y_offset + 20), (x_offset + GRID_SIZE - 20, y_offset + GRID_SIZE - 20), LINE_WIDTH)
    pygame.draw.line(screen, BLUE, (x_offset + GRID_SIZE - 20, y_offset + 20), (x_offset + 20, y_offset + GRID_SIZE - 20), LINE_WIDTH)

def draw_o(row, col):
    x_center = col * GRID_SIZE + GRID_SIZE // 2
    y_center = row * GRID_SIZE + GRID_SIZE // 2
    radius = GRID_SIZE // 2 - 20
    pygame.draw.circle(screen, RED, (x_center, y_center), radius, LINE_WIDTH)

# Fonction pour vérifier s'il y a un gagnant
def check_winner(board, player):
    for row in board:
        if all(symbol == player for symbol in row):
            return True
    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True
    if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
        return True
    return False

# Fonction pour vérifier si la grille est pleine
def is_full(board):
    return all(all(symbol != " " for symbol in row) for row in board)

# Fonction pour l'algorithme Minimax avec élagage alpha-bêta
def minimax(board, depth, is_maximizing, alpha, beta):
    # Vérification si le jeu est terminé
    if check_winner(board, "X"):
        return -10 + depth, None
    elif check_winner(board, "O"):
        return 10 - depth, None
    elif is_full(board):
        return 0, None

    if is_maximizing:
        max_eval = -float('inf')
        best_move = None
        for i in range(3):
            for j in range(3):
                if board[i][j] == " ":
                    board[i][j] = "O"
                    eval, _ = minimax(board, depth + 1, False, alpha, beta)
                    board[i][j] = " "
                    if eval > max_eval:
                        max_eval = eval
                        best_move = (i, j)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
        return max_eval, best_move
    else:
        min_eval = float('inf')
        best_move = None
        for i in range(3):
            for j in range(3):
                if board[i][j] == " ":
                    board[i][j] = "X"
                    eval, _ = minimax(board, depth + 1, True, alpha, beta)
                    board[i][j] = " "
                    if eval < min_eval:
                        min_eval = eval
                        best_move = (i, j)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
        return min_eval, best_move

# Fonction pour le tour du bot utilisant l'algorithme Minimax
def bot_turn(board, player):
    if player == "X":
        _, move = minimax(board, 0, True, -float('inf'), float('inf'))
    else:
        _, move = minimax(board, 0, False, -float('inf'), float('inf'))
    
    if move:
        board[move[0]][move[1]] = player

# Fonction pour réinitialiser le jeu
def reset_game():
    global board, current_player, result_message
    board = [[" " for _ in range(3)] for _ in range(3)]
    current_player = random.choice(["X", "O"])
    result_message = ""

# Fonction principale pour le jeu
def main():
    global use_delay

    button_rect = pygame.Rect(100, WINDOW_SIZE + 10, 100, 30)
    button_text = font.render("Toggle Delay", True, BLACK)
    button_color = GRAY

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and button_rect.collidepoint(event.pos):
                    use_delay = not use_delay
                    button_color = WHITE if use_delay else GRAY

        screen.fill(WHITE)
        draw_grid()
        draw_symbols(board)

        if result_message:
            result_surf = font.render(result_message, True, BLACK)
            screen.blit(result_surf, (50, WINDOW_SIZE // 2 - 24))
            pygame.display.flip()
            pygame.time.wait(1000)
            reset_game()
            continue

        pygame.draw.rect(screen, button_color, button_rect)
        screen.blit(button_text, (button_rect.x + 5, button_rect.y + 5))

        pygame.display.flip()

        if current_player == "X":
            if use_delay:
                pygame.time.wait(1000)  # Délai de 1 seconde
            bot_turn(board, "X")
            if check_winner(board, "X"):
                result_message = "Le joueur X a gagné!"
            elif is_full(board):
                result_message = "Match nul!"
            else:
                current_player = "O"
        elif current_player == "O":
            if use_delay:
                pygame.time.wait(1000)  # Délai de 1 seconde
            bot_turn(board, "O")
            if check_winner(board, "O"):
                result_message = "Le joueur O a gagné!"
            elif is_full(board):
                result_message = "Match nul!"
            else:
                current_player = "X"

# Lancement du jeu
if __name__ == "__main__":
    main()

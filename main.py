import pygame
import sys
import random

# Game Constants
WIDTH, HEIGHT = 640, 640
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (50, 50, 50)
RED = (255, 50, 50)
BLUE = (50, 50, 255)
GREEN = (50, 255, 50)
HIGHLIGHT_COLOR = (144, 238, 144)
BURN_COLOR = (218, 104, 18)
TEXT_COLOR = (255, 255, 255)

class Knight:
    def __init__(self, row, col, color, name, label, is_computer=False):
        self.row = row
        self.col = col
        self.color = color
        self.name = name
        self.label = label
        self.is_computer = is_computer

    def get_valid_moves(self, board, opponent_pos):
        moves = []
        directions = [
            (-2, -1), (-2, 1), (-1, -2), (-1, 2),
            (1, -2), (1, 2), (2, -1), (2, 1)
        ]
        for dr, dc in directions:
            r, c = self.row + dr, self.col + dc
            if 0 <= r < ROWS and 0 <= c < COLS:
                # Valid if square is not burnt OR if it's the opponent's current square
                if board.grid[r][c] == 0 or (r, c) == opponent_pos:
                    moves.append((r, c))
        return moves

class Board:
    def __init__(self):
        # 0 = empty, 1 = burnt
        self.grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]
    
    def burn_square(self, row, col):
        self.grid[row][col] = 1

def draw_board(win, board, p1, p2, valid_moves, font):
    win.fill(WHITE)
    
    # Draw grid
    for row in range(ROWS):
        for col in range(COLS):
            rect = pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            
            # Checkerboard pattern
            if (row + col) % 2 == 0:
                pygame.draw.rect(win, GRAY, rect)
            else:
                pygame.draw.rect(win, DARK_GRAY, rect)
            
            # Draw Burnt squares over the pattern
            if board.grid[row][col] == 1:
                pygame.draw.rect(win, BURN_COLOR, rect)
            
            # Highlight valid moves
            if (row, col) in valid_moves:
                pygame.draw.rect(win, HIGHLIGHT_COLOR, rect)
                pygame.draw.circle(win, GREEN, (col * SQUARE_SIZE + SQUARE_SIZE//2, row * SQUARE_SIZE + SQUARE_SIZE//2), 10)
            
            pygame.draw.rect(win, BLACK, rect, 1) # Square borders

    # Draw Knights
    for player in [p1, p2]:
        center = (player.col * SQUARE_SIZE + SQUARE_SIZE//2, player.row * SQUARE_SIZE + SQUARE_SIZE//2)
        pygame.draw.circle(win, player.color, center, SQUARE_SIZE//2 - 10)
        
        # 'K' Text
        text = font.render(player.label, True, TEXT_COLOR)
        text_rect = text.get_rect(center=center)
        win.blit(text, text_rect)

def draw_ui(win, current_player, game_over, winner_msg, font, big_font):
    if game_over:
        # Victory message
        text = big_font.render(winner_msg, True, GREEN)
        text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2 - 30))
        
        restart_text = font.render("Press SPACE to play again", True, WHITE)
        restart_rect = restart_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 30))
        
        bg_rect = pygame.Rect(
            min(text_rect.left, restart_rect.left) - 20, 
            text_rect.top - 20, 
            max(text_rect.width, restart_rect.width) + 40, 
            text_rect.height + restart_rect.height + 60
        )
        
        pygame.draw.rect(win, BLACK, bg_rect)
        pygame.draw.rect(win, WHITE, bg_rect, 2)
        
        win.blit(text, text_rect)
        win.blit(restart_text, restart_rect)
    else:
        # Turn indicator
        turn_text = font.render(f"Turn: {current_player.name}", True, current_player.color)
        bg_rect = pygame.Rect(5, 5, turn_text.get_width() + 20, turn_text.get_height() + 10)
        pygame.draw.rect(win, BLACK, bg_rect)
        pygame.draw.rect(win, WHITE, bg_rect, 2)
        win.blit(turn_text, (15, 10))

def intro_screen(win, font, big_font):
    win.fill(WHITE)
    title = big_font.render("Knight Chase", True, BLACK)
    title_rect = title.get_rect(center=(WIDTH//2, HEIGHT//3))
    win.blit(title, title_rect)
    
    prompt1 = font.render("Press 1 for Player vs Player", True, DARK_GRAY)
    prompt2 = font.render("Press 2 for Player vs Computer", True, DARK_GRAY)
    
    win.blit(prompt1, prompt1.get_rect(center=(WIDTH//2, HEIGHT//2)))
    win.blit(prompt2, prompt2.get_rect(center=(WIDTH//2, HEIGHT//2 + 50)))
    
    pygame.display.update()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return False
                elif event.key == pygame.K_2:
                    return True

def main():
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Knight Chase")
    clock = pygame.time.Clock()
    
    font = pygame.font.SysFont(None, 40)
    big_font = pygame.font.SysFont(None, 60)
    
    vs_computer = intro_screen(win, font, big_font)
    
    board = Board()
    p1 = Knight(0, 0, BLUE, "Player A", "K-A")
    p2 = Knight(ROWS-1, COLS-1, RED, "Player B", "K-B", is_computer=vs_computer)
    
    current_player = p1
    other_player = p2
    
    running = True
    game_over = False
    winner_msg = ""
    
    while running:
        clock.tick(FPS)
        
        opponent_pos = (other_player.row, other_player.col)
        
        # Calculate valid moves before handling events
        if not game_over:
            valid_moves = current_player.get_valid_moves(board, opponent_pos)
            
            # Trap condition
            if len(valid_moves) == 0:
                game_over = True
                winner_msg = f"{other_player.name} WINS! (Trap)"
        else:
            valid_moves = []
            
        if not game_over and current_player.is_computer:
            pygame.time.delay(500)
            if opponent_pos in valid_moves:
                row, col = opponent_pos
            else:
                row, col = random.choice(valid_moves)
                
            if (row, col) == (other_player.row, other_player.col):
                board.burn_square(current_player.row, current_player.col)
                current_player.row, current_player.col = row, col
                game_over = True
                winner_msg = f"{current_player.name} WINS! (Capture)"
            else:
                board.burn_square(current_player.row, current_player.col)
                current_player.row, current_player.col = row, col
                current_player, other_player = other_player, current_player
                
            pygame.event.clear(pygame.MOUSEBUTTONDOWN)
            continue
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            if game_over:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    main() # Restart the game
                    return
                continue
                
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over and not current_player.is_computer:
                x, y = event.pos
                col, row = x // SQUARE_SIZE, y // SQUARE_SIZE
                
                if (row, col) in valid_moves:
                    # Capture condition
                    if (row, col) == (other_player.row, other_player.col):
                        board.burn_square(current_player.row, current_player.col)
                        current_player.row, current_player.col = row, col
                        game_over = True
                        winner_msg = f"{current_player.name} WINS! (Capture)"
                    else:
                        # Standard move
                        board.burn_square(current_player.row, current_player.col)
                        current_player.row, current_player.col = row, col
                        
                        # Swap turns
                        current_player, other_player = other_player, current_player

        # Render
        draw_board(win, board, p1, p2, valid_moves, font)
        draw_ui(win, current_player, game_over, winner_msg, font, big_font)
        pygame.display.update()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

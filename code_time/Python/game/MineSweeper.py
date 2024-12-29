# pip install pygame
import pygame, sys, random
from pygame.locals import *

pygame.init()
WIDTH, HEIGHT = 800, 800
ROWS, COLS = 16, 16
CELL_SIZE = WIDTH // COLS
MINES = 40
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minesweeper")
FONT = pygame.font.SysFont('Arial', CELL_SIZE//2)
BIG_FONT = pygame.font.SysFont('Arial', 40)
BLACK, WHITE, GRAY, DARK_GRAY, RED, GREEN, BLUE, YELLOW = (0,0,0), (255,255,255), (192,192,192), (128,128,128), (255,0,0), (0,255,0), (0,0,255), (255,255,0)

class Cell:
    def __init__(self, row, col):
        self.row, self.col = row, col
        self.rect = pygame.Rect(col*CELL_SIZE, row*CELL_SIZE, CELL_SIZE, CELL_SIZE)
        self.mine = False
        self.revealed = False
        self.flagged = False
        self.adjacent = 0
    def draw(self):
        if self.revealed:
            pygame.draw.rect(screen, GRAY, self.rect)
            if self.mine:
                pygame.draw.circle(screen, BLACK, self.rect.center, CELL_SIZE//4)
            elif self.adjacent > 0:
                text = FONT.render(str(self.adjacent), True, self.get_color())
                screen.blit(text, (self.rect.x + CELL_SIZE//4, self.rect.y + CELL_SIZE//8))
        else:
            pygame.draw.rect(screen, DARK_GRAY, self.rect)
            if self.flagged:
                pygame.draw.polygon(screen, RED, [
                    (self.rect.x + CELL_SIZE//4, self.rect.y + CELL_SIZE//4),
                    (self.rect.x + 3*CELL_SIZE//4, self.rect.y + CELL_SIZE//2),
                    (self.rect.x + CELL_SIZE//4, self.rect.y + 3*CELL_SIZE//4)
                ])
        pygame.draw.rect(screen, BLACK, self.rect, 1)
    def get_color(self):
        colors = {1: BLUE, 2: GREEN, 3: RED, 4: DARK_GRAY, 5: YELLOW, 6: BLUE, 7: BLACK, 8: GREEN}
        return colors.get(self.adjacent, BLACK)

def create_grid():
    grid = [[Cell(r, c) for c in range(COLS)] for r in range(ROWS)]
    mines = random.sample(range(ROWS*COLS), MINES)
    for m in mines:
        r, c = divmod(m, COLS)
        grid[r][c].mine = True
    for r in range(ROWS):
        for c in range(COLS):
            if grid[r][c].mine:
                continue
            count = 0
            for dr in (-1,0,1):
                for dc in (-1,0,1):
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < ROWS and 0 <= nc < COLS and grid[nr][nc].mine:
                        count +=1
            grid[r][c].adjacent = count
    return grid

def reveal(grid, r, c):
    if grid[r][c].revealed or grid[r][c].flagged:
        return
    grid[r][c].revealed = True
    if grid[r][c].adjacent == 0 and not grid[r][c].mine:
        for dr in (-1,0,1):
            for dc in (-1,0,1):
                nr, nc = r + dr, c + dc
                if 0 <= nr < ROWS and 0 <= nc < COLS:
                    reveal(grid, nr, nc)

def check_win(grid):
    for row in grid:
        for cell in row:
            if not cell.mine and not cell.revealed:
                return False
    return True

def main():
    clock = pygame.time.Clock()
    grid = create_grid()
    game_over, win = False, False
    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN and not game_over and not win:
                x, y = pygame.mouse.get_pos()
                r, c = y // CELL_SIZE, x // CELL_SIZE
                if 0 <= r < ROWS and 0 <= c < COLS:
                    cell = grid[r][c]
                    if event.button == 1:
                        reveal(grid, r, c)
                        if cell.mine:
                            game_over = True
                            for row in grid:
                                for ccell in row:
                                    if ccell.mine:
                                        ccell.revealed = True
                    elif event.button == 3:
                        cell.flagged = not cell.flagged
            if event.type == KEYDOWN:
                if event.key == K_r:
                    grid = create_grid()
                    game_over, win = False, False
        if not game_over and not win:
            if check_win(grid):
                win = True
        screen.fill(BLACK)
        for row in grid:
            for cell in row:
                cell.draw()
        if game_over:
            text = BIG_FONT.render("Game Over! Press R to Restart.", True, RED)
            screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))
        if win:
            text = BIG_FONT.render("You Win! Press R to Restart.", True, GREEN)
            screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))
        pygame.display.flip()

main()

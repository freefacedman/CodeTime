#pip install pygame
import sys
import random

import pygame

pygame.init()

WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20
GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = HEIGHT // CELL_SIZE
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock()

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)


def draw_grid():
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(SCREEN, BLACK, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(SCREEN, BLACK, (0, y), (WIDTH, y))


def random_position():
    return (
        random.randint(0, GRID_WIDTH - 1) * CELL_SIZE,
        random.randint(0, GRID_HEIGHT - 1) * CELL_SIZE,
    )


def main():
    snake = [(WIDTH // 2, HEIGHT // 2)]
    direction = (CELL_SIZE, 0)
    food = random_position()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != (0, CELL_SIZE):
                    direction = (0, -CELL_SIZE)
                elif event.key == pygame.K_DOWN and direction != (0, -CELL_SIZE):
                    direction = (0, CELL_SIZE)
                elif event.key == pygame.K_LEFT and direction != (CELL_SIZE, 0):
                    direction = (-CELL_SIZE, 0)
                elif event.key == pygame.K_RIGHT and direction != (-CELL_SIZE, 0):
                    direction = (CELL_SIZE, 0)

        head = (snake[0][0] + direction[0], snake[0][1] + direction[1])

        if head in snake or not (0 <= head[0] < WIDTH and 0 <= head[1] < HEIGHT):
            pygame.quit()
            sys.exit()

        snake.insert(0, head)

        if head == food:
            food = random_position()
        else:
            snake.pop()

        SCREEN.fill(WHITE)
        draw_grid()

        for segment in snake:
            pygame.draw.rect(
                SCREEN, GREEN, pygame.Rect(segment[0], segment[1], CELL_SIZE, CELL_SIZE)
            )
        pygame.draw.rect(SCREEN, RED, pygame.Rect(food[0], food[1], CELL_SIZE, CELL_SIZE))

        pygame.display.flip()
        CLOCK.tick(15)


if __name__ == "__main__":
    main()

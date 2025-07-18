import math
import queue
import pygame

WIDTH, HEIGHT = 800, 600
NUM_LINES = 30


def run_display(speed_queue):
    """Display a simple moving tunnel controlled by speed."""
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    speed = 1.0
    offset = 0.0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        try:
            speed = speed_queue.get_nowait()
        except queue.Empty:
            pass

        offset += speed
        screen.fill((0, 0, 0))

        for i in range(NUM_LINES):
            depth = (i + offset) % NUM_LINES
            scale = depth / NUM_LINES
            size = (1 - scale) * min(WIDTH, HEIGHT)
            color = 255 - int(scale * 255)
            rect = pygame.Rect(0, 0, size, size)
            rect.center = (WIDTH // 2, HEIGHT // 2)
            pygame.draw.rect(screen, (color, color, color), rect, 2)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

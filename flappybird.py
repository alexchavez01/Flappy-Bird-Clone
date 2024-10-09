import pygame
import random

pygame.init()

WIDTH, HEIGHT = 400, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

FPS = 30
GRAVITY = 1
JUMP = -14
PIPE_WIDTH = 70
PIPE_GAP = 150

bird_img = pygame.Surface((30, 30))
bird_img.fill((255, 255, 0))


class Pipe:
    def __init__(self):
        self.x = WIDTH
        self.height = random.randint(50, HEIGHT - PIPE_GAP - 50)
        self.top = pygame.Rect(self.x, 0, PIPE_WIDTH, self.height)
        self.bottom = pygame.Rect(self.x, self.height + PIPE_GAP, PIPE_WIDTH, HEIGHT - self.height - PIPE_GAP)

    def update(self):
        self.x -= 5
        self.top.topleft = (self.x, 0)
        self.bottom.topleft = (self.x, self.height + PIPE_GAP)

    def draw(self, win):
        pygame.draw.rect(win, GREEN, self.top)
        pygame.draw.rect(win, GREEN, self.bottom)


class Bird:
    def __init__(self):
        self.x = 100
        self.y = HEIGHT // 2
        self.vel = 0
        self.rect = pygame.Rect(self.x, self.y, 30, 30)

    def update(self):
        self.y += self.vel
        self.vel += GRAVITY
        self.rect.topleft = (self.x, self.y)

    def jump(self):
        self.vel = JUMP

    def draw(self, win):
        win.blit(bird_img, (self.x, self.y))


def game_over(win, score, high_score):
    font_big = pygame.font.SysFont(None, 72)
    font_small = pygame.font.SysFont(None, 36)

    game_over_text = font_big.render("Game Over", True, BLACK)
    score_text = font_big.render(f"Score: {score}", True, BLACK)
    high_score_text = font_small.render(f"High Score: {high_score}", True, BLACK)
    restart_text = font_small.render("Press SPACE to Restart", True, BLACK)

    win.fill(WHITE)
    win.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 3))
    win.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
    win.blit(high_score_text, (WIDTH // 2 - high_score_text.get_width() // 2, HEIGHT // 2 + 50))
    win.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 100))
    pygame.display.update()
    wait_for_restart()


def wait_for_restart():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False


def main():
    clock = pygame.time.Clock()
    high_score = 0  # Initialize high score

    while True:  # Loop to restart the game
        bird = Bird()  # Reinitialize the bird
        pipes = [Pipe()]  # Reinitialize pipes
        score = 0
        font = pygame.font.SysFont(None, 36)

        run = True
        while run:
            clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    bird.jump()

            bird.update()

            if pipes[-1].x < WIDTH // 2:
                pipes.append(Pipe())

            for pipe in pipes[:]:
                pipe.update()
                if pipe.x + PIPE_WIDTH < 0:
                    pipes.remove(pipe)
                    score += 1

            for pipe in pipes:
                if bird.rect.colliderect(pipe.top) or bird.rect.colliderect(pipe.bottom):
                    run = False

            if bird.y > HEIGHT or bird.y < 0:
                run = False

            win.fill(WHITE)
            bird.draw(win)
            for pipe in pipes:
                pipe.draw(win)
            score_text = font.render(f"Score: {score}", True, BLACK)
            high_score_text = font.render(f"High Score: {high_score}", True, BLACK)
            win.blit(score_text, (10, 10))
            win.blit(high_score_text, (10, 50))
            pygame.display.update()

        # Update high score if the current score is higher
        if score > high_score:
            high_score = score

        # Show game over screen
        game_over(win, score, high_score)


if __name__ == "__main__":
    main()


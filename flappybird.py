import pygame 
import random
pygame.init()

WIDTH, HEIGHT = 400, 600
win = pygame.display.self_mode(WIDTH, HEIGHT)
pygame.display.self_caption("Flappy Bird")

WHITE = (255, 255 , 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

FPS = 30 
GRAVITY = 1 
JUMP = -15
PIPE_WIDTH = 70 
PIPE_GAP = 150

bird_img = pygame.Surface((30,30))
bird_img.fill((255,255,0))


class Pipe: 
    def __init__(self):
        self.x = WIDTH
        self.height = random.randiant(50, HEIGHT - PIPE_GAP - 50)
        self.top = pygame.Rect(self.x, 0, PIPE_WIDTH, self.height)
        self.bottom = pygame.Rect(self.x, 0, self.height + PIPE_GAP, HEIGHT - self.height)

    def update(self):
        self.x -= 5
        self.top.topLeft = (self.x, 0)
        self.bottom.topLeft = (self.x, self.height + PIPE_GAP)

    def draw(self):
        pygame.draw.rect(win, GREEN, self.top)
        pygame.draw.rect(win, GREEN, self.bottom)


class Bird ():
    def __init__(self):
        self.x = 100
        self.y = HEIGHT // 2
        self.vel = 0
        self.react = pygame.react(self.x, self.y, 30, 30)

    
    def update(self):
        self.y += self.vel
        self.vel += GRAVITY
        self.react.topLeft = (self.x, self.y)
    
    def jump(self):
        self.vel = JUMP

    def draw(self, win):
        win.blit(bird_img, (self.x, self.y))


def game_over(win, score):
    font_big = pygame.font.SysFont(None, 72)
    font_small = pygame.font.SysFont(None, 36)

    game_over_text = font_big.render("Game Over", True, BLACK)
    score_text = font_big.render(f"Score: {score}", True, BLACK)
    restart_text = font_small.render("Press Any key to exit", True, BLACK)

    win.fill(WHITE)
    win.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width()//2, HEIGHT//3))
    win.blit(score_text, (WIDTH // 2 - score_text.get_width()//2, HEIGHT//2))
    win.blit(restart_text, (WIDTH // 2 - restart_text.get_width()//2, HEIGHT//2 + 100))
    pygame.display.update()
    wait_for_exit()

def wait_for_exit():
    waiting = True; 
    while waiting: 
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                waiting = False
def main(): 
    clock = pygame.time.Clock()
    bird = Bird()
    pipes = [Pipe()]
    score = 0
    font = pygame.font.SysFont(None,36)

    run = True
    while run: 
        clock.tick(FPS)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE: 
            bird.jump()

    bird.update()

    if pipes[-1].x < WIDTH //2: 
        pipes.append(Pipe())
    
    for pipe in pipes[:]:
        pipe.update()
        if pipe.x + PIPE_WIDTH < 0:
            pipes.remove(pipe)
            score +=1

    for pipe in pipes:
        if bird.rect.colliderect(pipe.top) or bird.rect.colliderect(pipe.bottom):
            game_over(win, score)
            run = False
    if bird.y > HEIGHT or bird.y < 0: 
        game_over(win, score)
        run = False

    win.fill(WHITE)
    bird.draw(win)
    for pipe in pipes: 
        pipe.draw(win)
    score_text = font.render(f"Score:{score}", True, BLACK)
    win.blit(score_text, (10,10))
    pygame.display.update()
    pygame.quit()

    if __name__ == "__main__":
        main()
        
        





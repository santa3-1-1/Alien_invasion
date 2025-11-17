import pygame, random
from settings import SCREEN_WIDTH

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, screen, kind="life"):
        super().__init__()
        self.screen = screen
        self.kind = kind
        self.rect = pygame.Rect(0,0,20,20)
        self.rect.x = random.randint(0, SCREEN_WIDTH-20)
        self.rect.y = 0
        self.color = (0,255,0) if kind=="life" else (0,0,255)

    def update(self):
        self.rect.y += 2
        if self.rect.top > self.screen.get_rect().bottom:
            self.kill()

    def blitme(self):
        pygame.draw.rect(self.screen, self.color, self.rect)

import pygame
from settings import BULLET_SPEED

class Bullet(pygame.sprite.Sprite):
    def __init__(self, screen, ship, offset=0):
        super().__init__()
        self.screen = screen
        self.rect = pygame.Rect(0,0,3,15)
        self.rect.midtop = ship.rect.midtop
        self.rect.x += offset
        self.color = (255,255,0)
        self.speed = BULLET_SPEED

    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()

    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)

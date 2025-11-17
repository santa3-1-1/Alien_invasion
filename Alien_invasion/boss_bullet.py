import pygame
from settings import BULLET_SPEED

class BossBullet(pygame.sprite.Sprite):
    def __init__(self, screen, boss):
        super().__init__()
        self.screen = screen
        self.rect = pygame.Rect(0,0,5,15)
        self.rect.midtop = boss.rect.midbottom
        self.color = (255,0,0)
        self.speed = BULLET_SPEED - 2

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > self.screen.get_rect().bottom:
            self.kill()

    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)

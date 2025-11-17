import pygame
from settings import SHIP_SPEED, SHIP_IMAGE

SHIP_SCALE = (60, 48)  # 飞船大小，可调

class Ship:
    def __init__(self, screen):
        self.screen = screen
        img = pygame.image.load(SHIP_IMAGE).convert_alpha()
        self.image = pygame.transform.scale(img, SHIP_SCALE)
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.rect.midbottom = self.screen_rect.midbottom
        self.speed = SHIP_SPEED
        self.moving_right = False
        self.moving_left = False
        self.lives = 3

    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.rect.x += self.speed
        if self.moving_left and self.rect.left > 0:
            self.rect.x -= self.speed

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def reset_position(self):
        self.rect.midbottom = self.screen_rect.midbottom

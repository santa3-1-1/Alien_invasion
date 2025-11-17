import pygame
import random
from alien import Alien

class Fleet:
    def __init__(self, screen):
        self.screen = screen
        self.aliens = pygame.sprite.Group()
        self.speed = 2  # 水平移动速度
        self.down_speed = 2  # 每帧下移像素
        self.down_remaining = 0  # 剩余下移像素
        self.create_fleet()

    def create_fleet(self):
        self.aliens.empty()
        for row in range(3):
            for col in range(6):
                alien = Alien(self.screen, 60 + col*100, 50 + row*60)
                self.aliens.add(alien)

    def update(self):
        move_down = False
        for alien in self.aliens:
            alien.rect.x += self.speed
            if alien.rect.right >= self.screen.get_rect().right or alien.rect.left <= 0:
                move_down = True

        if move_down:
            self.speed *= -1
            self.down_remaining += 10  # 累积下移像素

        # 平滑下移
        if self.down_remaining > 0:
            step = min(self.down_speed, self.down_remaining)
            for alien in self.aliens:
                alien.rect.y += step
            self.down_remaining -= step

    def draw(self):
        for alien in self.aliens:
            alien.blitme()

    def check_bullet_collision(self, bullets):
        collisions = pygame.sprite.groupcollide(self.aliens, bullets, True, True)
        return len(collisions)

    def check_ship_collision(self, ship):
        for alien in self.aliens:
            if alien.rect.colliderect(ship.rect):
                return True
        return False

    def check_bottom(self):
        """检查是否有小兵触及屏幕底部"""
        for alien in self.aliens:
            if alien.rect.bottom >= self.screen.get_rect().bottom:
                return True
        return False

import pygame
import cv2
import os


class Alien(pygame.sprite.Sprite):
    def __init__(self, screen, x, y):
        super().__init__()
        self.screen = screen
        self.x = x
        self.y = y
        self.width = 50
        self.height = 50

        # 视频初始化
        video_path = os.path.join("videos", "alien_dance.mp4")
        self.cap = cv2.VideoCapture(video_path)
        if not self.cap.isOpened():
            print(f"Error: Cannot open video {video_path}")
            # 备用：创建默认图像
            self.image = pygame.Surface((self.width, self.height))
            self.image.fill((255, 0, 0))
        else:
            self.frame_surface = None
            self.update_frame()
            self.image = self.frame_surface if self.frame_surface else pygame.Surface((self.width, self.height))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update_frame(self):
        """更新视频帧"""
        ret, frame = self.cap.read()
        if not ret:
            # 视频结束，循环播放
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = self.cap.read()
            if not ret:
                return

        # 转 BGR → RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (self.width, self.height))
        # 转成 pygame surface
        self.frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
        self.image = self.frame_surface

    def blitme(self):
        """绘制外星人 - 兼容你现有的fleet.py"""
        self.update_frame()  # 每帧更新视频
        if self.frame_surface:
            self.screen.blit(self.frame_surface, (self.rect.x, self.rect.y))
        else:
            # 备用绘制
            pygame.draw.rect(self.screen, (255, 0, 0), self.rect)

    def move(self, dx, dy):
        """移动方法 - 保持兼容"""
        self.rect.x += dx
        self.rect.y += dy
import pygame
import cv2
import os
from settings import SCREEN_WIDTH, SCREEN_HEIGHT  # 导入屏幕尺寸

BOSS_SCALE = (120, 100)  # 稍微调整Boss尺寸，适应屏幕


class Boss(pygame.sprite.Sprite):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        self.screen_width = SCREEN_WIDTH  # 800
        self.screen_height = SCREEN_HEIGHT  # 600
        self.width, self.height = BOSS_SCALE

        # 视频初始化
        video_path = os.path.join("videos", "boss_dance.mp4")
        self.cap = cv2.VideoCapture(video_path)
        if not self.cap.isOpened():
            print(f"Error: Cannot open boss video {video_path}")
            self.image = pygame.Surface(BOSS_SCALE)
            self.image.fill((255, 0, 255))  # 洋红色备用
        else:
            self.frame_surface = None
            self.update_frame()
            self.image = self.frame_surface if self.frame_surface else pygame.Surface(BOSS_SCALE)

        self.rect = self.image.get_rect()
        # 确保Boss在屏幕水平居中，且离顶部有足够距离
        self.rect.midtop = (self.screen_width // 2, 60)
        self.hp = 20
        self.last_approach_time = pygame.time.get_ticks()  # 上次向下移动时间
        self.approach_interval = 2000  # 每 2 秒向下移动一次
        self.approach_amount = 15  # 每次下移 15 像素
        self.speed = 3  # 根据屏幕尺寸调整速度

    def update_frame(self):
        """更新Boss视频帧"""
        ret, frame = self.cap.read()
        if not ret:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = self.cap.read()
            if not ret:
                return

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (self.width, self.height))
        self.frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
        self.image = self.frame_surface

    def update(self):
        """更新位置和视频帧，确保在屏幕范围内"""
        # 移动
        self.rect.x += self.speed

        # 精确的边界检测，考虑Boss自身宽度
        if self.rect.right >= self.screen_width:
            self.speed = -abs(self.speed)  # 向左移动
            self.rect.right = self.screen_width - 1  # 确保不超出
        elif self.rect.left <= 0:
            self.speed = abs(self.speed)  # 向右移动
            self.rect.left = 1  # 确保不超出

        # 更新视频帧
        self.update_frame()



    def blitme(self):
        """绘制Boss和血条"""
        self.screen.blit(self.image, self.rect)

        # 血条
        bar_width = self.rect.width
        bar_height = 6
        fill_width = int(bar_width * self.hp / 20)
        # 血条背景（红色）
        pygame.draw.rect(self.screen, (255, 0, 0),
                         (self.rect.left, self.rect.top - 15, bar_width, bar_height))
        # 当前血量（绿色）
        pygame.draw.rect(self.screen, (0, 255, 0),
                         (self.rect.left, self.rect.top - 15, fill_width, bar_height))
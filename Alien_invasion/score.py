import pygame
import os

class Score:
    def __init__(self, screen):
        self.screen = screen
        self.points = 0
        self.high_score = 0
        self.font = pygame.font.SysFont(None, 36)

        self.load_high_score()

    def load_high_score(self):
        """从文件加载最高分（返回最高分供 UI 显示）"""
        try:
            if os.path.exists("high_score.txt"):
                with open("high_score.txt", "r") as f:
                    content = f.read().strip()
                    self.high_score = int(content) if content else 0
            else:
                self.high_score = 0

            print(f"[DEBUG] 加载最高分: {self.high_score}")
        except:
            print("[DEBUG] high_score.txt 读取失败，自动设为 0")
            self.high_score = 0

        return self.high_score

    def save_high_score(self):
        """保存最高分到 high_score.txt"""
        try:
            with open("high_score.txt", "w") as f:
                f.write(str(self.high_score))
            print(f"[DEBUG] 保存最高分: {self.high_score}")
        except:
            print("[DEBUG] 保存最高分失败！")

    def add_points(self, pts):
        """增加分数，并检查是否打破记录"""
        self.points += pts
        if self.points > self.high_score:
            self.high_score = self.points
            print(f"[DEBUG] 新最高分: {self.high_score}")

    def reset(self):
        """重置当前分数，但保留最高分"""
        self.points = 0

    def show_score(self, ship, level):
        text = f"Score: {self.points}  High: {self.high_score}  Lives: {ship.lives}  Level: {level}"
        img = self.font.render(text, True, (0,0,0))
        self.screen.blit(img, (10, 10))

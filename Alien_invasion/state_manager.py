# state_manager.py
import pygame
from collections import deque

class GameStateManager:
    """
    负责管理游戏不同的 screen/state
    使用 push/pop stack 方式以便支持临时弹层（暂停、对话框）
    """
    def __init__(self):
        self.stack = deque()

    def push(self, screen):
        # screen: ScreenBase 实例
        if self.stack:
            try:
                self.stack[-1].on_exit()
            except Exception:
                pass
        self.stack.append(screen)
        try:
            screen.on_enter()
        except Exception as e:
            print("Error on_enter:", e)

    def pop(self):
        if not self.stack:
            return
        top = self.stack.pop()
        try:
            top.on_exit()
        except Exception:
            pass
        if self.stack:
            try:
                self.stack[-1].on_enter()
            except Exception:
                pass

    def replace(self, screen):
        while self.stack:
            try:
                s = self.stack.pop()
                s.on_exit()
            except Exception:
                pass
        self.push(screen)

    def current(self):
        return self.stack[-1] if self.stack else None

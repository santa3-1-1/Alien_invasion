# ui.py
# Pygame 原生 UI 组件（简单按钮、输入框、屏幕管理和过渡效果）
import pygame
import time
from typing import Callable, Tuple

pygame.font.init()

DEFAULT_FONT = pygame.font.SysFont("arial", 20)

class Button:
    def __init__(self, rect: pygame.Rect, text: str, on_click: Callable, font=None):
        self.rect = rect
        self.text = text
        self.on_click = on_click
        self.font = font or DEFAULT_FONT
        self.hovered = False
        self.enabled = True
        self.hover_scale = 1.04
        self._last_hover = False
        # styles
        self.bg = (230, 230, 230)
        self.fg = (30, 30, 30)
        self.border = (180, 180, 180)
        self.radius = 6

    def handle_event(self, event):
        if not self.enabled:
            return
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                try:
                    self.on_click()
                except Exception as e:
                    print("Button callback error:", e)

    def update(self):
        pos = pygame.mouse.get_pos()
        self.hovered = self.rect.collidepoint(pos)

    def draw(self, surface):
        r = self.rect.copy()
        if self.hovered:
            # hover scale effect
            cx, cy = r.center
            r.inflate_ip(int(r.width*(self.hover_scale-1)), int(r.height*(self.hover_scale-1)))
            r.center = (cx, cy)
        pygame.draw.rect(surface, self.bg, r, border_radius=self.radius)
        pygame.draw.rect(surface, self.border, r, width=2, border_radius=self.radius)
        txt = self.font.render(self.text, True, self.fg)
        txt_rect = txt.get_rect(center=r.center)
        surface.blit(txt, txt_rect)

class InputBox:
    def __init__(self, rect: pygame.Rect, text="", font=None, maxlen=20, placeholder=""):
        self.rect = rect
        self.text = text
        self.font = font or DEFAULT_FONT
        self.active = False
        self.maxlen = maxlen
        self.placeholder = placeholder
        self.cursor_visible = True
        self.cursor_ms = 0
        self.cursor_period = 500

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        if self.active and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_RETURN:
                self.active = False
            else:
                if len(self.text) < self.maxlen and event.unicode.isprintable():
                    self.text += event.unicode

    def update(self, dt):
        self.cursor_ms += dt
        if self.cursor_ms >= self.cursor_period:
            self.cursor_visible = not self.cursor_visible
            self.cursor_ms %= self.cursor_period

    def draw(self, surface):
        pygame.draw.rect(surface, (255,255,255), self.rect)
        pygame.draw.rect(surface, (200,200,200), self.rect, 2)
        txt = self.text if self.text else self.placeholder
        color = (0,0,0) if self.text else (150,150,150)
        r = self.font.render(txt, True, color)
        surface.blit(r, (self.rect.x+8, self.rect.y+6))
        if self.active and self.cursor_visible:
            cursor_x = self.rect.x + 8 + r.get_width() + 2
            pygame.draw.rect(surface, (0,0,0), (cursor_x, self.rect.y+8, 2, self.rect.height-16))

class ScreenBase:
    def __init__(self, game):
        self.game = game
        self.surface = game.screen
        self.width, self.height = self.surface.get_size()
        self.elements = []

    def on_enter(self, **kwargs):
        # override
        pass

    def on_exit(self):
        # override
        pass

    def handle_event(self, event):
        for e in list(self.elements):
            if hasattr(e, "handle_event"):
                e.handle_event(event)

    def update(self, dt):
        for e in list(self.elements):
            if hasattr(e, "update"):
                e.update(dt)

    def draw(self):
        # override
        pass

# Simple fade transition function
def fade(surface, color=(255,255,255), duration=300):
    overlay = pygame.Surface(surface.get_size())
    overlay.fill(color)
    clock = pygame.time.Clock()
    start = pygame.time.get_ticks()
    while True:
        elapsed = pygame.time.get_ticks() - start
        if elapsed >= duration:
            break
        alpha = int(255 * (elapsed / duration))
        overlay.set_alpha(alpha)
        surface.blit(overlay, (0,0))
        pygame.display.flip()
        clock.tick(60)

# Specific screens will be created in main or imported, but helper functions here help.

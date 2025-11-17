import sys, random, json, pygame
from settings import *
from ship import Ship
from bullet import Bullet
from boss_bullet import BossBullet
from fleet import Fleet
from boss import Boss
from powerup import PowerUp
from score import Score

def safe_quit(score_obj=None):
    if score_obj is not None:
        try:
            score_obj.save_high_score()
        except:
            pass

    pygame.quit()
    sys.exit()

# ======================================================
#           基础 UI 绘制
# ======================================================
def draw_text(screen, text, size, x, y, color=(0,0,0), center=True):
    font = pygame.font.SysFont("Arial", size)
    surf = font.render(text, True, color)
    rect = surf.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    screen.blit(surf, rect)


def draw_button(screen, text, rect, hover, font_size=40):
    color = (180,180,180) if not hover else (120,120,120)
    pygame.draw.rect(screen, color, rect, border_radius=10)
    draw_text(screen, text, font_size, rect.centerx, rect.centery)


# ======================================================
#               界面状态
# ======================================================
class GameState:
    MENU = "menu"
    PLAYING = "playing"
    PAUSE = "pause"
    GAME_OVER = "game_over"


class GameStateManager:
    def __init__(self):
        self.state = GameState.MENU
        self.final_score = 0

    def change(self, new_state):
        self.state = new_state

# ======================================================
#               关卡管理类
# ======================================================
class StageType:
    NORMAL = "normal"
    BOSS = "boss"

class GameLevel:
    def __init__(self, start_level=1):
        self.current_level = start_level
        self.stage_type = StageType.NORMAL  # NORMAL 或 BOSS

    def next_level(self):
        self.current_level += 1
        # 每3关是Boss关
        if self.current_level % 3 == 0:
            self.stage_type = StageType.BOSS
        else:
            self.stage_type = StageType.NORMAL

    def is_boss_stage(self):
        return self.stage_type == StageType.BOSS

# ======================================================
#               主菜单界面
# ======================================================
def main_menu(screen, gsm):
    while gsm.state == GameState.MENU:
        screen.fill((255,255,255))

        draw_text(screen, "Alien Invasion", 60, SCREEN_WIDTH//2, 150)
        draw_text(screen, "Main Menu", 40, SCREEN_WIDTH//2, 230)

        start_rect = pygame.Rect(450, 300, 300, 60)
        score_rect = pygame.Rect(450, 380, 300, 60)
        quit_rect = pygame.Rect(450, 460, 300, 60)

        mouse_pos = pygame.mouse.get_pos()

        draw_button(screen, "Start Game", start_rect, start_rect.collidepoint(mouse_pos))
        draw_button(screen, "High Score", score_rect, score_rect.collidepoint(mouse_pos))
        draw_button(screen, "Quit", quit_rect, quit_rect.collidepoint(mouse_pos))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                safe_quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_rect.collidepoint(event.pos):
                    gsm.change(GameState.PLAYING)
                    return
                if score_rect.collidepoint(event.pos):
                    show_high_scores(screen)
                if quit_rect.collidepoint(event.pos):
                    safe_quit()


# ======================================================
#               显示最高分
# ======================================================
def show_high_scores(screen):
    score_obj = Score(screen)
    high = score_obj.load_high_score()

    while True:
        screen.fill((255,255,255))
        draw_text(screen, "High Score", 60, SCREEN_WIDTH//2, 150)
        draw_text(screen, f"Top Score: {high}", 40, SCREEN_WIDTH//2, 260)

        back_rect = pygame.Rect(450, 420, 300, 60)
        draw_button(screen, "Back", back_rect, back_rect.collidepoint(pygame.mouse.get_pos()))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                safe_quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_rect.collidepoint(event.pos):
                    return


# ======================================================
#               暂停界面（游戏中按 P）
# ======================================================
def pause_screen(screen, gsm):
    clock = pygame.time.Clock()
    while gsm.state == GameState.PAUSE:
        screen.fill((255, 255, 255))
        draw_text(screen, "Paused", 60, SCREEN_WIDTH // 2, 200)

        resume_rect = pygame.Rect(450, 350, 300, 60)
        menu_rect = pygame.Rect(450, 430, 300, 60)
        mouse_pos = pygame.mouse.get_pos()

        draw_button(screen, "Resume", resume_rect, resume_rect.collidepoint(mouse_pos))
        draw_button(screen, "Main Menu", menu_rect, menu_rect.collidepoint(mouse_pos))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                safe_quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:  # 按 P 也可 Resume
                    gsm.change(GameState.PLAYING)
                    return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if resume_rect.collidepoint(event.pos):
                    gsm.change(GameState.PLAYING)
                    return
                elif menu_rect.collidepoint(event.pos):
                    gsm.change(GameState.MENU)
                    return

        clock.tick(FPS)


# ======================================================
#               游戏结束界面
# ======================================================
def game_over_screen(screen, gsm):
    while gsm.state == GameState.GAME_OVER:
        screen.fill((255,255,255))
        draw_text(screen, "Game Over", 60, SCREEN_WIDTH//2, 200)
        draw_text(screen, f"Score: {gsm.final_score}", 40, SCREEN_WIDTH//2, 300)

        menu_rect = pygame.Rect(450, 420, 300, 60)
        draw_button(screen, "Main Menu", menu_rect, menu_rect.collidepoint(pygame.mouse.get_pos()))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                safe_quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if menu_rect.collidepoint(event.pos):
                    gsm.change(GameState.MENU)
                    return


# ======================================================
#               游戏主循环（完全不动你的逻辑）
# ======================================================
def run_gameplay(screen, gsm):
    ship = Ship(screen)
    bullets = pygame.sprite.Group()
    boss_bullets = pygame.sprite.Group()
    fleet = Fleet(screen)
    score = Score(screen)

    level_mgr = GameLevel(START_LEVEL)  # 关卡管理
    clock = pygame.time.Clock()

    boss_group = pygame.sprite.Group()
    powerups = pygame.sprite.Group()
    double_bullet_active = False
    double_bullet_end_time = 0

    pygame.mixer.init()
    pygame.mixer.music.load(BG_MUSIC)
    pygame.mixer.music.play(-1)
    shoot_sound = pygame.mixer.Sound(BULLET_SOUND)
    alien_hit_sound = pygame.mixer.Sound(ALIEN_HIT_SOUND)
    ship_hit_sound = pygame.mixer.Sound(SHIP_HIT_SOUND)

    last_boss_fire_time = pygame.time.get_ticks()
    boss_appear_time = 0  # 记录Boss出现时间
    pause_cooldown = 0    # 防止P键每帧重复触发

    while True:
        current_time = pygame.time.get_ticks()
        keys = pygame.key.get_pressed()

        # =====================================
        # P键暂停/恢复（实时检测 + 冷却）
        # =====================================
        if keys[pygame.K_p] and current_time > pause_cooldown:
            if gsm.state == GameState.PLAYING:
                gsm.change(GameState.PAUSE)
            elif gsm.state == GameState.PAUSE:
                gsm.change(GameState.PLAYING)
            pause_cooldown = current_time + 300  # 300ms 冷却

        # 退出事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                score.save_high_score()
                safe_quit()
            elif event.type == pygame.KEYDOWN:
                # 空格发射子弹
                if event.key == pygame.K_SPACE:
                    if double_bullet_active:
                        bullets.add(Bullet(screen, ship, offset=-10))
                        bullets.add(Bullet(screen, ship, offset=10))
                    else:
                        bullets.add(Bullet(screen, ship))
                    shoot_sound.play()

        # =====================================
        # 游戏逻辑
        # =====================================
        if gsm.state == GameState.PLAYING:
            # 左右移动
            ship.moving_right = keys[pygame.K_RIGHT]
            ship.moving_left = keys[pygame.K_LEFT]

            ship.update()
            bullets.update()
            boss_bullets.update()
            fleet.update()
            boss_group.update()
            powerups.update()

            # 小兵碰撞
            hits = fleet.check_bullet_collision(bullets)
            if hits:
                score.add_points(hits)
                alien_hit_sound.play()
                for _ in range(hits):
                    if random.random() < POWERUP_DROP_CHANCE:
                        powerup = PowerUp(screen, random.choice(["life", "double_bullet"]))
                        powerup.rect.x = random.randint(0, SCREEN_WIDTH - 20)
                        powerup.rect.y = 0
                        powerups.add(powerup)

            # Boss碰撞
            for boss in boss_group.copy():
                if pygame.sprite.spritecollide(boss, bullets, True):
                    boss.hp -= 1
                    alien_hit_sound.play()
                    score.add_points(5)
                    if boss.hp <= 0:
                        boss_group.remove(boss)

            # 船碰撞
            if fleet.check_ship_collision(ship):
                ship.lives -= 1
                ship_hit_sound.play()
                ship.reset_position()
                if ship.lives <= 0:
                    gsm.final_score = score.points
                    score.save_high_score()
                    gsm.change(GameState.GAME_OVER)
                    return

            # 拾取道具
            for p in powerups:
                if ship.rect.colliderect(p.rect):
                    if p.kind == "life":
                        ship.lives += 1
                    elif p.kind == "double_bullet":
                        double_bullet_active = True
                        double_bullet_end_time = current_time + DOUBLE_BULLET_DURATION
                    powerups.remove(p)

            if double_bullet_active and current_time > double_bullet_end_time:
                double_bullet_active = False

            # Boss发射子弹
            if boss_group and current_time - last_boss_fire_time > BOSS_FIRE_INTERVAL:
                for boss in boss_group:
                    boss_bullets.add(BossBullet(screen, boss))
                last_boss_fire_time = current_time

            # 检测Boss子弹碰撞
            for b in boss_bullets.copy():
                if ship.rect.colliderect(b.rect):
                    ship.lives -= 1
                    ship_hit_sound.play()
                    boss_bullets.remove(b)
                    if ship.lives <= 0:
                        gsm.final_score = score.points
                        score.save_high_score()
                        gsm.change(GameState.GAME_OVER)
                        return
                elif b.rect.top > SCREEN_HEIGHT:
                    boss_bullets.remove(b)

            # 关卡管理
            if not fleet.aliens and not boss_group:
                level_mgr.next_level()
                fleet.speed *= ALIEN_SPEEDUP_FACTOR
                fleet.create_fleet()
                if level_mgr.is_boss_stage():
                    boss = Boss(screen)
                    boss_group.add(boss)
                    boss_appear_time = pygame.time.get_ticks()

            # 小兵触底
            if fleet.check_bottom():
                gsm.final_score = score.points
                score.save_high_score()
                gsm.change(GameState.GAME_OVER)
                return
        # ================= 绘制部分 =================
        screen.fill((255, 255, 255))
        ship.blitme()
        for b in bullets: b.draw_bullet()
        for b in boss_bullets: b.draw_bullet()
        fleet.draw()
        for boss in boss_group: boss.blitme()
        for p in powerups: p.blitme()
        score.show_score(ship, level_mgr.current_level)

        # 永远显示 P 键提示在右下角
        font_small = pygame.font.SysFont("Arial", 24)
        p_hint = font_small.render("Press P to Pause/Resume", True, (0, 0, 0))
        hint_rect = p_hint.get_rect(bottomright=(SCREEN_WIDTH - 10, SCREEN_HEIGHT - 10))
        screen.blit(p_hint, hint_rect)

        # 暂停时显示大提示
        if gsm.state == GameState.PAUSE:
            font = pygame.font.SysFont("Arial", 50)
            pause_text = font.render("Paused - Press P to Resume", True, (255, 0, 0))
            rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(pause_text, rect)

        # Boss 来临提示
        if level_mgr.is_boss_stage() and boss_group and current_time - boss_appear_time < 2000:
            font = pygame.font.SysFont("Arial", 50)
            boss_text = font.render("Boss Incoming!", True, (255, 0, 0))
            rect = boss_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60))
            screen.blit(boss_text, rect)

        pygame.display.flip()
        clock.tick(FPS)





# ======================================================
#                   主入口
# ======================================================
def run_game():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    gsm = GameStateManager()

    while True:
        if gsm.state == GameState.MENU:
            main_menu(screen, gsm)
        elif gsm.state == GameState.PLAYING:
            run_gameplay(screen, gsm)
        elif gsm.state == GameState.PAUSE:
            pause_screen(screen, gsm)
        elif gsm.state == GameState.GAME_OVER:
            game_over_screen(screen, gsm)


if __name__ == "__main__":
    run_game()

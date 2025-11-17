# Alien Invasion 游戏项目

**课程作业提交 | Python 2D 游戏**

## 📂 项目概述

**Alien Invasion** 是一个基于 **Python + Pygame** 的 2D 飞船射击游戏，融合了经典 Space Invaders 元素和 Boss 战设计。玩家需要控制飞船射击外星小兵，并在特定关卡迎战 Boss。项目包含登录系统、UI 界面、分数统计和道具系统。

**特点：**  
- 多关卡设计，每三关出现 Boss。  
- Boss 使用视频播放动画，可左右移动并发射子弹。  
- 飞船支持拾取道具（加生命、双倍子弹）。  
- 飞船支持拾取道具（加生命、双倍子弹）。  
- 暂停与恢复功能，按 `P` 键随时暂停游戏，右下角显示提示。  
- 本地最高分记录，可查看历史最高分。  
- 登录系统（本地 JSON 保存用户信息）。  

---

## 📁 文件结构（2025 最新版）
Alien_invasion/
│
├── images/ # 图片资源
├── sounds/ # 音效资源
├── videos/ # Boss 视频资源
│
├── alien.py
├── auth.py
├── boss.py
├── boss_bullet.py
├── bullet.py
├── fleet.py
├── powerup.py
├── score.py
├── settings.py
├── ship.py
├── state_manager.py
├── ui.py
│
├── main.py # 游戏主入口
├── high_score.txt # 本地最高分记录
└── users.json # 用户数据（登录/注册）

## 🚀 运行游戏

在虚拟环境中执行：

python main.py


游戏启动流程：

显示主菜单（Start Game / High Score / Quit）。

点击 Start Game 进入游戏。

使用 左右箭头 移动飞船。

按 空格键 射击子弹。

按 P 暂停游戏（右下角显示提示）。

击败所有小兵进入下一关，每三关出现 Boss。

飞船碰撞小兵或被 Boss 子弹击中会扣生命，生命为 0 游戏结束。

游戏结束后可返回主菜单，最高分会保存到本地 high_score.txt。

## 🎮 游戏玩法说明
飞船操作

移动： 左右箭头

射击： 空格键

暂停/恢复： P 键（右下角提示）

小兵系统（Fleet）

3×6 固定阵型

小兵左右移动，每次触碰边界整体下降 1 步

被击中消失并有概率掉落道具

Boss 系统

每三关出现

使用视频播放动画，可左右移动

有血条

可发射子弹

道具系统

Life（生命+1）

Double Bullet（双倍子弹）

分数系统

每击中小兵 +1 分

击中 Boss +5 分

显示当前分数、最高分、生命值、关卡

## 🔧 模块说明
模块	功能
main.py	游戏主入口，控制主循环和状态机
alien.py / fleet.py	小兵逻辑、碰撞检测
boss.py / boss_bullet.py	Boss 逻辑、动画和子弹
bullet.py	飞船子弹管理
powerup.py	道具生成和效果
score.py	分数统计和最高分保存
ship.py	玩家飞船逻辑
ui.py	菜单、按钮、暂停/恢复界面
auth.py	用户注册/登录
settings.py	全局参数、屏幕尺寸、速度等
state_manager.py	游戏状态机控制
## ⚠ 注意事项

本地实现：

登录系统仅本地 JSON 存储，不支持在线同步。

Boss 视频需放置在 videos/boss_dance.mp4。

按键提示：

游戏界面右下角始终显示 Press P to Pause，避免玩家忘记暂停操作。

依赖兼容性：

本项目在 Python 3.11+ 测试通过，其他版本可能需要调整依赖版本。


## ⚙ 环境依赖（无需单独 requirements 文件）

本项目使用 **Python 3.11+**，推荐使用虚拟环境 `alien_env` 以隔离依赖。  
依赖库及版本如下（均可直接安装，无需额外文件）：

```bash
# 建议使用虚拟环境
python -m venv alien_env
# 激活虚拟环境
# Windows:
alien_env\Scripts\activate
# macOS / Linux:
source alien_env/bin/activate

# 安装依赖
pip install pygame==2.6.1 numpy==2.2.6 opencv-python==4.12.0.88 pillow==11.3.0 \
moviepy==2.2.1 imageio-ffmpeg==0.6.0 colorama==0.4.6 decorator==5.2.1 \
python-dotenv==1.2.1 tqdm==4.67.1 ImageIO==2.37.2 proglog==0.1.12

#⚠ 注意：依赖版本已固定，保证项目可直接复现。


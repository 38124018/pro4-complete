"""定数定義"""
import os

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
FPS = 60

PLAYER_SIZE = (40, 20)
PLAYER_SPEED = 6
PLAYER_Y = SCREEN_HEIGHT - 60

BULLET_SIZE = (4, 14)
BULLET_SPEED = 10

ENEMY_SIZE = (32, 22)
ENEMY_SPEED = 2
ENEMY_SPAWN_INTERVAL = 45  # フレーム数
ENEMY_SCORE = 100

NAME_MAX_LEN = 10
HIGH_SCORE_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "data", "high_scores.json",
)
MAX_HIGH_SCORES = 5

WHITE = (240, 240, 240)
BLACK = (10, 10, 15)
RED = (220, 70, 70)
BLUE = (80, 140, 230)
GREEN = (90, 200, 120)
GRAY = (150, 150, 150)
YELLOW = (230, 200, 80)

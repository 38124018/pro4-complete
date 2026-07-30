"""<<entity>> クラス群: Player / PlayerCharacter / Bullet / Enemy / Score"""
from __future__ import annotations
import json
import os
import pygame

from .constants import (
    PLAYER_SIZE, PLAYER_SPEED, BULLET_SIZE, BULLET_SPEED,
    ENEMY_SIZE, ENEMY_SPEED, SCREEN_WIDTH, SCREEN_HEIGHT,
    HIGH_SCORE_FILE, MAX_HIGH_SCORES,
    WHITE, RED, BLUE, YELLOW,
)


class Player:
    """<<entity>> プレイヤー: プレイヤー名を保持する"""

    def __init__(self) -> None:
        self._name: str = ""

    def save_name(self, name: str) -> None:
        self._name = name

    @property
    def name(self) -> str:
        return self._name


class PlayerCharacter:
    """<<entity>> プレイヤーキャラクタ: 自機の位置を管理する"""

    def __init__(self, x: int, y: int) -> None:
        self._rect = pygame.Rect(x, y, *PLAYER_SIZE)
        self._speed = PLAYER_SPEED

    @property
    def rect(self) -> pygame.Rect:
        return self._rect

    def is_at_right_edge(self) -> bool:
        return self._rect.right >= SCREEN_WIDTH

    def is_at_left_edge(self) -> bool:
        return self._rect.left <= 0

    def move_right(self) -> None:
        self._rect.x = min(self._rect.x + self._speed, SCREEN_WIDTH - self._rect.width)

    def move_left(self) -> None:
        self._rect.x = max(self._rect.x - self._speed, 0)

    def update_position(self, direction: str) -> None:
        if direction == "right":
            self.move_right()
        elif direction == "left":
            self.move_left()

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.polygon(
            surface, BLUE,
            [(self._rect.centerx, self._rect.top),
             (self._rect.left, self._rect.bottom),
             (self._rect.right, self._rect.bottom)],
        )


class Bullet:
    """<<entity>> 弾"""

    def __init__(self, x: int, y: int) -> None:
        self._rect = pygame.Rect(x, y, *BULLET_SIZE)
        self._speed = BULLET_SPEED
        self._alive = True

    @property
    def rect(self) -> pygame.Rect:
        return self._rect

    @property
    def alive(self) -> bool:
        return self._alive

    def move_forward(self) -> None:
        self._rect.y -= self._speed

    def is_off_screen(self) -> bool:
        return self._rect.bottom < 0

    def destroy(self) -> None:
        self._alive = False

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, YELLOW, self._rect)


class Enemy:
    """<<entity>> 敵"""

    def __init__(self, x: int, y: int) -> None:
        self._rect = pygame.Rect(x, y, *ENEMY_SIZE)
        self._speed = ENEMY_SPEED
        self._alive = True

    @property
    def rect(self) -> pygame.Rect:
        return self._rect

    @property
    def alive(self) -> bool:
        return self._alive

    def move_down(self) -> None:
        self._rect.y += self._speed

    def is_off_screen(self) -> bool:
        return self._rect.top > SCREEN_HEIGHT

    def destroy(self) -> None:
        self._alive = False

    def is_hit(self, bullet: Bullet) -> bool:
        return self._rect.colliderect(bullet.rect)

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, RED, self._rect)


class Score:
    """<<entity>> スコア"""

    def __init__(self) -> None:
        self._point = 0

    def add_point(self, point: int) -> None:
        self._point += point

    def get_point(self) -> int:
        return self._point


# ---------------------------------------------------------------------------
# ハイスコア永続化（ファイル入出力。設計モデルの Score を拡張して利用）
# ---------------------------------------------------------------------------
def load_high_scores() -> list[dict]:
    if not os.path.exists(HIGH_SCORE_FILE):
        return []
    try:
        with open(HIGH_SCORE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return []


def save_high_score(name: str, point: int) -> list[dict]:
    scores = load_high_scores()
    scores.append({"name": name, "point": point})
    scores.sort(key=lambda s: s["point"], reverse=True)
    scores = scores[:MAX_HIGH_SCORES]
    try:
        os.makedirs(os.path.dirname(HIGH_SCORE_FILE), exist_ok=True)
        with open(HIGH_SCORE_FILE, "w", encoding="utf-8") as f:
            json.dump(scores, f, ensure_ascii=False, indent=2)
    except OSError:
        pass
    return scores

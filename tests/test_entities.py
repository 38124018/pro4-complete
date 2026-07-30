"""entity クラスの単体テスト（pytest）"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import pygame
pygame.init()

from shooting_game.entities import PlayerCharacter, Bullet, Enemy
from shooting_game.constants import SCREEN_WIDTH, SCREEN_HEIGHT


def test_player_character_stops_at_right_edge():
    pc = PlayerCharacter(SCREEN_WIDTH - 40, 400)
    assert pc.is_at_right_edge() is True
    before = pc.rect.x
    pc.move_right()
    # is_at_right_edge()はMovementControl側でチェックする想定のため、
    # move_right()単体は右端を超えない範囲でクランプされることを確認する。
    assert pc.rect.right <= SCREEN_WIDTH
    assert pc.rect.x >= before


def test_player_character_stops_at_left_edge():
    pc = PlayerCharacter(0, 400)
    assert pc.is_at_left_edge() is True
    pc.move_left()
    assert pc.rect.left >= 0


def test_bullet_off_screen():
    bullet = Bullet(100, 5)
    for _ in range(10):
        bullet.move_forward()
    assert bullet.is_off_screen() is True


def test_enemy_is_hit_by_overlapping_bullet():
    enemy = Enemy(100, 100)
    bullet = Bullet(105, 105)
    assert enemy.is_hit(bullet) is True


def test_enemy_not_hit_by_far_bullet():
    enemy = Enemy(100, 100)
    bullet = Bullet(500, 400)
    assert enemy.is_hit(bullet) is False

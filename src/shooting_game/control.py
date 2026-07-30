"""<<control>> クラス群"""
from __future__ import annotations

from .constants import NAME_MAX_LEN, ENEMY_SCORE
from .entities import Player, PlayerCharacter, Bullet, Enemy, Score, load_high_scores


class NameInputControl:
    """<<control>> 名前入力管理"""

    def __init__(self, player: Player) -> None:
        self._player = player

    def confirm_input(self, player_name: str) -> bool:
        return 0 < len(player_name) <= NAME_MAX_LEN

    def save_player_name(self, player_name: str) -> None:
        self._player.save_name(player_name)


class MovementControl:
    """<<control>> 移動管理"""

    def __init__(self, character: PlayerCharacter) -> None:
        self._character = character

    def move_right(self) -> None:
        if not self._character.is_at_right_edge():
            self._character.move_right()

    def move_left(self) -> None:
        if not self._character.is_at_left_edge():
            self._character.move_left()


class BulletControl:
    """<<control>> 弾発射管理"""

    def __init__(self, score: Score) -> None:
        self._score = score
        self._bullets: list[Bullet] = []

    @property
    def bullets(self) -> list[Bullet]:
        return self._bullets

    def fire_bullet(self, x: int, y: int) -> None:
        self._bullets.append(Bullet(x, y))

    def update(self, enemies: list[Enemy]) -> None:
        for bullet in self._bullets:
            bullet.move_forward()
            if bullet.is_off_screen():
                bullet.destroy()
                continue
            for enemy in enemies:
                if enemy.alive and enemy.is_hit(bullet):
                    enemy.destroy()
                    bullet.destroy()
                    self._score.add_point(ENEMY_SCORE)
                    break
        self._bullets = [b for b in self._bullets if b.alive]


class HighScoreControl:
    """<<control>> ハイスコア管理"""

    def __init__(self, score: Score) -> None:
        self._score = score

    def execute_show_high_score(self) -> list[dict]:
        return load_high_scores()

    def show_high_score_screen(self) -> None:
        pass  # 実際の描画はGameApp側でHighScoreScreen.show()を呼び出す


class GameStartControl:
    """<<control>> ゲーム開始管理"""

    def execute_game_start(self) -> None:
        pass  # ゲーム状態（自機・弾・スコア等）の初期化はGameApp._reset_game_entities()が行う

    def show_game_screen(self) -> None:
        pass  # 実際の描画はメインループでGameScreen.show()が継続的に行う


class RetryControl:
    """<<control>> リトライ管理"""

    def execute_retry(self) -> None:
        pass  # スコアの記録・状態のリセットはGameAppが行う

    def show_title_screen(self) -> None:
        pass  # 実際の描画はメインループでTitleScreen.show()が行う


class TitleReturnControl:
    """<<control>> タイトル画面復帰管理"""

    def execute_return_to_title(self) -> None:
        pass  # 状態遷移そのものはGameAppが行う

    def show_title_screen(self) -> None:
        pass  # 実際の描画はメインループでTitleScreen.show()が行う

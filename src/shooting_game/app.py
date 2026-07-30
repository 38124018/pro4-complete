"""GameApp: 状態遷移とメインループ"""
from __future__ import annotations
import sys
import random
import pygame

from .constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, PLAYER_SIZE, PLAYER_Y,
    BULLET_SIZE, ENEMY_SIZE, ENEMY_SPAWN_INTERVAL, NAME_MAX_LEN,
)
from .entities import Player, PlayerCharacter, Enemy, Score, save_high_score
from .boundary import TitleScreen, NameInputScreen, GameScreen, GameOverScreen, HighScoreScreen
from .control import (
    NameInputControl, MovementControl, BulletControl, HighScoreControl,
    GameStartControl, RetryControl, TitleReturnControl,
)
from .fonts import load_japanese_font


class GameApp:
    STATE_TITLE = "TITLE"
    STATE_NAME_INPUT = "NAME_INPUT"
    STATE_PLAYING = "PLAYING"
    STATE_GAME_OVER = "GAME_OVER"
    STATE_HIGH_SCORE = "HIGH_SCORE"

    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("シューティングゲーム")
        self._screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self._clock = pygame.time.Clock()
        self._font = load_japanese_font(28)
        self._big_font = load_japanese_font(56)

        # boundary
        self._title_screen = TitleScreen(self._screen, self._font, self._big_font)
        self._name_input_screen = NameInputScreen(self._screen, self._font)
        self._game_screen = GameScreen(self._screen, self._font)
        self._game_over_screen = GameOverScreen(self._screen, self._font, self._big_font)
        self._high_score_screen = HighScoreScreen(self._screen, self._font, self._big_font)

        # entity
        self._player = Player()

        self._state = None
        self._name_buffer = ""
        self._high_scores: list[dict] = []

        self._reset_game_entities()
        self._state = self.STATE_TITLE

    def _reset_game_entities(self) -> None:
        self._character = PlayerCharacter(
            SCREEN_WIDTH // 2 - PLAYER_SIZE[0] // 2, PLAYER_Y
        )
        self._score = Score()
        self._movement_control = MovementControl(self._character)
        self._bullet_control = BulletControl(self._score)
        self._enemies: list[Enemy] = []
        self._enemy_spawn_timer = 0

    # -- 各ユースケースに対応する処理 --------------------------------------
    def _handle_title_events(self, events: list[pygame.event.Event]) -> None:
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    # ②ゲームスタートする（名前未入力の場合は先に名前入力へ）
                    game_start_control = GameStartControl()
                    game_start_control.execute_game_start()
                    if self._player.name:
                        self._reset_game_entities()
                        game_start_control.show_game_screen()
                        self._state = self.STATE_PLAYING
                    else:
                        self._name_buffer = ""
                        self._state = self.STATE_NAME_INPUT
                elif e.key == pygame.K_h:
                    # ⑦ハイスコアを表示する
                    high_score_control = HighScoreControl(self._score)
                    self._high_scores = high_score_control.execute_show_high_score()
                    high_score_control.show_high_score_screen()
                    self._state = self.STATE_HIGH_SCORE

    def _handle_name_input_events(self, events: list[pygame.event.Event]) -> None:
        # ①プレイヤー名を入力する
        control = NameInputControl(self._player)
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN:
                    if control.confirm_input(self._name_buffer):
                        control.save_player_name(self._name_buffer)
                        game_start_control = GameStartControl()
                        game_start_control.execute_game_start()
                        self._reset_game_entities()
                        game_start_control.show_game_screen()
                        self._state = self.STATE_PLAYING
                    else:
                        self._name_input_screen.show_error_message(
                            f"1〜{NAME_MAX_LEN}文字以内で入力してください"
                        )
                elif e.key == pygame.K_BACKSPACE:
                    self._name_buffer = self._name_buffer[:-1]
                elif e.unicode and len(self._name_buffer) < NAME_MAX_LEN:
                    self._name_buffer += e.unicode

    def _handle_playing(self, events: list[pygame.event.Event]) -> None:
        for e in events:
            if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
                # ⑤弾を発射する
                self._bullet_control.fire_bullet(
                    self._character.rect.centerx - BULLET_SIZE[0] // 2,
                    self._character.rect.top,
                )

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            # ③右に移動する
            self._movement_control.move_right()
        if keys[pygame.K_LEFT]:
            # ④左に移動する
            self._movement_control.move_left()

        # 敵の生成
        self._enemy_spawn_timer += 1
        if self._enemy_spawn_timer >= ENEMY_SPAWN_INTERVAL:
            self._enemy_spawn_timer = 0
            x = random.randint(0, SCREEN_WIDTH - ENEMY_SIZE[0])
            self._enemies.append(Enemy(x, -ENEMY_SIZE[1]))

        # 弾の更新・当たり判定
        self._bullet_control.update(self._enemies)

        # 敵の移動
        for enemy in self._enemies:
            if enemy.alive:
                enemy.move_down()
                if enemy.rect.colliderect(self._character.rect):
                    self._state = self.STATE_GAME_OVER
        self._enemies = [en for en in self._enemies if en.alive and not en.is_off_screen()]

        self._game_screen.show(self._character, self._bullet_control.bullets,
                                self._enemies, self._score)

    def _handle_game_over_events(self, events: list[pygame.event.Event]) -> None:
        for e in events:
            if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
                # ⑥リトライする
                save_high_score(self._player.name, self._score.get_point())
                retry_control = RetryControl()
                retry_control.execute_retry()
                self._reset_game_entities()
                retry_control.show_title_screen()
                self._state = self.STATE_TITLE

    def _handle_high_score_events(self, events: list[pygame.event.Event]) -> None:
        for e in events:
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                # ⑧タイトル画面に戻る
                title_return_control = TitleReturnControl()
                title_return_control.execute_return_to_title()
                title_return_control.show_title_screen()
                self._state = self.STATE_TITLE

    # -- メインループ --------------------------------------------------------
    def run(self) -> None:
        while True:
            events = pygame.event.get()
            for e in events:
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            if self._state == self.STATE_TITLE:
                self._handle_title_events(events)
                self._title_screen.show()
            elif self._state == self.STATE_NAME_INPUT:
                self._handle_name_input_events(events)
                self._name_input_screen.show(self._name_buffer)
            elif self._state == self.STATE_PLAYING:
                self._handle_playing(events)
            elif self._state == self.STATE_GAME_OVER:
                self._handle_game_over_events(events)
                self._game_over_screen.show(self._score)
            elif self._state == self.STATE_HIGH_SCORE:
                self._handle_high_score_events(events)
                self._high_score_screen.show(self._high_scores)

            self._clock.tick(FPS)

"""<<boundary>> クラス群"""
from __future__ import annotations
import pygame

from .constants import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, RED, GRAY
from .entities import PlayerCharacter, Bullet, Enemy, Score


class TitleScreen:
    """<<boundary>> タイトル画面"""

    def __init__(self, screen: pygame.Surface, font: pygame.font.Font, big_font: pygame.font.Font) -> None:
        self._screen = screen
        self._font = font
        self._big_font = big_font

    def show(self) -> None:
        self._screen.fill(BLACK)
        title = self._big_font.render("SHOOTING GAME", True, WHITE)
        self._screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, 150)))
        opt1 = self._font.render("[SPACE] ゲームスタートを選択する", True, WHITE)
        opt2 = self._font.render("[H] ハイスコアを選択する", True, WHITE)
        self._screen.blit(opt1, opt1.get_rect(center=(SCREEN_WIDTH // 2, 260)))
        self._screen.blit(opt2, opt2.get_rect(center=(SCREEN_WIDTH // 2, 300)))
        pygame.display.flip()


class NameInputScreen:
    """<<boundary>> プレイヤー名入力画面"""

    def __init__(self, screen: pygame.Surface, font: pygame.font.Font) -> None:
        self._screen = screen
        self._font = font
        self._error_message = ""

    def show_error_message(self, message: str) -> None:
        self._error_message = message

    def show(self, current_input: str) -> None:
        self._screen.fill(BLACK)
        label = self._font.render("プレイヤー名を入力してください (Enterで確定)", True, WHITE)
        self._screen.blit(label, label.get_rect(center=(SCREEN_WIDTH // 2, 160)))
        box = pygame.Rect(SCREEN_WIDTH // 2 - 150, 200, 300, 40)
        pygame.draw.rect(self._screen, WHITE, box, 2)
        text = self._font.render(current_input, True, WHITE)
        self._screen.blit(text, (box.x + 8, box.y + 8))
        if self._error_message:
            err = self._font.render(self._error_message, True, RED)
            self._screen.blit(err, err.get_rect(center=(SCREEN_WIDTH // 2, 270)))
        pygame.display.flip()


class GameScreen:
    """<<boundary>> ゲーム画面"""

    def __init__(self, screen: pygame.Surface, font: pygame.font.Font) -> None:
        self._screen = screen
        self._font = font

    def show(self, character: PlayerCharacter, bullets: list[Bullet],
              enemies: list[Enemy], score: Score) -> None:
        self._screen.fill(BLACK)
        character.draw(self._screen)
        for bullet in bullets:
            bullet.draw(self._screen)
        for enemy in enemies:
            if enemy.alive:
                enemy.draw(self._screen)
        score_text = self._font.render(f"SCORE: {score.get_point()}", True, WHITE)
        self._screen.blit(score_text, (10, 10))
        pygame.display.flip()


class GameOverScreen:
    """<<boundary>> ゲームオーバー画面"""

    def __init__(self, screen: pygame.Surface, font: pygame.font.Font, big_font: pygame.font.Font) -> None:
        self._screen = screen
        self._font = font
        self._big_font = big_font

    def show(self, score: Score) -> None:
        self._screen.fill(BLACK)
        title = self._big_font.render("GAME OVER", True, RED)
        self._screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, 160)))
        score_text = self._font.render(f"SCORE: {score.get_point()}", True, WHITE)
        self._screen.blit(score_text, score_text.get_rect(center=(SCREEN_WIDTH // 2, 230)))
        retry_text = self._font.render("[SPACE] リトライを選択する", True, WHITE)
        self._screen.blit(retry_text, retry_text.get_rect(center=(SCREEN_WIDTH // 2, 300)))
        pygame.display.flip()


class HighScoreScreen:
    """<<boundary>> ハイスコア画面"""

    def __init__(self, screen: pygame.Surface, font: pygame.font.Font, big_font: pygame.font.Font) -> None:
        self._screen = screen
        self._font = font
        self._big_font = big_font

    def show(self, scores: list[dict]) -> None:
        self._screen.fill(BLACK)
        title = self._big_font.render("HIGH SCORE", True, WHITE)
        self._screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, 80)))
        if not scores:
            empty = self._font.render("記録がありません", True, GRAY)
            self._screen.blit(empty, empty.get_rect(center=(SCREEN_WIDTH // 2, 200)))
        else:
            for i, s in enumerate(scores):
                line = self._font.render(f"{i + 1}. {s['name']}  {s['point']}", True, WHITE)
                self._screen.blit(line, line.get_rect(center=(SCREEN_WIDTH // 2, 150 + i * 40)))
        back = self._font.render("[ESC] タイトルに戻るを選択する", True, WHITE)
        self._screen.blit(back, back.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 40)))
        pygame.display.flip()

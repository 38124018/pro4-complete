"""日本語フォント読み込みユーティリティ"""
import sys
import pygame


def load_japanese_font(size: int) -> pygame.font.Font:
    """日本語グリフを含むフォントを探して読み込む。
    見つからない場合はデフォルトフォント（日本語は表示されない）にフォールバックする。
    """
    candidates = [
        "notosanscjkjp", "notosanscjkjpregular", "notosansjp",
        "ipagothic", "ipapgothic", "ipaexgothic",
        "hiraginosans", "hiraginokakugothicpron",
        "yugothic", "yugothicmedium", "msgothic", "meiryo",
        "takaogothic", "vlgothic",
    ]
    for name in candidates:
        path = pygame.font.match_font(name)
        if path:
            return pygame.font.Font(path, size)
    print(
        "[警告] 日本語フォントが見つかりませんでした。"
        "日本語が文字化け・空白表示になる場合はOSに日本語フォントを"
        "インストールするか、pygame.font.Font('お手持ちのフォント.ttf', size) で"
        "パスを直接指定してください。",
        file=sys.stderr,
    )
    return pygame.font.SysFont(None, size)

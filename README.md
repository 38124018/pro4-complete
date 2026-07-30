# シューティングゲーム

プログラミング演習 課題6 実装物（Python + pygame）

## フォルダ構成

```
shooting-game/
├── .gitignore
├── README.md
├── requirements.txt
│
├── src/
│   ├── main.py               # エントリーポイント
│   └── shooting_game/
│       ├── __init__.py
│       ├── app.py            # GameApp（状態遷移・メインループ）
│       ├── constants.py      # 画面サイズ・色・速度などの定数
│       ├── entities.py       # Player, PlayerCharacter, Bullet, Enemy, Score
│       ├── boundary.py       # TitleScreen, NameInputScreen, GameScreen, GameOverScreen, HighScoreScreen
│       ├── control.py        # NameInputControl, GameStartControl, MovementControl,
│       │                     # BulletControl, HighScoreControl, RetryControl, TitleReturnControl
│       └── fonts.py          # 日本語フォント読み込みユーティリティ
│
├── tests/
│   └── test_entities.py
│
├── docs/                     # 課題提出物一式
│   ├── 仕様書.docx
│   ├── 概念モデル.docx
│   ├── 分析モデル.docx
│   ├── 詳細設計モデル_課題6.docx
│   ├── 詳細設計モデル_課題6.drawio
│   └── チェックシート.docx
│
└── data/
    └── high_scores.json      # 実行時に自動生成（.gitignore対象）
```

クラスはentity / boundary / control のファイルに分割しており、詳細設計モデルのクラス図の3層構造とそのまま対応している。

## 起動方法

```bash
pip install -r requirements.txt
python src/main.py
```

## 操作方法

| 画面 | キー | 動作 |
|---|---|---|
| タイトル画面 | SPACE | ゲームスタート（名前未登録なら名前入力画面へ） |
| タイトル画面 | H | ハイスコア画面を表示 |
| 名前入力画面 | 文字キー | プレイヤー名を入力（最大10文字） |
| 名前入力画面 | BackSpace | 1文字削除 |
| 名前入力画面 | Enter | 入力を確定してゲーム開始 |
| ゲーム画面 | ← / → | 自機を左右に移動 |
| ゲーム画面 | SPACE | 弾を発射 |
| ゲームオーバー画面 | SPACE | リトライ（タイトル画面に戻る） |
| ハイスコア画面 | ESC | タイトル画面に戻る |

## テスト

```bash
pip install pytest
pytest tests/
```

# ToanTimer for Discord

ToanTimerは、Discord上でタイマーを設定するためのシンプルなアプリケーションです。設定されたショートカットキーを使ってタイマーを開始し、経過時間をDiscordのボイスチャンネルで通知します。ローカル環境での使用も可能です。

## クイックスタート

1. Pythonをインストールする (開発者環境: Python 3.10.6)
2. ffmpegをインストールする
3. python -m venv venv
4. venv\Scripts\activate
5. pip install -r requirements.txt
6. `start.bat`を実行する


## 設定 (config.ini)

### [settings]

- `timer_minutes`: タイマーの分数 (整数)
- `timer_seconds`: タイマーの秒数 (整数)
- `start_hotkey`: ショートカットキー (文字列)
- `use_discord`: Discordの利用またはローカルの利用 (1: Discord, 2: ローカル)

### [discord]

- `token`: Discord botのトークン (文字列)
- `voice_channel`: DiscordのボイスチャンネルID (数値)
- `guild_id`: DiscordのギルドID (数値)

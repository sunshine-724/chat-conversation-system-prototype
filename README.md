# Chat Conversation System Prototype

Next.js（フロントエンド）とFastAPI（バックエンド）を使用した、ローカルLLM向けの雑談対話システムプロトタイプです。
ストリーミング応答とモデル切り替えに対応しています。

## 前提条件

*   **Node.js**: v18以上
*   **Python**: v3.10以上
*   **uv**: Pythonパッケージマネージャー
*   **Ollama**: ローカルLLM実行用（オプション。ない場合はシミュレーションモードで動作します）

## セットアップ

### 1. バックエンド (Python/FastAPI)

`uv` を使用して依存関係をインストールします。

```bash
cd backend
uv sync
```

### 2. フロントエンド (Next.js)

npmを使用して依存関係をインストールします。

```bash
cd frontend
npm install
```

## 起動方法

### バックエンドの起動

```bash
cd backend
uv run uvicorn main:app --reload
```
*   ポート: `8000`
*   APIドキュメント: http://localhost:8000/docs

### フロントエンドの起動

別のターミナルを開いて実行してください。

```bash
cd frontend
npm run dev
```
*   URL: http://localhost:3000

## 機能

*   **リアルタイムチャット**: ユーザー入力に対する応答をストリーミング表示します。
*   **モデル切り替え**: UI右上のドロップダウンから使用するモデル（Qwen, Llamaなど）を選択できます。
*   **シミュレーションモード**: Ollamaが検出されない場合、自動的にエコー応答モードに切り替わり、UIの動作確認が可能です。

## ローカルLLM (Ollama) の使用方法

1.  [Ollama](https://ollama.com/) をインストールして起動します。
2.  使用したいモデルをpullします（例: `ollama pull qwen2.5:32b`）。
3.  `backend/main.py` のコメントアウトされている `ollama.chat` 部分を有効化し、シミュレーション部分を無効化してください。

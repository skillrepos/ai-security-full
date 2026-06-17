#!/usr/bin/env bash
# Installs Ollama and pulls the default lab model. Runs once at Codespace
# creation (postCreateCommand). Safe to re-run.
set -e
MODEL="${OLLAMA_MODEL:-llama3.2:3b}"

if ! command -v ollama >/dev/null 2>&1; then
    echo "[ollama] installing Ollama..."
    curl -fsSL https://ollama.com/install.sh | sh
fi

# Start the server in the background if it isn't already running.
if ! curl -s http://localhost:11434/api/tags >/dev/null 2>&1; then
    echo "[ollama] starting server..."
    nohup ollama serve >/tmp/ollama.log 2>&1 &
    sleep 3
fi

echo "[ollama] pulling model $MODEL (one-time download)..."
ollama pull "$MODEL"
echo "[ollama] ready. Model: $MODEL"

#!/usr/bin/env bash
# Re-attach helper: makes sure the Ollama server is running. Runs on
# postAttachCommand (every time the Codespace resumes) and is safe to run by
# hand if a lab reports it can't reach Ollama.
set -e

if ! command -v ollama >/dev/null 2>&1; then
    echo "[ollama] command not found -- installing dependencies and Ollama..."
    sudo apt-get update
    sudo apt-get install -y zstd
    curl -fsSL https://ollama.com/install.sh | sh
fi

if ! curl -s http://localhost:11434/api/tags >/dev/null 2>&1; then
    echo "[ollama] server not running -- starting it..."
    nohup ollama serve >/tmp/ollama.log 2>&1 &
    sleep 3
fi
echo "[ollama] server is up at http://localhost:11434"

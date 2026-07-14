# Local Setup — macOS (No VS Code)
 
## AI Security for Developers and Practitioners (Full Day)
 
This guide is for **macOS** users who don't have VS Code and don't want to install it. You'll run all 8 labs plus the capstone using the built‑in **Terminal**, **Python**, **Git**, **Ollama**, and any text editor (TextEdit, `nano`, etc.). No Codespaces, no Docker, no VS Code required.
 
Because you're not using VS Code, three things in `labs.md` work a little differently — **paths**, the **`code` view command**, and the **`code -d` diff‑and‑merge step**. This guide sets everything up and then explains exactly how to handle those three differences. Read the **"How the labs differ"** section before you start Lab 1.
 
> Open **Terminal** (Applications → Utilities → Terminal, or Spotlight → "Terminal") for all commands below. Works on both Apple Silicon (M‑series) and Intel Macs.
 
---
 
## 1. Install Homebrew (package manager)
 
The easiest way to install everything else. If you already have Homebrew (`brew --version` works), skip this. Otherwise, paste this into Terminal and follow the prompts:
 
```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
 
After it finishes, it may tell you to run one or two `echo ... >> ~/.zprofile` commands to add `brew` to your PATH — do that, then **open a new Terminal window**. Confirm:
 
```
brew --version
```
 
> Don't want Homebrew? You can install Python from <https://www.python.org/downloads/macos/>, Git via `xcode-select --install`, and Ollama from <https://ollama.com/download>. The rest of the guide is the same.
 
---
 
## 2. Install Python and Git
 
```
brew install python git
```
 
Verify (you may need to use `python3`/`pip3` on macOS rather than `python`/`pip`):
 
```
python3 --version
git --version
```
 
You should see Python 3.1x. **Throughout the labs, use `python3` wherever `labs.md` says `python`** (macOS reserves plain `python`). Inside an activated virtual environment, plain `python` also works — see step 5.
 
---
 
## 3. Install Ollama (the local model runtime)
 
```
brew install ollama
```
 
(Or download the app from <https://ollama.com/download>.) Then start the server and pull the course model:
 
```
ollama serve &
ollama pull llama3.2:3b
```
 
The `&` runs the server in the background in this Terminal. (If you installed the **app**, just launch Ollama from Applications instead — it runs the server for you and you can skip `ollama serve`.) The model download is ~2 GB, one time. Confirm the server is up:
 
```
curl http://localhost:11434/api/tags
```
 
That should return JSON listing your models.
 
---
 
## 4. Get the repository
 
```
cd ~
git clone https://github.com/skillrepos/ai-security-full.git
cd ai-security-full
```
 
**Remember this folder** — it's your repo root, and every lab starts from here. This guide calls it **`<repo>`** (it's `~/ai-security-full`).
 
---
 
## 5. Create and activate the Python virtual environment
 
From the repo root:
 
```
python3 -m venv py_env
source py_env/bin/activate
```
 
Your prompt should now start with `(py_env)`, and inside it plain `python` and `pip` work. Install the lab dependencies:
 
```
pip install -r requirements.txt
```
 
---
 
## 6. Pre‑download the Chroma embedding model (used by Lab 2)
 
This one‑time download makes Lab 2's first run fast. With `(py_env)` active:
 
```
python -c "import chromadb; c=chromadb.Client(); col=c.get_or_create_collection('warmup_kb'); col.add(documents=['warm up'], ids=['1']); print('embedding model ready')"
```
 
You should see `embedding model ready`. (Yellow warnings are fine to ignore.)
 
---
 
## 7. (Optional but recommended) Get and set a free Groq API key
 
A few labs are stronger with Groq's hosted models. Without a key, everything still runs on the local Ollama model.
 
1. Go to <https://console.groq.com>, create an account, then **API Keys → Create API Key**, and **copy the key** (you can't view it again later).
2. Set it. The course's `scripts/setup-key.sh` works in a **bash/zsh terminal**, but it appends to `~/.bashrc`; macOS Terminal uses **zsh** by default, so set the variables directly instead:
**For the current Terminal window only:**
 
```
export AGENT_PROVIDER=groq
export GROQ_API_KEY=your_key_here
```
 
**To persist it for all future Terminal windows**, add those two lines to `~/.zshrc`:
 
```
echo 'export AGENT_PROVIDER=groq' >> ~/.zshrc
echo 'export GROQ_API_KEY=your_key_here' >> ~/.zshrc
```
 
Then open a new Terminal (or run `source ~/.zshrc`) and confirm with `echo $GROQ_API_KEY`.
 
---
 
## 8. Warm up the local model
 
With `(py_env)` active:
 
```
python scripts/warmup_ollama.py
```
 
The first model call in a session is slow (~30–60s) while the model loads; this warms it up so labs feel responsive.
 
---
 
## 9. Open the labs
 
Open `labs.md` in your browser or any Markdown viewer. On GitHub you can read it rendered on the repo page; locally, open the raw file in TextEdit, or use an online Markdown viewer.
 
**You're ready — but first read the next section**, which covers the handful of command changes for a no‑VS‑Code setup.
 
---
 
## How the labs differ without VS Code
 
`labs.md` was written for the Codespaces/VS Code environment. Four small substitutions cover everything; the rest of each lab — every command, prompt, and "look at the output" step — is **identical**. (Remember: use `python3`, or plain `python` inside the activated venv.)
 
### A. Paths: `/workspaces/ai-security-full/...`
 
Some labs write absolute paths like:
 
```
cd /workspaces/ai-security-full/guardrails
```
 
That path only exists in Codespaces. On your Mac, `cd` into the matching folder under **your** repo instead:
 
```
cd <repo>/guardrails
```
 
The labs that use the relative form (`cd ../rag`, `cd ../mcp`, …) work as‑is *if* you run them from the previous lab's folder. When in doubt, go back to the repo root and `cd` into the lab folder by name. The lab folders are: `threat-model`, `rag`, `guardrails`, `agents`, `mcp`, `observability`, `redteam`, `governance`, `deploy`.
 
### B. `code <file>` (just viewing a file)
 
Wherever a lab says something like `code architecture.json` or `code kb.py` to **read** a file, open it in any editor instead:
 
```
open -e architecture.json      # opens in TextEdit
```
 
(Or `cat architecture.json` to print it, or `nano architecture.json`.)
 
### C. `code -d <complete> <skeleton>` (the diff‑and‑merge step)
 
This is the one real workflow change. In VS Code you merge the finished code into a skeleton side‑by‑side. Without VS Code, you'll **review the differences, then copy the complete reference file over the skeleton.** The reference file (in `extra/`) is the full, correct version of the skeleton.
 
**Step 1 — see what you'd be merging** (optional but recommended, so you learn the change). Use `diff`. For example, for Lab 3:
 
```
diff extra/guardrails_complete.txt guardrails/guardrails_demo.py
```
 
Read the differences — they're the guard logic the lab is teaching. (The yellow hover "bubble" comments you'd see in VS Code are described in the lab text itself, so you're not missing the explanations.)
 
> Prefer a side‑by‑side visual diff? macOS ships **FileMerge** (`opendiff`) with the Xcode Command Line Tools: `opendiff extra/guardrails_complete.txt guardrails/guardrails_demo.py`. Or use `diff -y` for a two‑column view in the terminal.
 
**Step 2 — apply the complete version** by copying it over the skeleton:
 
```
cp extra/guardrails_complete.txt guardrails/guardrails_demo.py
```
 
That's it — the skeleton is now the completed file, exactly as if you'd merged every block in VS Code. Then continue the lab (`python guardrails_demo.py`, etc.).
 
**The file pairs for every lab** (reference `.txt` → skeleton you overwrite):
 
| Lab | `diff` / `cp` source (`extra/...`) | Destination skeleton |
|---|---|---|
| Lab 1 – Threat model | `extra/threat_model_complete.txt` | `threat-model/threat_model.py` |
| Lab 2 – RAG hardening | `extra/rag_hardened_complete.txt` | `rag/rag_hardened.py` |
| Lab 3 – Guardrails | `extra/guardrails_complete.txt` | `guardrails/guardrails_demo.py` |
| Lab 4 – Secure agent | `extra/secure_agent_complete.txt` | `agents/secure_agent.py` |
| Lab 5 – MCP server | `extra/secure_server_complete.txt` | `mcp/secure_server.py` |
| Lab 6 – Observability | `extra/observable_agent_complete.txt` | `observability/observable_agent.py` |
| Lab 7 – Red team | `extra/target_agent_complete.txt` | `redteam/target_agent.py` |
| Lab 8 – Governance | `extra/policy_engine_complete.txt` | `governance/policy_engine.py` |
| Capstone – Security gate | `extra/security_gate_complete.txt` | `deploy/security_gate.py` |
 
> Prefer to merge by hand instead of copying? Open both files in your editor side by side, and paste the missing blocks from the `_complete.txt` file into the skeleton — save the skeleton with its original `.py` name. The end result is the same completed file.
 
### D. Lab 1 only — the Mermaid diagram preview
 
Lab 1 Step 10 renders `architecture_dfd.mmd` with VS Code's Mermaid preview. Without VS Code, open <https://mermaid.live> and paste the file's contents to see the rendered data‑flow diagram. Print the file first with:
 
```
cat threat-model/architecture_dfd.mmd
```
 
This step is just to *view* the diagram — it doesn't change any lab result.
 
### E. Lab 5 — two terminals
 
Lab 5 needs two terminals (one for the server, one for the client). Open a **second Terminal window/tab** (Cmd+T for a new tab), `cd <repo>`, activate the venv (`source py_env/bin/activate`), and `cd mcp` in it. The rest of the lab is unchanged. Stop the server with **Ctrl+C** when done.
 
---
 
## Daily start‑up checklist
 
Each time you sit down to do labs, open Terminal and:
 
1. `cd <repo>`  (your `~/ai-security-full` folder)
2. Activate the venv: `source py_env/bin/activate`  (prompt shows `(py_env)`)
3. Make sure Ollama is running — `curl http://localhost:11434/api/tags`; if it fails, run `ollama serve &` (or launch the Ollama app).
4. If using Groq and it isn't persisted: `export AGENT_PROVIDER=groq; export GROQ_API_KEY=your_key_here`
5. Warm up once: `python scripts/warmup_ollama.py`
---
 
## Troubleshooting
 
- **`command not found: python`** — use `python3`, or make sure your `py_env` virtual environment is active (inside it, plain `python` works).
- **A lab reports it cannot reach Ollama** — the server isn't running. Run `ollama serve &` (or open the Ollama app), then retry. Check its output if it persists.
- **First model call is slow (~30–60s)** — run `python scripts/warmup_ollama.py` once, then retry.
- **Groq 429 (rate limit)** — free tier is ~30 req/min. Wait a few seconds, or switch to local: `export LLM_BACKEND=ollama`.
- **Groq 401 / invalid key** — re‑copy the key from console.groq.com and `export GROQ_API_KEY` again, or unset it to fall back to Ollama.
- **`ModuleNotFoundError` (e.g. `yaml`, `chromadb`, `fastmcp`)** — the venv isn't active or packages didn't install. Run `source py_env/bin/activate` then `pip install -r requirements.txt`.
- **`Address already in use` in Lab 5** — a previous server is still running. Stop it with **Ctrl+C**, or `kill $(lsof -t -i:8000)`.
- **A `python` command seems to "hang"** — the RAG and MCP labs use interactive prompts or run a server. Follow the lab's stop instruction (`quit` or **Ctrl+C**).
---
 
*For educational use only by the attendees of our workshops.*
 
*© 2026 Tech Skills Transformations and Brent C. Laster. All rights reserved.*
 

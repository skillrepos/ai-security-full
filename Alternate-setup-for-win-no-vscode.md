# Local Setup — Windows (No VS Code)
 
## AI Security for Developers and Practitioners (Full Day)
 
This guide is for **Windows** users who don't have VS Code and don't want to install it. You'll run all 8 labs plus the capstone using plain Windows tools: **PowerShell**, **Python**, **Git**, **Ollama**, and any text editor (Notepad works). No Codespaces, no Docker, no VS Code required.
 
Because you're not using VS Code, three things in `labs.md` work a little differently — **paths**, the **`code` view command**, and the **`code -d` diff‑and‑merge step**. This guide sets everything up and then explains exactly how to handle those three differences. Read the **"How the labs differ"** section before you start Lab 1.
 
> Use **PowerShell** for all commands below (Start menu → type "PowerShell"). Not the old Command Prompt.
 
---
 
## 1. Install Python
 
1. Download **Python 3.12** from <https://www.python.org/downloads/windows/> (the "Windows installer (64‑bit)").
2. Run the installer. **On the first screen, check "Add python.exe to PATH,"** then click **Install Now**.
3. Verify in a **new** PowerShell window:
```
python --version
```
 
You should see `Python 3.12.x`. If Windows opens the Microsoft Store instead, disable the app‑alias: **Settings → Apps → Advanced app settings → App execution aliases**, and turn **off** the `python.exe` / `python3.exe` aliases, then reopen PowerShell.
 
---
 
## 2. Install Git
 
1. Download **Git for Windows** from <https://git-scm.com/download/win> and install it with the default options.
2. Verify:
```
git --version
```
 
---
 
## 3. Install Ollama (the local model runtime)
 
1. Download **Ollama for Windows** from <https://ollama.com/download> and run the installer.
2. After it installs, Ollama runs automatically in the background (look for its icon in the system tray). It also adds the `ollama` command to PowerShell.
3. Verify and pull the course model (this downloads ~2 GB, one time):
```
ollama --version
ollama pull llama3.2:3b
```
 
4. Confirm the server is reachable (Ollama listens on port 11434 by default):
```
curl http://localhost:11434/api/tags
```
 
If `curl` isn't recognized, use `Invoke-WebRequest http://localhost:11434/api/tags` instead. Either should return JSON listing your models. If it doesn't, open the Ollama app from the Start menu to start the background server.
 
---
 
## 4. Get the repository
 
Pick a folder with no spaces in the path (for example your user folder), then clone:
 
```
cd $HOME
git clone https://github.com/skillrepos/ai-security-full.git
cd ai-security-full
```
 
**Remember this folder** — it's your repo root. Every lab starts from here. From now on this guide calls it **`<repo>`**.
 
---
 
## 5. Create and activate the Python virtual environment
 
From the repo root:
 
```
python -m venv py_env
.\py_env\Scripts\Activate.ps1
```
 
Your prompt should now start with `(py_env)`. Then install the lab dependencies:
 
```
pip install -r requirements.txt
```
 
> **If activation is blocked** with a script‑execution error, run this once, then retry the activate command:
> ```
> Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
> ```
 
---
 
## 6. Pre‑download the Chroma embedding model (used by Lab 2)
 
This one‑time download makes Lab 2's first run fast. With `(py_env)` active, run:
 
```
python -c "import chromadb; c=chromadb.Client(); col=c.get_or_create_collection('warmup_kb'); col.add(documents=['warm up'], ids=['1']); print('embedding model ready')"
```
 
You should see `embedding model ready`. (Yellow warnings are fine to ignore.)
 
---
 
## 7. (Optional but recommended) Get and set a free Groq API key
 
A few labs are stronger with Groq's hosted models. Without a key, everything still runs on the local Ollama model.
 
1. Go to <https://console.groq.com>, create an account, then **API Keys → Create API Key**, and **copy the key** (you can't view it again later).
2. Set it for your labs. **Note:** the course's `scripts/setup-key.sh` is a bash script and won't run in PowerShell — set the variables directly instead.
**For the current PowerShell window only:**
 
```
$env:AGENT_PROVIDER = "groq"
$env:GROQ_API_KEY = "your_key_here"
```
 
**To persist it for all future PowerShell windows** (run once, then reopen PowerShell):
 
```
setx AGENT_PROVIDER "groq"
setx GROQ_API_KEY "your_key_here"
```
 
Confirm with `echo $env:GROQ_API_KEY`.
 
---
 
## 8. Warm up the local model
 
With `(py_env)` active:
 
```
python scripts\warmup_ollama.py
```
 
The first model call in a session is slow (~30–60s) while the model loads; this warms it up so labs feel responsive.
 
---
 
## 9. Open the labs
 
Open `labs.md` in your browser or any Markdown viewer. On GitHub you can read it rendered at the repo page; locally you can open the raw file in Notepad, or view it nicely with a browser extension / online Markdown viewer.
 
**You're ready — but first read the next section**, which covers the handful of command changes for a no‑VS‑Code setup.
 
---
 
## How the labs differ without VS Code
 
`labs.md` was written for the Codespaces/VS Code environment. Three kinds of steps need a small substitution. Everything else — every `python somefile.py` command, every prompt you type, every "look at the output" step — is **identical**.
 
### A. Paths: `/workspaces/ai-security-full/...`
 
Some labs write absolute paths like:
 
```
cd /workspaces/ai-security-full/guardrails
```
 
That path only exists in Codespaces. On Windows, `cd` into the matching folder under **your** repo instead. From the repo root:
 
```
cd <repo>\guardrails
```
 
The labs that use the relative form (`cd ../rag`, `cd ../mcp`, …) work as‑is *if* you run them from the previous lab's folder. When in doubt, just go back to the repo root and `cd` into the lab's folder by name. The lab folders are: `threat-model`, `rag`, `guardrails`, `agents`, `mcp`, `observability`, `redteam`, `governance`, `deploy`.
 
### B. `code <file>` (just viewing a file)
 
Wherever a lab says something like `code architecture.json` or `code kb.py` to **read** a file, open it in any editor instead:
 
```
notepad architecture.json
```
 
(Or use `type architecture.json` to print it in the terminal, or open it in your editor of choice.)
 
### C. `code -d <complete> <skeleton>` (the diff‑and‑merge step)
 
This is the one real workflow change. In VS Code you merge the finished code into a skeleton side‑by‑side. Without VS Code, you'll **review the differences, then copy the complete reference file over the skeleton.** The reference file (in `extra\`) is the full, correct version of the skeleton.
 
**Step 1 — see what you'd be merging** (optional but recommended, so you learn the change). `fc` is the built‑in Windows file‑compare. For example, for Lab 3:
 
```
fc extra\guardrails_complete.txt guardrails\guardrails_demo.py
```
 
Read the differences — they're the guard logic the lab is teaching. (The yellow hover "bubble" comments you'd see in VS Code are described in the lab text itself, so you're not missing the explanations.)
 
**Step 2 — apply the complete version** by copying it over the skeleton:
 
```
copy /Y extra\guardrails_complete.txt guardrails\guardrails_demo.py
```
 
That's it — the skeleton is now the completed file, exactly as if you'd merged every block in VS Code. Then continue the lab (`python guardrails_demo.py`, etc.).
 
**The file pairs for every lab** (reference `.txt` → skeleton you overwrite):
 
| Lab | `fc` / `copy` source (`extra\...`) | Destination skeleton |
|---|---|---|
| Lab 1 – Threat model | `extra\threat_model_complete.txt` | `threat-model\threat_model.py` |
| Lab 2 – RAG hardening | `extra\rag_hardened_complete.txt` | `rag\rag_hardened.py` |
| Lab 3 – Guardrails | `extra\guardrails_complete.txt` | `guardrails\guardrails_demo.py` |
| Lab 4 – Secure agent | `extra\secure_agent_complete.txt` | `agents\secure_agent.py` |
| Lab 5 – MCP server | `extra\secure_server_complete.txt` | `mcp\secure_server.py` |
| Lab 6 – Observability | `extra\observable_agent_complete.txt` | `observability\observable_agent.py` |
| Lab 7 – Red team | `extra\target_agent_complete.txt` | `redteam\target_agent.py` |
| Lab 8 – Governance | `extra\policy_engine_complete.txt` | `governance\policy_engine.py` |
| Capstone – Security gate | `extra\security_gate_complete.txt` | `deploy\security_gate.py` |
 
> Prefer to merge by hand instead of copying? Open both files in your editor side by side, and paste the missing blocks from the `_complete.txt` file into the skeleton — save the skeleton with its original `.py` name. The end result is the same completed file.
 
### D. Lab 1 only — the Mermaid diagram preview
 
Lab 1 Step 10 renders `architecture_dfd.mmd` with VS Code's Mermaid preview. Without VS Code, open <https://mermaid.live> and paste the file's contents to see the rendered data‑flow diagram. Print the file first with:
 
```
type threat-model\architecture_dfd.mmd
```
 
This step is just to *view* the diagram — it doesn't change any lab result.
 
### E. Lab 5 — two terminals
 
Lab 5 needs two terminals (one for the server, one for the client). Just open a **second PowerShell window**, `cd <repo>`, activate the venv (`.\py_env\Scripts\Activate.ps1`), and `cd mcp` in it. The rest of the lab is unchanged. Stop the server with **Ctrl+C** when done.
 
---
 
## Daily start‑up checklist
 
Each time you sit down to do labs, open PowerShell and:
 
1. `cd <repo>`  (your `ai-security-full` folder)
2. Activate the venv: `.\py_env\Scripts\Activate.ps1`  (prompt shows `(py_env)`)
3. Make sure Ollama is running — check `curl http://localhost:11434/api/tags`; if it fails, open the Ollama app from the Start menu.
4. If using Groq: `$env:AGENT_PROVIDER="groq"; $env:GROQ_API_KEY="your_key_here"` (skip if you used `setx` and reopened PowerShell).
5. Warm up once: `python scripts\warmup_ollama.py`
---
 
## Troubleshooting
 
- **`python` opens the Microsoft Store** — turn off the Python app execution aliases (Settings → Apps → Advanced app settings → App execution aliases), reopen PowerShell.
- **`Activate.ps1 cannot be loaded because running scripts is disabled`** — run `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned`, then activate again.
- **A lab reports it cannot reach Ollama** — the server isn't running. Open the Ollama app from the Start menu (or run `ollama serve` in a spare PowerShell window), then retry.
- **First model call is slow (~30–60s)** — run `python scripts\warmup_ollama.py` once, then retry.
- **Groq 429 (rate limit)** — free tier is ~30 req/min. Wait a few seconds, or switch to local: `$env:LLM_BACKEND="ollama"`.
- **Groq 401 / invalid key** — re‑copy the key from console.groq.com and set `$env:GROQ_API_KEY` again, or unset it to fall back to Ollama.
- **`ModuleNotFoundError` (e.g. `yaml`, `chromadb`, `fastmcp`)** — the venv isn't active or packages didn't install. Activate `py_env` and run `pip install -r requirements.txt`.
- **`Address already in use` in Lab 5** — a previous server is still running. Stop it with **Ctrl+C** in the server window, or restart it in a fresh terminal.
- **A `python` command seems to "hang"** — the RAG and MCP labs use interactive prompts or run a server. Follow the lab's stop instruction (`quit` or **Ctrl+C**).
---
 
*For educational use only by the attendees of our workshops.*
 
*© 2026 Tech Skills Transformations and Brent C. Laster. All rights reserved.*

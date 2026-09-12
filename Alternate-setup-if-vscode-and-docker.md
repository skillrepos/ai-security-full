# Local Setup — VS Code + Dev Container
 
## AI Security for Developers and Practitioners (Full Day)
 
This guide is for you if you **have VS Code** (or will install it) and can run **Docker**. It reproduces the exact GitHub Codespaces environment on your own machine using the repo's `.devcontainer`. The big advantage: **every command in `labs.md` works exactly as written** — same `/workspaces/ai-security-full/...` paths, same `code -d` diff‑and‑merge steps, same Mermaid preview. Nothing in the labs changes.
 
The Dev Container does all the heavy lifting for you: it builds a Debian container, creates the Python virtual environment, installs `requirements.txt`, installs Ollama, and pulls the `llama3.2:3b` model — the same scripts the Codespace runs.
 
---
 
## 1. Install the prerequisites
 
You need three things on your host machine.
 
**a. Docker.** Install **Docker Desktop** (Windows/macOS) or Docker Engine (Linux) from <https://www.docker.com/products/docker-desktop/>. Start it and let it finish initializing.
 
**b. VS Code.** Install from <https://code.visualstudio.com>.
 
**c. The Dev Containers extension.** In VS Code, open the Extensions panel (Ctrl/Cmd+Shift+X), search for **"Dev Containers"** (publisher: Microsoft), and install it.
 
> **Give Docker enough memory.** The container asks for **16 GB** and the local model needs several GB of RAM to run comfortably. In **Docker Desktop → Settings → Resources**, give it at least **8 GB of memory** (more is better) and ~**6 GB of disk**. If Docker has too little RAM, the model calls will be very slow or fail.
 
---
 
## 2. Get the repository onto your machine
 
If you already have this folder locally, skip to step 3. Otherwise, open a terminal and clone it:
 
```
git clone https://github.com/skillrepos/ai-security-full.git
cd ai-security-full
```
 
> **Folder name matters.** The devcontainer mounts your folder at `/workspaces/<folder-name>`. The labs use `/workspaces/ai-security-full`, so keep the folder named **`ai-security-full`**. If yours is named differently, either rename it, or mentally substitute your folder name wherever a lab uses that path (the relative `cd ../rag` steps are unaffected).
 
---
 
## 3. (Optional but recommended) Get a free Groq API key
 
A few labs are stronger with Groq's hosted models. Getting the key now means the container can pick it up automatically.
 
1. Go to <https://console.groq.com> and create an account.
2. Top right → **API Keys** → **Create API Key**. Fill in the info, submit, and **copy the key** (you can't view it again later).
You can also skip this and add the key later from inside the container (step 6b) — everything runs on the local Ollama model without it.
 
**To have the container pick it up automatically,** set `GROQ_API_KEY` on your **host** *before* opening the container (the devcontainer forwards `${localEnv:GROQ_API_KEY}` into the container):
 
- **macOS/Linux (bash/zsh):** add `export GROQ_API_KEY=your_key_here` to `~/.zshrc` or `~/.bashrc`, then open a **new** terminal and launch VS Code from it with `code .`
- **Windows (PowerShell):** run `setx GROQ_API_KEY "your_key_here"`, then **close and reopen** your terminal / VS Code so the variable is visible.
---
 
## 4. Open the folder in the container
 
1. In VS Code, open the `ai-security-full` folder (**File → Open Folder**).
2. VS Code detects the `.devcontainer` and shows a toast: **"Reopen in Container."** Click it.
   - If you miss the toast, open the Command Palette (**F1**), type **"Dev Containers: Reopen in Container,"** and select it.
The first build takes several minutes. It runs the same setup the Codespace does:
 
- `scripts/pysetup.sh` — creates the `py_env` virtual environment, installs `requirements.txt`, and pre‑downloads Chroma's embedding model (used by Lab 2).
- `scripts/startup_ollama.sh` — installs Ollama, starts the server, pulls `llama3.2:3b`, and warms it up.
Watch the terminal/progress output. **Setup is done when the build finishes and you get a normal shell prompt** in the integrated terminal, with the `py_env` environment active.
 
> The container also disables Copilot/inline suggestions and installs the Mermaid preview extension automatically — matching the course setup.
 
---
 
## 5. Verify the environment
 
Open a terminal in VS Code (**Terminal → New Terminal**) and run these quick checks:
 
```
python --version
ollama list
```
 
You should see Python 3.x and `llama3.2:3b` in the Ollama model list. If `ollama list` errors that it can't connect, start the server:
 
```
bash scripts/startup_ollama.sh
```
 
---
 
## 6. Set your Groq key inside the container (if using Groq)
 
**a. If you set `GROQ_API_KEY` on the host in step 3**, it's already available — confirm with `echo $GROQ_API_KEY`. You can still run the helper below to persist `AGENT_PROVIDER=groq` for all terminals.
 
**b. Otherwise, set it now.** In the VS Code terminal, run the course helper and paste your key when prompted:
 
```
source scripts/setup-key.sh
```
 
You should see confirmation that `AGENT_PROVIDER` and `GROQ_API_KEY` are set. This persists them for all future terminals in the container.
 
---
 
## 7. Warm up the local model (faster first responses)
 
```
python scripts/warmup_ollama.py
```
 
The first model call in any session is slow (~30–60s) while the model loads into memory; this warms it up so the labs feel snappy.
 
---
 
## 8. Open the labs and go
 
Open `labs.md` (right‑click → **Open Preview**, or the Command Palette → "Markdown: Open Preview"). Because you're in the Dev Container, **follow `labs.md` exactly as written** — every path, every `code` command, and every `code -d` diff‑merge step works as printed.
 
**You're ready for the labs!**
 
---
 
## Daily start‑up checklist
 
Each time you come back to the labs:
 
1. Open the folder in VS Code → **Reopen in Container** (it reuses the existing container; the `postAttachCommand` restarts Ollama for you).
2. In a terminal, confirm the model server is up: `bash scripts/startup_ollama.sh`
3. If you use Groq and it isn't already set: `source scripts/setup-key.sh`
4. Warm up once: `python scripts/warmup_ollama.py`
---
 
## Troubleshooting
 
- **"Reopen in Container" never appears** — make sure the Dev Containers extension is installed and Docker Desktop is running, then use **F1 → Dev Containers: Reopen in Container** manually.
- **Build fails on Ollama install / out of memory** — increase Docker Desktop's memory allocation (Settings → Resources) to at least 8 GB and rebuild (**F1 → Dev Containers: Rebuild Container**).
- **A lab reports it cannot reach Ollama** — run `bash scripts/startup_ollama.sh` from the repo root, then retry. Check `/tmp/ollama.log` if it persists.
- **First model call is slow (~30–60s)** — run `python scripts/warmup_ollama.py` once, then retry.
- **Groq 429 (rate limit)** — you've exceeded the free tier (~30 req/min). Wait and retry, or `export LLM_BACKEND=ollama` to use the local model.
- **Groq 401 / invalid key** — re‑run `source scripts/setup-key.sh` with a fresh key from console.groq.com, or unset it to fall back to Ollama.
- **`ModuleNotFoundError`** — the virtual env isn't active or packages didn't install. Run `pip install -r requirements.txt` from the repo root inside the container.
- **`Address already in use` in Lab 5** — a previous server is still running. Stop it with `Ctrl+C`, or `kill $(lsof -t -i:8000)`.
The rest of the standard troubleshooting in `README.md` applies unchanged.
 
---
 
*For educational use only by the attendees of our workshops.*
 
*© 2026 Tech Skills Transformations and Brent C. Laster. All rights reserved.*

# AI Security for Developers and Practitioners (Full Day)

## Building safe, trustworthy, and resilient AI systems ##

This full-day, hands-on workshop equips developers, architects, and technical leaders to secure AI systems end to end - from model interaction to production deployment. Across **eight focused labs** you will threat-model an AI system, defend a RAG pipeline, build guardrails, harden an MCP server, instrument an agent for observability, red-team an agent, enforce security-as-code governance, and gate a deployment with DevSecOps checks.

Each lab runs in about **10-12 minutes** inside a GitHub Codespace, with no local installation. Labs 2, 3, 5, 6, and 7 use a real language model (see **Language models** below); Labs 1, 4, and 8 use none. The only Python dependency is PyYAML (Lab 7), installed automatically during setup.

These instructions will guide you through configuring a GitHub Codespaces environment that you can use to do the labs.

**1. Change your codespace's default timeout from 30 minutes to longer (90 minutes is recommended for a full-day session).**
To do this, when logged in to GitHub, go to https://github.com/settings/codespaces and scroll down on that page until you see the *Default idle timeout* section. Adjust the value as desired.

![Changing codespace idle timeout value](./images/prompt-accel1.png?raw=true "Changing codespace idle timeout value")

**2. Click on the button below to start a new codespace from this repository.**

Click here ➡️  [![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/skillrepos/ai-security-full?quickstart=1)

**3. Then click on the option to create a new codespace.**

![Creating new codespace from button](./images/prompt-accel2.png?raw=true "Creating new codespace from button")

This will run for a while as it builds the environment and runs the setup script to prepare the Python environment. This takes a couple of minutes.

The codespace is ready to use when you see a prompt in its terminal and the setup script reports `Environment ready.`

![Ready to use](./images/prompt-accel4.png?raw=true "Ready to use")

**4. Open up the *labs.md* file so you can follow along with the labs.**
You can either open it in a separate browser instance or open it in the codespace.

![Opening labs](./images/ai-security-labs.png?raw=true "Opening labs")

**Now, you are ready for the labs!**

---

## Language models

Labs 2, 3, 5, 6, and 7 use a real language model so you can observe genuine model behavior and genuine attacks. A shared helper, `common/llm.py`, picks the backend automatically; you do not call it directly.

**Ollama (`llama3.2:3b`) - default, no setup needed.** The `scripts/startup_ollama.sh` script (run automatically when the Codespace is created) installs Ollama, starts it, pulls `llama3.2:3b`, and runs a first-inference warm-up. If a lab ever reports it cannot reach Ollama, run `bash scripts/startOllama.sh` from the repo root. You can also pre-warm manually with `python3 scripts/warmup_ollama.py`. The first model call in a session may still take ~30-60 seconds after long idle periods; subsequent calls are quick.

**Groq - optional, faster and more powerful.** If you set a free Groq API key, **all five model labs use Groq instead of Ollama** - `llama-3.1-8b-instant` for the "fast" labs and `llama-3.3-70b-versatile` for the "strong" ones (Labs 2 and 5). Groq's inference is extremely fast and removes the local warm-up. Without a key, the labs use Ollama automatically. To enable it:

1. In a browser, go to https://console.groq.com and sign in (free).
2. Open **API Keys**, click **Create API Key**, and copy the key (you can't view it again later).
3. Make the key available to the labs. For the whole Codespace: **GitHub → Settings → Codespaces → Secrets → New secret**, name it `GROQ_API_KEY`, and grant it access to this repository (then rebuild/reopen). For a single terminal session you can instead run:

   ```
   export GROQ_API_KEY=<paste-your-key-here>
   ```

   The free tier allows about 30 requests/minute and 1,000 requests/day per key - plenty for the labs, as long as each person uses their own key. (You can override the model ids with `GROQ_MODEL_FAST` / `GROQ_MODEL_STRONG` if you like.)

**Choosing a backend manually.** Any lab honors an `LLM_BACKEND` override: `export LLM_BACKEND=ollama` (or `groq`, or `mock` for an offline deterministic stand-in used only for testing).

Because these labs use a real model, **exact wording varies from run to run** - the lab steps describe what to look for, not an exact transcript.

---

## Labs at a glance

| # | Lab | Directory | Focus |
|---|-----|-----------|-------|
| 1 | Mapping AI Security Risks | `threat-model/` | Threat modeling, OWASP LLM Top 10, attack surface |
| 2 | Securing Prompts and Contexts | `rag/` | RAG document poisoning, injection defense, output scanning |
| 3 | Implementing Guardrails | `guardrails/` | Input/output validator pipeline (Guardrails.ai / Llama Guard pattern) |
| 4 | Hardening MCP Servers and Tools | `mcp/` | Scoped JWT auth, per-tool authorization, least privilege |
| 5 | Auditing and Observability for Agents | `observability/` | Trace IDs, structured audit logs, anomaly detection |
| 6 | Adversarial Testing and Red-Teaming | `redteam/` | Automated attack harness, measure-mitigate-remeasure |
| 7 | Policy-Driven Governance | `governance/` | Security-as-code policy engine, runtime enforcement |
| 8 | Secure Deployment and Lifecycle Management | `deploy/` | DevSecOps gate: secrets, CVEs, signing, compliance |

## System requirements

- A GitHub account with Codespaces enabled. The devcontainer requests a **4-core / 16 GB** machine so the local model (Ollama `llama3.2:3b`) runs comfortably.
- A modern browser (Chrome recommended for copy/paste in the Codespace).
- No local installation is required. A free Groq API key is optional (see **Language models**).

## Troubleshooting

- **A lab reports it cannot reach Ollama** - the server isn't running. Run `bash scripts/startOllama.sh` from the repo root, then retry. Check `/tmp/ollama.log` if it persists.
- **The first model call is slow (~30-60s)** - run `python3 scripts/warmup_ollama.py` once, then retry. Later calls in the same session are fast.
- **Groq returns 429 (rate limit)** - you've exceeded the free tier's ~30 req/min. Wait a few seconds and retry, or `export LLM_BACKEND=ollama` to switch to the local model. Make sure each person uses their own key.
- **Groq returns 401 / invalid key** - `GROQ_API_KEY` is missing or wrong. Re-copy the key from console.groq.com, or unset it to fall back to Ollama.
- **A `python` command "hangs"** - the RAG and MCP labs use interactive prompts or run servers. Follow the lab's stop instruction (`quit` or `Ctrl+C`).
- **`Address already in use` in Lab 4** - a previous server is still running. Stop it with `Ctrl+C`, or `kill $(lsof -t -i:8000)` / `:9000`.
- **`ModuleNotFoundError: yaml` in Lab 7** - run `pip install -r requirements.txt` from the repo root.
- **Skeleton file errors before merging** - the skeleton files are meant to be completed via the `code -d` diff-merge step first. Each lab tells you when to merge.

## License and attribution

For educational use only by the attendees of our workshops.

© 2026 Tech Skills Transformations and Brent C. Laster. All rights reserved.

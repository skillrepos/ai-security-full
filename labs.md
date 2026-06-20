# AI Security for Developers and Practitioners (Full Day)
## Building safe, trustworthy, and resilient AI systems
## Session labs
## Revision 4.0 - 06/20/26


**Follow the startup instructions in the README.md file IF NOT ALREADY DONE!**

**NOTE: To copy and paste in the codespace, you may need to use keyboard commands - CTRL-C and CTRL-V. Chrome may work best for this.**


**Lab 1: Mapping AI Security Risks**

**Purpose: In this lab, we'll perform a structured threat model of an AI system. We'll map every component (LLM, RAG, agent, MCP tools) to the OWASP Top 10 for LLM Applications (2025), score the attack surface, and pinpoint where the highest-risk vulnerabilities and trust-boundary crossings occur.**

---

**What we're doing:** A threat model answers three questions about a system — *what could go wrong, where, and what do we fix first* — in a structured, repeatable way rather than as a brainstorm. In this lab a small Python engine builds that model for a sample AI product and prints a ranked report. There's no language model here — it's pure analysis of the system's design, so it runs instantly and gives the same answer every time.

**The big idea, in one line:** take a description of the system, match each part to a list of known AI risks, score those risks, and sort them — so you end up with a *prioritized to-do list* instead of a vague worry. That's all the engine does.

**The files in the *threat-model* directory and what each is for:**

| File | Role |
|---|---|
| **`architecture.json`** | The **system under review** — the OmniTech assistant described as *data, not code*: its components, the data flows between them, and the trust boundaries they cross. This is the input you are modeling. |
| **`owasp_llm.py`** | The **knowledge base** (provided complete) — the OWASP LLM Top 10 (2025) catalog: for each risk, which component *types* it applies to, plus a `COMPONENT_EXPOSURE` table of likelihood weights. |
| **`threat_model.py`** | The **engine** — you fill in **two** small functions; it then joins the system to the catalog, scores every component-vs-risk pair, flags trust-boundary crossings, prints the ranked threat model, and writes two deliverables. |
| **`../extra/threat_model_complete.txt`** | The completed reference you diff-and-merge into the skeleton. |

> **A note on frameworks (no memorizing required):** the **OWASP LLM Top 10 (2025)** is the risk list we map to — *that's* the one to pay attention to. You'll also see a **MITRE ATLAS** column of ids like `AML.T0051`; ATLAS is a catalog of real-world AI attack techniques ("ATT&CK for AI"). Treat it as a **bonus cross-reference** for now — we go deeper later, and nobody expects you to know the ids.

---

<br>

1. From the terminal, change to the *threat-model* directory:

```
cd threat-model
```

<br><br>

2. First, examine the description of the system we are going to threat-model. Open the architecture file and read through it:

```
code architecture.json
```

This describes the **OmniTech Customer Support AI Assistant** as structured data with three parts:
   - **`components`** — every part of the system. Each has a **`type`** (`ui`, `llm`, `rag`, `agent`, `tool`, `mcp`, `datastore`, or `deploy`) — this is the key the engine uses to look up which risks apply — a **`trust_zone`** (`public`, `app`, or `internal`) saying how exposed it is, and a **`handles_pii`** flag that raises the impact of a compromise.
   - **`data_flows`** — how information moves between components (for example, `web_ui -> chat_llm`). These are the paths an attacker's input can travel.
   - **`trust_boundaries`** — where one trust zone meets another (the internet edge between `public` and `app`, and the app-to-data boundary between `app` and `internal`). These are the lines an attacker has to cross, so controls matter most here.

This is just a model of the system — change the JSON and the threat model changes with it (you'll try that at the end).

![Examining the architecture](./images/sl1.png?raw=true "Examining the architecture")

<br><br>

3. Now look at the risk catalog we'll map against. Open it and skim the entries:

```
code owasp_llm.py
```

This is the **OWASP Top 10 for LLM Applications (2025)** encoded as a lookup table. Read it from the component's point of view: each risk's **`applies_to`** list says which component *types* that risk is relevant to (for example, `LLM06 Excessive Agency` applies to `agent`, `tool`, and `mcp`). So when the engine processes the `support_agent`, it inherits every risk whose `applies_to` includes `agent` — prompt injection, excessive agency, improper output handling, and more — while a `datastore` inherits only the couple that list it.

Each risk also carries an optional **`atlas`** field — the MITRE ATLAS technique id(s) for that risk (e.g., `LLM01 Prompt Injection` → `AML.T0051`). Some are left blank where ATLAS has no clean match yet. As noted above, this is bonus context — skim it and move on.

Below the catalog, the **`COMPONENT_EXPOSURE`** table gives each component type a **likelihood weight** from 1 to 3 — how reachable/attackable that type is. A `ui` and a `rag` are `3` (they take untrusted input directly), an `llm`/`tool`/`mcp` are `2`, and an internal `datastore`/`deploy` are `1`. The engine uses this number as the *likelihood* half of the score.

![Examining the architecture](./images/sl2.png?raw=true "Examining the architecture")

<br><br>

4. Now open the engine. Most of it is already written; just **two** functions are left blank for you — the lookup and the scoring. Open the diff-and-merge view to compare the skeleton (right) with the complete reference (left):

```
code -d ../extra/threat_model_complete.txt threat_model.py
```

The two functions you complete (the join, the trust-boundary check, and the report writers are already done for you):
   - **`map_risks(component)`** — the *lookup*: keep only the OWASP risks whose `applies_to` list includes this component's `type`. (So an `agent` picks up prompt injection, excessive agency, and more; a `datastore` picks up just a couple.)
   - **`score(component, risk)`** — the *math*: **likelihood × impact**. *Likelihood* is the component type's `COMPONENT_EXPOSURE` weight (1–3; higher = more exposed). *Impact* is `2`, or `3` if the component handles PII, bumped one higher for the two most damaging risks (Sensitive Disclosure `LLM02` and Excessive Agency `LLM06`). The result is banded **HIGH** (≥ 8), **MEDIUM** (5–7), or **LOW** (< 5).

That's the whole method: the engine never "guesses" a threat — it mechanically pairs every component with every applicable risk and scores the pair, which is what makes the result repeatable.

![Merging the threat model engine](./images/sl3.png?raw=true "Merging the threat model engine")

<br><br>

5. Merge the highlighted differences from the complete version (left) into the skeleton (right) by clicking the arrows (›) in the middle bar — you'll see just three: a short comment block at the top and the two function bodies. When no differences remain, close the diff tab to save.

<br><br>

6. Run the threat model:

```
python threat_model.py
```

✓ **Success looks like:** a table prints and the run ends with `=== DELIVERABLES WRITTEN ===` and two file names. If you instead see `NotImplementedError`, one of the two functions didn't get merged — reopen the diff (Step 4) and finish it.

![Runnning the threat model engine](./images/sl4.png?raw=true "Running the threat model engine")

<br><br>

7. **Scroll up in the terminal to the start of the tool output.** Look at the **threat model table** — you don't need to read all 43 rows, just scan the top. Each row is one **component × risk** pair; the columns are the component, its type, the OWASP risk id and name, the mapped **MITRE ATLAS** technique id(s), the numeric score, and the band. It is sorted by score, highest first. Notice that the `support_agent` component dominates the top with multiple **HIGH** rows — it is an `agent` (likelihood 3) that handles PII (impact 3), so its applicable risks score 9. That matches the real world: an agent that acts autonomously and calls tools is the largest attack surface in this system. The ATLAS column ties each finding to a real, documented attack technique you can look up at atlas.mitre.org.

![Threat model output](./images/sl5.png?raw=true "Threat model output")

<br><br>

8. Look at the **TRUST BOUNDARY CROSSINGS** section. These are the data flows that move between trust zones (for example, `web_ui -> chat_llm` crosses the internet edge). These crossings are where you should concentrate your strongest controls.

![Trust boundary crossings](./images/sl6.png?raw=true "Trust boundary crossings")

<br><br>

9. Finally, review the **TOP 5 RISKS TO MITIGATE FIRST**. This is the prioritized list you would hand to an engineering team - it tells them exactly which risk, on which component, to address first.

![Top 5 risks](./images/sl7.png?raw=true "Top 5 risks")

<br><br>

10. The run also wrote two **deliverables** - the actual artifacts a threat-modeling exercise produces. Open them:

```
code threat_model_report.md
code architecture_dfd.mmd
```

`threat_model_report.md` is a **risk register** - the full prioritized table (OWASP + ATLAS), the trust-boundary crossings, and the top-5, formatted to hand to a team or drop into a ticket. `architecture_dfd.md` is a **data-flow diagram** written in Mermaid - the components grouped by trust zone, with ** arrows (`-->`) marking every flow that crosses a trust boundary**. To see it rendered, open `architecture_dfd.mmd` and click `F1` to get to the `Command Pallet`. Then find  `Mermaid: Mermaid Preview` and select that entry.

![Generated risk register](./images/sl8.png?raw=true "Generated risk register")

![Generated data-flow diagram](./images/sl10.png?raw=true "Generated data-flow diagram")

<br><br>

11. (Optional) Threat models change as the system changes. Open `architecture.json`, find the `account_tool` component, and change its `"handles_pii"` value from `true`... or add a brand-new component such as `{"id": "audit_log", "type": "datastore", "trust_zone": "internal", "handles_pii": true}` to the components list. Save, then re-run `python threat_model.py` and watch the scores, rankings, and both deliverables update.

<br><br>



<br><br>

**Key Takeaways:**
- **Threat modeling is structured, not guesswork** - mapping components to a known catalog (OWASP LLM Top 10) makes coverage systematic and repeatable.
- **Agents and tools concentrate risk** - autonomy plus tool access creates the largest attack surface.
- **Trust-boundary crossings deserve the strongest controls** - that's where untrusted data meets trusted systems.
- **A good threat model produces a prioritized backlog** - it tells the team what to fix first, not just what could go wrong.

<p align="center">
<b>[END OF LAB]</b>
</p>
<br><br>

**Lab 2: Defending RAG from Poisoned Documents**

**Purpose: In this lab, we'll defend a RAG pipeline against document poisoning. We'll see how a malicious document injected into the knowledge base can hijack the model with hidden instructions and phish users, then implement defensive layers - source allowlisting, injection detection, relevance filtering, and output scanning - to neutralize the attack.**

<br>

1. From the terminal, change to the *rag* directory:

```
cd ../rag

or

cd /workspaces/ai-security-full/rag
```

<br><br>

2. Examine the poisoned document that simulates what an attacker might inject into a knowledge base. Open it and read through it carefully:

```
code docs/OmniTech_Security_Bulletin.txt
```

This looks like a legitimate OmniTech bulletin, but it carries three attacks: a hidden `[SYSTEM OVERRIDE]` **prompt injection**, a **phishing URL** (`https://omnitech-secure-verify.com/reset`), and a **social-engineering** instruction to email full credit card numbers for "refund verification."

![The poisoned document](./images/sl11.png?raw=true "The poisoned document")

<br><br>

3. Look at the retrieval helpers used by both versions of the lab:

```
code kb.py
```

This is a **real RAG pipeline** built on a local **Chroma vector database**. `kb.py` opens that database, runs a **semantic similarity** search (`retrieve`) using real embeddings (Chroma's built-in `all-MiniLM-L6-v2`), and sends the top chunks to a **real model** (`rag_answer`, which uses `prefer="strong"` - Groq's 70B model if you have a key, otherwise Ollama). Notice the system prompt tells the model to answer **using only the retrieved context** and to include any URL or instruction it finds there - which is exactly why a poisoned chunk reaching this stage is dangerous.

<br><br>

4. Now build the vector database. `create_db.py` chunks every document in `docs/` - the legitimate handbook and returns policy **and** the poisoned bulletin - embeds them, and stores them in the same Chroma collection. This simulates an attacker who has slipped a malicious document into the knowledge base:

```
python create_db.py
```

You'll see each source and its chunk count, with the poisoned PDF flagged. (The first run downloads the small embedding model, ~30-60s; later runs are instant.)

![Building the vector database](./images/sl12.png?raw=true "Building the vector database")

<br><br>

5. Run the **vulnerable** RAG system - this is RAG with no security defenses:

```
python rag_vulnerable.py
```

You'll see the vector DB load, including the poisoned source mixed in with the two legitimate documents. (The first model query also includes a ~30-60s warm-up.)

![Loading the knowledge base](./images/sl13.png?raw=true "Loading the knowledge base")

<br><br>

6. At the prompt, ask:

```
How do I reset my password?
```

Watch the **SOURCES** and **ANSWER**. Because the poisoned bulletin really is about password resets, it scores a high similarity and `OmniTech_Security_Bulletin_2024.pdf` appears among the retrieved sources - and the answer hands the user the **phishing URL** from the poisoned document.

![Phishing URL in the answer](./images/sl14.png?raw=true "Phishing URL in the answer")

<br><br>

7. Now ask:

```
How do I get a refund?
```

The poisoned document's instruction to share a full credit card number surfaces in the response. The vulnerable system trusts all retrieved context equally. Type `quit` to exit.

![Phishing URL in the answer](./images/sl15.png?raw=true "Phishing URL in the answer")

<br><br>

8. Now let's add defenses. You can `exit` out of the running program. Open the diff-and-merge view to compare the skeleton with the complete hardened version:

```
code -d ../extra/rag_hardened_complete.txt rag_hardened.py
```

![Building the hardened version](./images/sl16.png?raw=true "Building the hardened version")

<br><br>

9. Examine the `SecurityGuard` class in the complete version (left side). It implements four layers of defense in depth:
   - **Source allowlist** - only chunks from known, verified PDFs are trusted (the poisoned bulletin is not on the list)
   - **Injection detection** - regex patterns catch `[SYSTEM OVERRIDE]`, `ignore previous instructions`, `supersedes all previous`, etc.
   - **Relevance threshold** - low-confidence chunks are dropped
   - **Output scanning** - the final answer is scrubbed of phishing domains and sensitive-data requests

Note the `filter_chunks()` and `scan_output()` methods - these are the two checkpoints that block bad input and redact bad output.

<br><br>

10. Merge all sections from the complete version (left) into the skeleton (right). When no differences remain, close the diff tab to save.

<br><br>

11. Run the hardened version against the same poisoned knowledge base:

```
python rag_hardened.py
```

Notice the startup output now labels each source `[TRUSTED]` or `[UNKNOWN]`.

![Trusted vs unknown sources](./images/sl17.png?raw=true "Trusted vs unknown sources")

<br><br>

12. Ask the same two questions again:

```
How do I reset my password?
```
```
How do I get a refund?
```

This time the poisoned chunks are blocked at the source-allowlist stage, and any sensitive request that slips into the output is redacted. The answers now come only from the legitimate handbook and returns policy. Type `report` to see every security event, then `quit` to exit.


![Blocked and redacted](./images/sl18.png?raw=true "Blocked and redacted")

<br><br>

**Key Takeaways:**
- **Document poisoning is a real threat** - anyone who can insert a document into a RAG knowledge base can steer its outputs.
- **Treat retrieved content as untrusted input** - it can carry hidden instructions aimed at the model.
- **Defense in depth wins** - source allowlists, injection detection, relevance filtering, and output scanning each catch what the others miss.
- **Output scanning is the safety net** - it protects users even when a malicious chunk slips through input filtering.

<p align="center">
<b>[END OF LAB]</b>
</p>
<br><br>

**Lab 3: Implementing Guardrails**

**Purpose: In this lab, we'll build a guardrails pipeline modeled on the validator pattern used by frameworks like Guardrails.ai and Llama Guard. Input guards run *before* the model to block jailbreaks and off-topic or oversized requests; output guards run *after* the model to redact PII and block unsafe completions before they reach the user.**

<br>

1. From the terminal, change to the *guardrails* directory:

```
cd /workspaces/ai-security/guardrails
```

<br><br>

2. Open the skeleton and review its shape:

```
code guardrails_demo.py
```

Notice the two families of guards. **Input guards** (`guard_jailbreak`, `guard_topic`, `guard_length`) screen the user's request. **Output guards** (`guard_pii`, `guard_banned`) screen the model's response. Each guard returns `(ok, reason, fixed_text)` - if a guard returns fixed text, the pipeline *repairs* the content and continues; if it returns `None`, the content is *blocked*. These are the cheap, fast, deterministic checks you control.

Wrapping those hand-built guards, `main()` also calls a **real safety classifier — Meta's Llama Guard 4, hosted on Groq** — on both the input and the output (via `llm.moderate()`). That's the production pattern: regex/allowlist guards you own, **plus** a model-based classifier that catches whole categories of harmful content (violence, weapons, hate, self-harm, ...) you could never enumerate by hand. Llama Guard runs only if you've set a `GROQ_API_KEY`; without one, the lab still runs with just the hand-built guards.

<br><br>

3. Open the diff-and-merge view to fill in the validator logic:

```
code -d ../extra/guardrails_complete.txt guardrails_demo.py
```

![Building the guardrails pipeline](./images/fd-l3-1.png?raw=true "Building the guardrails pipeline")

<br><br>

4. Review the **input guards** in the complete version: the jailbreak patterns (`ignore previous instructions`, `reveal your system prompt`, "developer mode," etc.), the `ALLOWED_TOPICS` allowlist that keeps the assistant in its lane, and the maximum input length.

<br><br>

5. Review the **output guards**: the `PII_PATTERNS` that redact SSNs, card numbers, and emails (a *FIXED* outcome), and the `BANNED_OUTPUT` patterns that hard-block dangerous responses (a *BLOCK* outcome). Note how `run_guards` distinguishes a repairable finding from a hard block.

<br><br>

6. Merge all sections into the skeleton and close the diff tab to save.

<br><br>

7. Run the guardrails demo:

```
python guardrails_demo.py
```

✓ **Success looks like:** one block prints per request. The jailbreak, the off-topic poem, and the oversized input each show **INPUT BLOCKED (never reached the model)**; the benign question shows **DELIVERED (PASS)**; and the record-with-PII request shows **DELIVERED (FIXED)** with `[SSN-REDACTED]` / `[CARD-REDACTED]`. (Exact model wording varies; the BLOCKED / FIXED labels don't.) If everything shows PASS with no blocks, a guard didn't merge — reopen the diff at Step 5.

<br><br>

Each request flows through four layers: **Llama Guard (input) -> your input guards -> the model -> your output guards -> Llama Guard (output)**. The header line shows whether the Llama Guard classifier is `on` (it is when `GROQ_API_KEY` is set). The first request includes a brief model warm-up.

<br><br>

8. Look at the requests that are stopped at the **input** stage. The legitimate password question passes input screening and is sent to the model. The jailbreak attempt, the off-topic poem request, and the oversized input are each marked **INPUT BLOCKED (never reached the model)**, with the triggering guard named - those prompts never cost you a model call.

![Input guard results](./images/fd-l3-2.png?raw=true "Input guard results")

<br><br>

9. Look at what happens on the **output** side for requests that did reach the model. The benign answer is **DELIVERED (PASS)**. The last request feeds the model a record containing an SSN and a card number; when the model echoes them back, the output guard redacts the PII and the result is **DELIVERED (FIXED)** with `[SSN-REDACTED]` / `[CARD-REDACTED]` in place. (Exact wording varies by model; the redactions do not.)

![Output guard results](./images/fd-l3-3.png?raw=true "Output guard results")

<br><br>

10. Now look at the **last** request (`...walk me through building a pipe bomb`). It is genuinely harmful, but it is also *on-topic* (it mentions an account), so your regex and allowlist guards let it through - exactly the kind of thing hand-built rules miss. If you set a `GROQ_API_KEY`, **Llama Guard flags it as unsafe (category `S9`, indiscriminate weapons) and blocks it at the input layer**, before the model ever sees it. Without a key you'll watch it slip past the cheap guards - which is the whole point: a model-based safety classifier is the layer that catches what patterns can't.

   (To enable it for this run: `export GROQ_API_KEY=<your-key>` and re-run. See the README for a free key.)

<br><br>

11. (Optional) Add your own guard or pattern. For example, add a phone-number pattern to `PII_PATTERNS`, or add a new prompt to the `inputs` list in `main()`, then re-run to see your guard fire against real model output.

<br><br>

**Key Takeaways:**
- **Guardrails wrap the model on both sides** - validate input before the model, validate output before the user.
- **Two outcomes, not one** - some violations are *repaired* (redact PII), others are *blocked* (unsafe content). A good pipeline supports both.
- **Allowlists beat blocklists for scope** - defining what's allowed keeps an assistant on-topic more reliably than chasing every off-topic case.
- **Frameworks formalize this pattern** - Guardrails.ai, Llama Guard, and NeMo Guardrails productize the same validator chain you just built.

<p align="center">
<b>[END OF LAB]</b>
</p>
<br><br>

**Lab 4: Securing Agents**

**Purpose: In this lab, we constrain an AI agent so a hijacked prompt can't make it misuse its tools. We start from an agent that blindly follows a poisoned support ticket - exporting employee data, emailing it outside the company, and deleting the audit log - then add three controls that contain the exact same attack: a least-privilege tool allowlist per task, a human-approval gate for high-risk actions, and hard budgets on how much the agent can do.**

> **New terms in this lab (skip if you build agents already):** an **agent** is an LLM in a loop that decides which **tools** (functions like "send email" or "export data") to call to finish a job. **Indirect prompt injection** is when the malicious instructions arrive *inside data the agent reads* - here, a hidden note in a support ticket - rather than from the user. **Least privilege** means giving the agent only the tools a given task needs. An **allowlist** is the explicit set of permitted tools. An **approval gate** pauses a risky action for a human to approve. A **budget** is a hard cap on how many steps or tool calls one run may take.

<br>

1. From the terminal, change to the *agents* directory:

```
cd /workspaces/ai-security/agents
```

<br><br>

2. Open the agent skeleton and read the scenario:

```
code secure_agent.py
```

Look at three things. `TICKET` is a support request that *looks* benign ("summarize the Q3 benefits changes") but hides an attacker's instructions in an HTML comment - the indirect-injection payload. The tool set is split into `SAFE_TOOLS` (`read_ticket`, `summarize`) and `HIGH_RISK_TOOLS` (`export_data`, `send_email`, `delete_records`). A **real model** reads the ticket in `build_plan()` and proposes which tools to call - and, taking the bait, it tries to run the dangerous ones.

<br><br>

3. Run the agent as shipped to see the attack land:

```
python secure_agent.py
```

The script runs the agent's plan twice. Right now the three control functions are no-ops, so **both** runs behave identically: `export_data`, `send_email`, and `delete_records` all fire, ending in `BREACH`. That's the undefended agent doing exactly what the poisoned ticket told it to. (Tool choices come from a real model, so the model's proposed plan may vary run to run; the canonical attack is replayed so the breach is reproducible.)

<br><br>

4. Open the diff-and-merge view to build the three controls:

```
code -d ../extra/secure_agent_complete.txt secure_agent.py
```

![Building the secured agent](./images/fd-secagents-1.png?raw=true "Building the secured agent")

<br><br>

5. Review the three functions you'll merge in - this is the whole defense:
   - **`allowed_tools(task)`** - *least privilege.* Return only the tools this job needs (`read_ticket`, `summarize`, `send_email`). Because `export_data` and `delete_records` are never offered, a hijacked plan that calls them is refused outright.
   - **`approve(tool, args)`** - *human approval gate.* Low-risk tools run freely; high-risk tools pause for an operator. In this unattended demo the operator denies the unexpected action (emailing data to an outside address was never part of the ticket).
   - **`within_budget(steps_taken, executed)`** - *budgets.* Stop the run once it exceeds `MAX_STEPS`, so even a bypassed agent can't loop or escalate.

<br><br>

6. Merge all three sections into the skeleton and close the diff tab to save.

<br><br>

7. Run the secured agent:

```
python secure_agent.py
```

✓ **Success looks like:** the **SECURED AGENT** section shows `export_data` **BLOCKED** (allowlist), `send_email` **BLOCKED** (approval denied), the remaining steps **HALTED** (budget), and ends `contained (no high-risk tool fired)` — while the **UNDEFENDED** section above still ends in `BREACH`. If the secured run also shows `BREACH`, a control didn't merge; reopen the diff at Step 4.

<br><br>

8. Compare the two runs in the output. The **UNDEFENDED AGENT** still ends in `BREACH`. The **SECURED AGENT** runs the same plan but contains it - and you can see *each control* doing a distinct job:
   - `export_data` -> **BLOCKED (not in least-privilege allowlist)**
   - `send_email` -> **BLOCKED (approval denied)**
   - the remaining attacker steps -> **HALTED (budget)**

   The legitimate `read_ticket` and `summarize` steps still succeed, so the agent completes the job it was actually hired to do.

![Same hijack, contained](./images/fd-secagents-2.png?raw=true "Same hijack, contained")

<br><br>

9. Notice that all three controls are necessary. Least privilege removes the tools the task never needs; the approval gate catches a high-risk tool the task *does* legitimately use (`send_email`) but that the attacker tried to abuse; budgets cap the blast radius if anything slips through. Defense in depth - no single control has to be perfect.

<br><br>

10. (Optional) Tighten or loosen a control and re-run to see the effect:
   - In `approve()`, temporarily `return True` for everything and re-run - `send_email` now fires. Put the denial back.
   - In `allowed_tools()`, add `"export_data"` to the returned set and re-run - the export is no longer blocked by least privilege (the approval gate and budget are your remaining nets). Remove it again.
   - Lower `MAX_STEPS` to `2` and re-run - even the second legitimate step gets budget-halted, showing why budgets must be sized to the real work.

<br><br>

**Key Takeaways:**
- **The agent will be talked into things** - indirect prompt injection means any data the agent reads can carry instructions. Assume the model will follow them.
- **Least privilege first** - the safest dangerous tool is the one you never hand the model for that task.
- **Gate high-risk actions** - some tools are legitimate but consequential; route those through a human (or a stricter policy) before they fire.
- **Budget the blast radius** - hard caps on steps and tool calls keep a hijacked agent from looping or escalating, even when other controls miss.

<p align="center">
<b>[END OF LAB]</b>
</p>
<br><br>

**Lab 5: Hardening MCP Servers and Tools**

**Purpose: In this lab, we'll harden a real Model Context Protocol (MCP) server built with FastMCP. A token authority issues scoped JWT access tokens (PyJWT), and the MCP server enforces per-tool scope checks in FastMCP middleware - so the same server grants different clients access to different subsets of tools, following least privilege.**

**This lab uses two terminals: the MCP server and the client.**

> **New terms in this lab (skip if you do API auth in your sleep):** a **token / JWT** here is a short, signed "pass" a caller presents — *not* the AI "token" from Lab 0. A **Bearer token** just means "whoever holds this pass is allowed in," sent in the request's `Authorization` header. A **scope** is one specific permission written into that pass (e.g., `tools:add` = "may call the add tool"). **Middleware** is code that runs on *every* request before it reaches a tool — the perfect place to check the pass. **Least privilege** = give each caller only the scopes it actually needs. An **identity provider** is the service that issues these passes (here, our little `auth.py`).

<br>

1. From the terminal, change to the *mcp* directory:

```
cd /workspaces/ai-security/mcp
```

<br><br>

2. Review the token authority (provided complete):

```
code auth.py
```

`auth.py` mints and verifies scoped JWTs with the real **PyJWT** library. Note the **client registry**: `full-client` is granted scopes for all three tools (`tools:add`, `tools:multiply`, `tools:divide`), while `limited-client` is granted only `tools:add`. Those scopes are signed into each token's `scope` claim, so they can't be tampered with. (This stands in for a real identity provider.)

<br><br>

3. Open the MCP server skeleton:

```
code secure_server.py
```

This is a real **FastMCP** server exposing three tools (`add`, `multiply`, `divide`) over HTTP. The security lives in `ScopeMiddleware.on_call_tool`, which runs on **every** tool call: it reads the `Authorization` header, verifies the Bearer JWT with `auth.verify_token`, and then calls `enforce_scope()` - the one function you'll complete - to allow the call only if the token carries the matching `tools:<name>` scope.

<br><br>

4. Open the diff-and-merge view and build the scope check:

```
code -d ../extra/secure_server_complete.txt secure_server.py
```

The provided code already authenticates the JWT (a missing or bad token raises **401**). The piece you merge in is **`enforce_scope(claims, tool_name)`**: read the token's scopes, and raise a **403** `ToolError` if they don't include `tools:<tool_name>`. Because the check is in middleware, it protects every tool by default.

![Building the secure MCP server](./images/fd-l4-1.png?raw=true "Building the secure MCP server")

<br><br>

5. Merge `enforce_scope` into the skeleton and close the diff tab to save.

<br><br>

6. **Terminal 1 (server).** Start the FastMCP server and leave it running:

```
python secure_server.py
```

You should see `FastMCP server on http://127.0.0.1:8000/mcp/` and the list of scope-protected tools.

![Secure server running](./images/fd-l4-3.png?raw=true "Secure server running")

<br><br>

7. **Terminal 2 (client).** Open a new terminal (click the `+` in the terminal panel), then run the client:

```
cd /workspaces/ai-security/mcp
python client.py
```

The client mints a scoped JWT for each registered client and calls all three tools against the server.

✓ **Success looks like:** the client prints three passes — **no-auth** → every call `401`; **full-client** → `add`, `multiply`, `divide` all succeed; **limited-client** → `add` succeeds but `multiply` and `divide` are **DENIED (403)**. If `limited-client` is allowed to multiply or divide, `enforce_scope` didn't merge — stop the server (Ctrl+C in Terminal 1), reopen the diff at Step 4, finish it, and restart the server.

<br><br>

8. Watch the output. First, the **no-auth** run (no token) is rejected on every call with **401 Unauthorized: missing bearer token** - an unauthenticated call never reaches a tool.

<br><br>

9. Then the client runs as each registered client:
   - **full-client**: `add`, `multiply`, and `divide` all succeed
   - **limited-client**: `add` succeeds, but `multiply` and `divide` are **DENIED (403)** because the token only carries the `tools:add` scope

This is per-tool authorization - the same server, different access levels driven entirely by signed token scopes. Look at the **server** terminal too: it logs each allowed call (`[SECURE] full-client -> multiply (allowed)`).

![Scope enforcement in action](./images/fd-l4-4.png?raw=true "Scope enforcement in action")

<br><br>

10. (Optional) Inspect what's actually inside a token. In Terminal 2:

```
python -c "import auth; print(auth.verify_token(auth.mint_token('limited-client')))"
```

You'll see `'scope': 'tools:add'` - confirming the limited client's token never carries the multiply/divide scopes, so the server can't be tricked into running them.

<br><br>

11. When you're done, stop the server with **Ctrl+C** in Terminal 1.

<br><br>

**Key Takeaways:**
- **Authenticate every MCP call** - an unauthenticated tool call should never reach your tools.
- **Scope tokens per tool** - least privilege means a client gets exactly the tools it needs and nothing more.
- **Enforce in middleware** - centralizing the scope check keeps every tool protected by default.
- **Restrict the manifest** - only expose the tools a client population actually needs.

<p align="center">
<b>[END OF LAB]</b>
</p>
<br><br>

**Lab 6: Auditing and Observability for Agents**

**Purpose: In this lab, we'll make an AI agent observable using real OpenTelemetry. We'll wrap every tool call in an OTel span - trace IDs, span IDs, attributes, status - under one session trace, then run an anomaly detector over the captured spans to surface suspicious tool-call patterns. You can't defend what you can't see.**

> **New terms in this lab (skip if you've used tracing before):** **observability** just means being able to see what your system actually did. **OpenTelemetry (OTel)** is the industry-standard library for recording that. A **span** is one timed record of one operation — like a log line with a stopwatch and a label (think "logged: agent called export_employee_data for mallory, status=denied, 12ms"). A **trace** ties together all the spans from one session, via a shared **trace ID**, so you can see the whole sequence; each span also has its own **span ID**. Real systems ship these to tools like Jaeger or a SIEM; here we keep them in memory so we can inspect them right away.

<br>

1. From the terminal, change to the *observability* directory:

```
cd /workspaces/ai-security/observability
```

<br><br>

2. Open the skeleton and review its shape:

```
code observable_agent.py
```

Note the `REQUESTS` list of natural-language `(user, request)` pairs and the `SENSITIVE_TOOLS` set (`export_employee_data`, `send_company_email`, `update_salary`). A **real model** drives the agent: `choose_tool()` asks it (with `prefer="strong"`) to pick one tool per request and return JSON. The provided `build_tracer()` sets up a real **OpenTelemetry** tracer with an in-memory span exporter. Some requests are benign; `mallory` issues a burst of bulk-export requests and `bob` asks for a mass email - your instrumentation has to make all of that visible.

<br><br>

3. Open the diff-and-merge view to add the instrumentation and detector:

```
code -d ../extra/observable_agent_complete.txt observable_agent.py
```

![Building the observable agent](./images/fd-l5-1.png?raw=true "Building the observable agent")

<br><br>

4. Review the two pieces you're completing in the complete version:
   - **`instrument_call`** - opens an OpenTelemetry span (`tracer.start_as_current_span`) around the model's tool choice, sets attributes on it (`user`, `tool`, `args`, `sensitive`, `status`), marks unauthorized calls with an ERROR status, and prints a compact `[AUDIT]` line with the span's real `trace_id` / `span_id`.
   - **`detect_anomalies`** - reads the **captured spans** (from the in-memory exporter) and flags denied calls, sensitive-tool bursts (3+ of the same call), and any user touching sensitive tooling.

   The simple authorization stub (`authorize`, only `alice` may call sensitive tools) and the OTel setup are already provided.

<br><br>

5. Merge all sections into the skeleton and close the diff tab to save.

<br><br>

6. Run the observable agent:

```
python observable_agent.py
```

✓ **Success looks like:** a stream of `[AUDIT]` lines (one per request), each carrying a `trace=` and `span=` id, followed by a **TELEMETRY SUMMARY** and an **ANOMALY DETECTION** block that flags `mallory`'s denied exports, a **BURST**, and the users who touched sensitive tooling. If you see `NotImplementedError` or no anomaly findings, a function didn't merge — reopen the `code -d` diff and finish it.

<br><br>

7. Look at the stream of **`[AUDIT]`** lines (one per request, after the model picks a tool). Every call is a real OpenTelemetry span sharing a single **trace_id** for the session, each with its own **span_id** - the same trace/span model you'd export to Jaeger, Tempo, or a SIEM. (Tool choices come from a real model, so the exact split of tools may vary slightly run to run.)

![Structured audit stream](./images/fd-l5-2.png?raw=true "Structured audit stream")

<br><br>

8. Look at the **TELEMETRY SUMMARY** - tool spans, sensitive calls, and denied calls, all read back from the captured OpenTelemetry spans. These are the kind of metrics you'd graph on a dashboard.

<br><br>

9. Look at the **ANOMALY DETECTION** section. The detector flags `mallory`'s denied export attempts, the **BURST** of three rapid export calls, and surfaces every user who touched sensitive tooling for review.

![Anomaly detection](./images/fd-l5-3.png?raw=true "Anomaly detection")

<br><br>

10. (Optional) Add a new `(user, request)` pair to the `REQUESTS` list (for example, another `mallory` export request, or a benign question), or add a tool name to `SENSITIVE_TOOLS`, then re-run and watch the telemetry and anomaly findings change.

<br><br>

**Key Takeaways:**
- **Instrument every tool call** - structured logs with trace and span IDs make agent behavior auditable and explainable.
- **Telemetry feeds both ops and security** - the same spans power latency dashboards and intrusion detection.
- **Detect patterns, not just events** - bursts and denied-call clusters reveal abuse that any single line wouldn't.
- **Audit trails enable incident response** - forensics depends on having recorded what happened.

<p align="center">
<b>[END OF LAB]</b>
</p>
<br><br>

**Lab 7: Adversarial Testing and Red-Teaming**

**Purpose: In this lab, we'll red-team an AI agent. We'll fire a battery of adversarial prompts - prompt injection, goal hijacking, data exfiltration, system-prompt leakage, and context poisoning - at a target agent, score which attacks succeed, then build a defense and re-run to prove the attacks are neutralized without breaking legitimate use.**

<br>

1. From the terminal, change to the *redteam* directory:

```
cd /workspaces/ai-security/redteam
```

<br><br>

2. Open the attack suite and review it:

```
code attacks.py
```

The target is a **real model** acting as an HR assistant. Its system prompt contains a confidential secret (an SSN, `123-45-6789`) it is told never to reveal. Each attack tries a different technique to extract that secret or leak the system prompt - direct ask, prompt injection, a role-play jailbreak, context poisoning, and a "repeat your instructions" leak. The `success_marker` for each is the secret itself: if it appears in the response, the attack **succeeded**. The `BENIGN` case (a normal PTO question) must keep working. A good defense makes the secret stop leaking while leaving the benign case intact.

<br><br>

3. Open the target agent skeleton:

```
code target_agent.py
```

Note that, as shipped, `is_blocked()` returns `False` for everything - the agent is **undefended**, so every attack prompt reaches the real model. `model_reply()` sends the prompt straight to the model (with the secret in its system prompt), so the input filter is the only thing standing between an attacker and the secret.

<br><br>

4. Run the red-team harness against the **undefended** agent:

```
python redteam_runner.py
```

✓ **At this point (attacks landing):** the scorecard shows one or more rows marked **VULNERABLE** and a non-zero `Compromised:` count, while the `BENIGN` row shows **PASS**. How many leak varies by model — that's expected, and it's the point.

<br><br>

5. Look at the scorecard. You'll typically see several attacks marked **VULNERABLE** - the undefended model leaked the secret SSN under one or more techniques. The `BENIGN` request still **PASSes**. (How many leak depends on the model: smaller models like `llama3.2:3b` tend to give the secret up more readily, which is itself the lesson - never rely on the model's own restraint.) The summary reports a non-zero `Compromised:` count.

![Undefended red-team run](./images/fd-l6-1.png?raw=true "Undefended red-team run")

<br><br>

6. Now build the defense. Open the diff-and-merge view:

```
code -d ../extra/target_agent_complete.txt target_agent.py
```

![Building the defense](./images/fd-l6-2.png?raw=true "Building the defense")

<br><br>

7. Review the defense in the complete version: the `HIJACK_PATTERNS` (ignore/forget instructions, "you are now ...bot," override claims, "repeat everything above," "system prompt / hidden notes," role-play), the `RESTRICTED_INTENT` patterns (any `ssn` / social-security request, export, send-to-all-staff), and the `is_blocked()` function that screens every prompt before it reaches the model.

<br><br>

8. Merge all sections into the skeleton and close the diff tab to save.

<br><br>

9. Re-run the **same** red-team harness against the now-defended agent:

```
python redteam_runner.py
```

✓ **Success looks like:** every attack row now shows **DEFENDED**, the summary reads `Compromised: 0` with `[OK] All attacks defended and legitimate use preserved.`, and the `BENIGN` row still **PASSes**. If any attack still shows **VULNERABLE**, the input filter didn't fully merge — reopen the diff at Step 6.

<br><br>

10. Look at the scorecard again. All five attacks are now **DEFENDED** - each manipulative prompt is blocked at the input filter before it ever reaches the model, so the secret can't leak. The benign request still **PASSes**, and the summary reports `Compromised: 0` with `[OK] All attacks defended and legitimate use preserved.` This is the core red-team loop: measure, mitigate, re-measure.

![Defended red-team run](./images/fd-l6-3.png?raw=true "Defended red-team run")

<br><br>

11. (Optional challenge) Try to beat your own defense. Add a new attack to `attacks.py` (for example, a base64-encoded or politely-worded injection) and re-run. If it gets through, that's the point - no single filter is complete, which is why red-teaming is continuous and defenses are layered.

<br><br>

**Key Takeaways:**
- **Red-teaming is measurement** - you can't claim an agent is safe until you've attacked it and scored the results.
- **Keep a benign control** - a defense that blocks legitimate use is a failed defense.
- **Measure, mitigate, re-measure** - the loop turns "we added some filters" into evidence.
- **Defenses are layered and never final** - new attacks emerge, so red-teaming is a continuous practice, not a one-time gate.

<p align="center">
<b>[END OF LAB]</b>
</p>
<br><br>

**Lab 8: Policy-Driven Governance**

**Purpose: In this lab, we'll govern an agent with "security as code." Instead of burying rules in application logic, we'll define allowed tools, query types, data scopes, and rate limits in a versioned policy file, and enforce that policy at runtime on every request. Changing the security posture becomes a config change, not a code change.**

<br>

1. From the terminal, change to the *governance* directory:

```
cd /workspaces/ai-security/governance
```

<br><br>

2. Open the policy file and read it:

```
code security_policy.yaml
```

This is the single source of truth for what the agent may do: an `allowed_tools` allowlist, a `denied_tools` blocklist, permitted `allowed_query_types`, `data_scopes` (PII access on/off, in-scope departments), and `limits` (max requests per session). Notice there is no application logic here - just policy.

<br><br>

3. Open the policy engine skeleton:

```
code policy_engine.py
```

The engine loads the YAML and exposes a `check(req)` method that every request must pass before any tool runs.

<br><br>

4. Open the diff-and-merge view to implement the enforcement logic:

```
code -d ../extra/policy_engine_complete.txt policy_engine.py
```

![Building the policy engine](./images/fd-l7-1.png?raw=true "Building the policy engine")

<br><br>

5. Review the `check()` method in the complete version. It enforces, in order: the **rate limit**, the **tool deny-list then allow-list**, the **query-type allow-list**, and the **data scopes** (block PII access when `allow_pii` is false, block out-of-scope departments). Each rejection returns a clear reason.

<br><br>

6. Merge all sections into the skeleton and close the diff tab to save.

<br><br>

7. Run the governed agent:

```
python policy_engine.py
```

✓ **Success looks like:** the six requests print with **[ALLOW]** on the two benign ones (each followed by a `-> model:` reply) and **[DENY]** on the other four, each denial naming the rule it hit (denied tool, PII scope, out-of-scope department); the summary reads `Allowed: 2   Denied: 4`. If everything is allowed or you see `NotImplementedError`, the `check()` logic didn't merge — reopen the diff at Step 4.

Each of the six requests is evaluated against the policy *before* anything else happens. **ALLOW**ed requests are then sent to a real model (you'll see `-> model:` with its reply); **DENY**ed requests never reach the model at all, and each denial reason maps directly to a rule in the YAML (denied tool, PII scope, out-of-scope department). The first allowed request includes a brief model warm-up.

![Policy decisions](./images/fd-l7-2.png?raw=true "Policy decisions")

<br><br>

8. Now change the policy *without touching any code*. Open `security_policy.yaml`, find `data_scopes:` and change `allow_pii: false` to `allow_pii: true`. Save the file.

```
code security_policy.yaml
```

<br><br>

9. Re-run the agent:

```
python policy_engine.py
```

The **Read SSN** request that was previously denied is now **ALLOWed** - the behavior changed because the *policy* changed, not the application. This is the essence of security as code.

![Policy change takes effect](./images/fd-l7-3.png?raw=true "Policy change takes effect")

<br><br>

10. Try one more policy change. In `security_policy.yaml`, set `max_requests_per_session: 3`, save, and re-run. Now the later requests are denied with `rate limit exceeded for session` - runtime governance enforced straight from the policy file. (Set `allow_pii` back to `false` and the limit back to `6` when you're done if you want the original behavior.)

<br><br>

**Key Takeaways:**
- **Security as code is auditable and reviewable** - policy lives in a versioned file you can diff, review, and roll back.
- **Separate policy from logic** - changing the security posture shouldn't require changing (or redeploying) application code.
- **Enforce at runtime, on every request** - a policy is only as good as the checkpoint that applies it.
- **One file, many controls** - tools, query types, data scopes, and rate limits governed in one place reduce the chance of a gap.

<p align="center">
<b>[END OF LAB]</b>
</p>
<br><br>

**Capstone Demo: Secure Deployment and Lifecycle Management**

**Purpose: In this capstone, we'll apply DevSecOps practices to an AI service before it ships. We'll build a pre-deployment security gate that scans for hardcoded secrets, lints the Dockerfile, checks dependencies against known CVEs, signs the release artifact, and enforces a compliance gate - blocking the release if any control fails, exactly as it would in a CI/CD pipeline.**

<br>

1. From the terminal, change to the *deploy* directory:

```
cd /workspaces/ai-security/deploy
```

<br><br>

2. Examine the artifacts we're about to ship. They intentionally contain problems. Open the app, the Dockerfile, and the dependency list:

```
code app/app.py Dockerfile app/requirements_app.txt
```

Notice the **hardcoded secrets** in `app.py`, the Dockerfile using **`FROM python:latest`** with **no `USER` directive** (runs as root), and **outdated dependency versions** in the requirements file.

![Reviewing the deployment artifacts](./images/fd-l8-1.png?raw=true "Reviewing the deployment artifacts")

<br><br>

3. Look at the two data files the gate uses:

```
code cve_db.json compliance_rules.json
```

`cve_db.json` is a small offline vulnerability database (no network needed). `compliance_rules.json` lists the **required controls**, each marked blocking - every one must pass before release.

<br><br>

4. Open the security gate skeleton:

```
code security_gate.py
```

The scanners are stubbed out. You'll implement secret scanning, Dockerfile linting, dependency CVE scanning, and artifact signing.

<br><br>

5. Open the diff-and-merge view to implement the scanners:

```
code -d ../extra/security_gate_complete.txt security_gate.py
```

![Building the security gate](./images/fd-l8-2.png?raw=true "Building the security gate")

<br><br>

6. Review the four scanners in the complete version:
   - **`scan_secrets`** - greps the app source for API-key, password, and AWS-key patterns
   - **`lint_dockerfile`** - flags an unpinned base image and a missing `USER` directive
   - **`scan_dependencies`** - compares each pinned dependency version against the CVE database
   - **`sign_artifact`** - hashes the app tree (SHA-256), produces an HMAC signature, and writes a `release_manifest.json`

<br><br>

7. Merge all sections into the skeleton and close the diff tab to save.

<br><br>

8. Run the security gate:

```
python security_gate.py
```

✓ **Success looks like:** the report lists four **[FAIL]** controls (hardcoded secrets, root container, unpinned base image, HIGH-severity CVEs) and one **[PASS]** (signed artifact), ending `Blocking failures: 4` and `RESULT: DEPLOYMENT BLOCKED`. If every control PASSes on this first run, a scanner didn't merge — reopen the diff at Step 5.

<br><br>

9. Look at the gate report. Four blocking controls **FAIL**: hardcoded secrets, root container, unpinned base image, and HIGH-severity dependency CVEs. The artifact is signed (you'll see the SHA-256 and signature, and a `release_manifest.json` is written), but the final result is **DEPLOYMENT BLOCKED**. (Run `echo $?` to confirm the non-zero exit code a pipeline would catch.)

![Deployment blocked](./images/fd-l8-3.png?raw=true "Deployment blocked")

<br><br>

10. Now remediate the findings. Make these fixes:
   - In `app/app.py`, replace the hardcoded `API_KEY`/`DB_PASSWORD` with `os.environ.get(...)` lookups.
   - In `Dockerfile`, pin the base image (for example `FROM python:3.12-slim`) and add a non-root user (`RUN useradd -m appuser` and `USER appuser`).
   - In `app/requirements_app.txt`, bump the versions past the fixes listed in `cve_db.json` (for example `requests==2.32.0`, `pyyaml==6.0.1`, `flask==2.2.5`).

<br><br>

11. Re-run the gate:

```
python security_gate.py
```

✓ **Success looks like:** all five controls show **[PASS]** and the result is **CLEARED FOR RELEASE** with a zero exit code (`echo $?` → `0`). If it's still **DEPLOYMENT BLOCKED**, one of the three fixes in Step 10 is incomplete — the named failing control tells you which file to revisit.

All five controls now **PASS** and the result is **CLEARED FOR RELEASE** with a zero exit code. The same gate that blocked the insecure build now lets the hardened one through.

![Cleared for release](./images/fd-l8-4.png?raw=true "Cleared for release")

<br><br>

**Key Takeaways:**
- **Shift security left** - catch secrets, bad base images, and vulnerable dependencies before they ship, not after.
- **Make the gate blocking** - a non-zero exit code in CI/CD is what actually stops an insecure release.
- **Sign your artifacts** - a hash plus signature gives you integrity and provenance for what you deploy.
- **Compliance as a gate, not a document** - encoding required controls as automated checks keeps every release honest.

<p align="center">
<b>[END OF LAB]</b>
</p>
<br><br>

<p align="center">
<b>For educational use only by the attendees of our workshops.</b>
</p>

<p align="center">
<b>(c) 2026 Tech Skills Transformations and Brent C. Laster. All rights reserved.</b>
</p>


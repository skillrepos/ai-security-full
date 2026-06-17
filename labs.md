# AI Security for Developers and Practitioners (Full Day)
## Building safe, trustworthy, and resilient AI systems
## Session labs
## Revision 2.1 - 06/12/26


**Follow the startup instructions in the README.md file IF NOT ALREADY DONE!**

**NOTE: To copy and paste in the codespace, you may need to use keyboard commands - CTRL-C and CTRL-V. Chrome may work best for this.**

**Models used in these labs:** Labs 2, 3, 5, 6, and 7 use a real language model so you can watch genuine model behavior (and genuine attacks). A shared helper, `common/llm.py`, routes each lab to the right backend:

- **Ollama `llama3.2:3b`** runs locally in your Codespace and is the default. The setup script pulls it for you; the first query of a session includes a one-time model warm-up of about 30-60 seconds.
- **Groq** (optional, free, and much faster) is used for **all five** model labs whenever you set a `GROQ_API_KEY` - `llama-3.1-8b-instant` for the "fast" labs and `llama-3.3-70b-versatile` for the "strong" ones (Labs 2 and 5). Without a key, the labs use Ollama automatically. See the README for the one-minute Groq setup.

You can force a backend for any lab with an environment variable, e.g. `export LLM_BACKEND=ollama` (or `groq`, or `mock` for an offline, deterministic stand-in). Because these labs use a real model, **exact wording will vary from run to run** — the lab notes describe what to look for, not an exact transcript.

Labs 1, 4, and 8 use no model at all (threat modeling, MCP auth, and deploy-time scanning have no model in the loop). The only Python dependency is PyYAML (Lab 7), installed during setup.

<br><br>

**Lab 1: Mapping AI Security Risks**

**Purpose: In this lab, we'll perform a structured threat model of an AI system. We'll map every component (LLM, RAG, agent, MCP tools) to the OWASP Top 10 for LLM Applications (2025), score the attack surface, and pinpoint where the highest-risk vulnerabilities and trust-boundary crossings occur.**

<br>

1. From the terminal, change to the *threat-model* directory:

```
cd /workspaces/ai-security/threat-model
```

<br><br>

2. First, examine the description of the system we are going to threat-model. Open the architecture file and read through it:

```
code architecture.json
```

This describes the **OmniTech Customer Support AI Assistant**. Notice the three parts: a list of **components** (each with a type, a trust zone, and whether it handles PII), the **data flows** between them, and the **trust boundaries** (the internet edge and the app-to-data boundary).

![Examining the architecture](./images/fd-l1-1.png?raw=true "Examining the architecture")

<br><br>

3. Now look at the risk catalog we'll map against. Open it and skim the entries:

```
code owasp_llm.py
```

This is the **OWASP Top 10 for LLM Applications (2025)**. Each risk lists the component *types* it typically applies to (for example, `LLM06 Excessive Agency` applies to `agent`, `tool`, and `mcp`). The `COMPONENT_EXPOSURE` table assigns a likelihood weight to each component type.

<br><br>

4. The threat-model engine is provided as a skeleton with the core logic removed. Open the diff-and-merge view to compare the skeleton with the complete reference:

```
code -d ../extra/threat_model_complete.txt threat_model.py
```

As you review, note the four functions you are completing:
   - **`map_risks`** - filters the OWASP catalog to the risks that apply to a component's type
   - **`score`** - computes a risk score (likelihood x impact), boosting Sensitive Disclosure (LLM02) and Excessive Agency (LLM06), and assigns a HIGH/MEDIUM/LOW band
   - **`find_boundary_crossings`** - flags any data flow whose two endpoints sit in different trust zones
   - **`build_threat_model`** - walks every component x applicable-risk pair and collects the scored rows

![Merging the threat model engine](./images/fd-l1-2.png?raw=true "Merging the threat model engine")

<br><br>

5. Merge each section from the complete version (left) into the skeleton (right) by clicking the arrows in the middle bar. When no differences remain, close the diff tab to save.

<br><br>

6. Run the threat model:

```
python threat_model.py
```

<br><br>

7. Look at the **threat model table**. It is sorted by score, highest first. Notice that the `support_agent` component dominates the top of the list with multiple **HIGH** rows - an agent that can act autonomously and call tools is the largest attack surface in this system.

![Threat model output](./images/fd-l1-3.png?raw=true "Threat model output")

<br><br>

8. Look at the **TRUST BOUNDARY CROSSINGS** section. These are the data flows that move between trust zones (for example, `web_ui -> chat_llm` crosses the internet edge). These crossings are where you should concentrate your strongest controls.

<br><br>

9. Finally, review the **TOP 5 RISKS TO MITIGATE FIRST**. This is the prioritized list you would hand to an engineering team - it tells them exactly which risk, on which component, to address first.

<br><br>

10. (Optional) Threat models change as the system changes. Open `architecture.json`, find the `account_tool` component, and change its `"handles_pii"` value from `true`... or add a brand-new component such as `{"id": "audit_log", "type": "datastore", "trust_zone": "internal", "handles_pii": true}` to the components list. Save, then re-run `python threat_model.py` and watch the scores and rankings update.

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

**Lab 2: Securing Prompts and Contexts**

**Purpose: In this lab, we'll defend a RAG pipeline against document poisoning. We'll see how a malicious document injected into the knowledge base can hijack the model with hidden instructions and phish users, then implement defensive layers - source allowlisting, injection detection, relevance filtering, and output scanning - to neutralize the attack.**

<br>

1. From the terminal, change to the *rag* directory:

```
cd /workspaces/ai-security/rag
```

<br><br>

2. Examine the poisoned document that simulates what an attacker might inject into a knowledge base. Open it and read through it carefully:

```
code docs/OmniTech_Security_Bulletin.txt
```

This looks like a legitimate OmniTech bulletin, but it carries three attacks: a hidden `[SYSTEM OVERRIDE]` **prompt injection**, a **phishing URL** (`https://omnitech-secure-verify.com/reset`), and a **social-engineering** instruction to email full credit card numbers for "refund verification."

![The poisoned document](./images/fd-l2-1.png?raw=true "The poisoned document")

<br><br>

3. Look at the retrieval helpers used by both versions of the lab:

```
code kb.py
```

`kb.py` loads the documents, retrieves the most relevant chunks by keyword overlap, and sends them to a **real model** (`rag_answer`, which uses `prefer="strong"` - Groq's 70B model if you have a key, otherwise Ollama). Notice the system prompt tells the model to answer **using only the retrieved context** and to include any URL or instruction it finds there - which is exactly why a poisoned chunk reaching this stage is dangerous. (The first query includes a ~30-60s model warm-up.)

<br><br>

4. Run the **vulnerable** RAG system - this is RAG with no security defenses:

```
python rag_vulnerable.py
```

You'll see the knowledge base load, including the poisoned source mixed in with the two legitimate documents.

![Loading the knowledge base](./images/fd-l2-2.png?raw=true "Loading the knowledge base")

<br><br>

5. At the prompt, ask:

```
How do I reset my password?
```

Watch the **SOURCES** and **ANSWER**. The poisoned `OmniTech_Security_Bulletin_2024.pdf` appears as a source, and the answer hands the user the **phishing URL** from the poisoned document.

![Phishing URL in the answer](./images/fd-l2-3.png?raw=true "Phishing URL in the answer")

<br><br>

6. Now ask:

```
How do I get a refund?
```

The poisoned document's instruction to share a full credit card number surfaces in the response. The vulnerable system trusts all retrieved context equally. Type `quit` to exit.

<br><br>

7. Now let's add defenses. Open the diff-and-merge view to compare the skeleton with the complete hardened version:

```
code -d ../extra/rag_hardened_complete.txt rag_hardened.py
```

![Building the hardened version](./images/fd-l2-4.png?raw=true "Building the hardened version")

<br><br>

8. Examine the `SecurityGuard` class in the complete version (left side). It implements four layers of defense in depth:
   - **Source allowlist** - only chunks from known, verified PDFs are trusted (the poisoned bulletin is not on the list)
   - **Injection detection** - regex patterns catch `[SYSTEM OVERRIDE]`, `ignore previous instructions`, `supersedes all previous`, etc.
   - **Relevance threshold** - low-confidence chunks are dropped
   - **Output scanning** - the final answer is scrubbed of phishing domains and sensitive-data requests

Note the `filter_chunks()` and `scan_output()` methods - these are the two checkpoints that block bad input and redact bad output.

<br><br>

9. Merge all sections from the complete version (left) into the skeleton (right). When no differences remain, close the diff tab to save.

<br><br>

10. Run the hardened version against the same poisoned knowledge base:

```
python rag_hardened.py
```

Notice the startup output now labels each source `[TRUSTED]` or `[UNKNOWN]`.

![Trusted vs unknown sources](./images/fd-l2-5.png?raw=true "Trusted vs unknown sources")

<br><br>

11. Ask the same two questions again:

```
How do I reset my password?
```
```
How do I get a refund?
```

This time the poisoned chunks are blocked at the source-allowlist stage, and any sensitive request that slips into the output is redacted. The answers now come only from the legitimate handbook and returns policy. Type `report` to see every security event, then `quit` to exit.

![Blocked and redacted](./images/fd-l2-6.png?raw=true "Blocked and redacted")

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

Notice the two families of guards. **Input guards** (`guard_jailbreak`, `guard_topic`, `guard_length`) screen the user's request. **Output guards** (`guard_pii`, `guard_banned`) screen the model's response. Each guard returns `(ok, reason, fixed_text)` - if a guard returns fixed text, the pipeline *repairs* the content and continues; if it returns `None`, the content is *blocked*. This is the same idea production frameworks implement, just distilled to its essentials.

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

<br><br>

Each request now flows through the full pipeline: **INPUT guards -> real model -> OUTPUT guards**. The first request includes a brief model warm-up.

<br><br>

8. Look at the requests that are stopped at the **input** stage. The legitimate password question passes input screening and is sent to the model. The jailbreak attempt, the off-topic poem request, and the oversized input are each marked **INPUT BLOCKED (never reached the model)**, with the triggering guard named - those prompts never cost you a model call.

![Input guard results](./images/fd-l3-2.png?raw=true "Input guard results")

<br><br>

9. Look at what happens on the **output** side for requests that did reach the model. The benign answer is **DELIVERED (PASS)**. The last request feeds the model a record containing an SSN and a card number; when the model echoes them back, the output guard redacts the PII and the result is **DELIVERED (FIXED)** with `[SSN-REDACTED]` / `[CARD-REDACTED]` in place. (Exact wording varies by model; the redactions do not.)

![Output guard results](./images/fd-l3-3.png?raw=true "Output guard results")

<br><br>

10. (Optional) Add your own guard or pattern. For example, add a phone-number pattern to `PII_PATTERNS`, or add a new prompt to the `inputs` list in `main()`, then re-run to see your guard fire against real model output.

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

**Lab 4: Hardening MCP Servers and Tools**

**Purpose: In this lab, we'll harden a Model Context Protocol (MCP) server. An authorization server issues scoped JWT access tokens, and the MCP server enforces per-tool scope checks in middleware - so the same server grants different clients access to different subsets of tools, following least privilege.**

**This lab uses three terminals: an authorization server, an MCP server, and a client.**

<br>

1. From the terminal, change to the *mcp* directory:

```
cd /workspaces/ai-security/mcp
```

<br><br>

2. Review the two provided (complete) files. Open the JWT helper and the authorization server:

```
code jwt_util.py auth_server.py
```

`jwt_util.py` is a minimal HMAC-signed JWT implementation (no external dependencies). In `auth_server.py`, note the **client registry**: `full-client` is granted scopes for all three tools (`tools:add`, `tools:multiply`, `tools:divide`), while `limited-client` is granted only `tools:add`. The granted scopes are embedded in the token's `scope` claim.

<br><br>

3. Now harden the MCP server. Open the diff-and-merge view:

```
code -d ../extra/secure_server_complete.txt secure_server.py
```

![Building the secure MCP server](./images/fd-l4-1.png?raw=true "Building the secure MCP server")

<br><br>

4. Review the security middleware in the complete version:
   - **`_authenticate`** - reads the `Authorization` header and verifies the Bearer JWT; a missing or invalid token yields **401**
   - **Per-tool scope enforcement** - for a `tools/call`, the server checks that the token's scopes include `tools:<name>`; if not, it returns **403** with a clear message
   - **Restricted manifest** - only `add`, `multiply`, and `divide` are exposed

Merge all sections into the skeleton and close the diff tab to save.

<br><br>

5. **Terminal 1 (auth server).** Start the authorization server and leave it running:

```
python auth_server.py
```

You should see `authorization server on http://127.0.0.1:9000`.

![Auth server running](./images/fd-l4-2.png?raw=true "Auth server running")

<br><br>

6. **Terminal 2 (MCP server).** Open a new terminal (click the `+` in the terminal panel), then:

```
cd /workspaces/ai-security/mcp
python secure_server.py
```

You should see `secure MCP server on http://127.0.0.1:8000` and the list of exposed tools. Leave it running.

![Secure server running](./images/fd-l4-3.png?raw=true "Secure server running")

<br><br>

7. **Terminal 3 (client).** Open a third terminal, then:

```
cd /workspaces/ai-security/mcp
python client.py
```

<br><br>

8. Watch the output. First, an unauthenticated `tools/list` is rejected with **401 Missing or invalid token**.

<br><br>

9. Then the client runs as each registered client:
   - **full-client**: `add`, `multiply`, and `divide` all succeed
   - **limited-client**: `add` succeeds, but `multiply` and `divide` are **DENIED (403)** because the token only carries the `tools:add` scope

This is per-tool authorization - the same server, different access levels driven entirely by token scopes.

![Scope enforcement in action](./images/fd-l4-4.png?raw=true "Scope enforcement in action")

<br><br>

10. (Optional) In Terminal 3, inspect a token's scopes directly:

```
TOKEN=$(curl -s -X POST -d "username=limited-client&password=limitedpass" http://127.0.0.1:9000/token | python3 -c "import sys,json;print(json.load(sys.stdin)['access_token'])")
curl -s -X POST http://127.0.0.1:9000/introspect -H "Content-Type: application/json" -d "{\"token\":\"$TOKEN\"}"
```

You'll see `"scope": "tools:add"` - confirming the limited client never receives the multiply/divide scopes.

<br><br>

11. When you're done, stop both servers with **Ctrl+C** in Terminal 1 and Terminal 2.

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

**Lab 5: Auditing and Observability for Agents**

**Purpose: In this lab, we'll make an AI agent observable. We'll wrap every tool call in structured telemetry - trace IDs, span IDs, timing, and JSON audit lines - and then run an anomaly detector over the audit stream to surface suspicious tool-call patterns. You can't defend what you can't see.**

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

Note the `REQUESTS` list of natural-language `(user, request)` pairs and the `SENSITIVE_TOOLS` set (`export_employee_data`, `send_company_email`, `update_salary`). A **real model** drives the agent: `choose_tool()` asks it (with `prefer="strong"`) to pick one tool per request and return JSON. Some requests are benign; `mallory` issues a burst of bulk-export requests and `bob` asks for a mass email - your telemetry has to make all of that visible.

<br><br>

3. Open the diff-and-merge view to add the telemetry and detector:

```
code -d ../extra/observable_agent_complete.txt observable_agent.py
```

![Building the observable agent](./images/fd-l5-1.png?raw=true "Building the observable agent")

<br><br>

4. Review the three pieces you're completing in the complete version:
   - **`Telemetry.record`** - builds a structured event (trace id, span id, user, tool, args, status, latency, sensitive flag), prints it as a JSON `[AUDIT]` line, and stores it
   - **`handle_request`** - times the model's tool choice (`choose_tool`), applies a simple authorization stub (only `alice` may call sensitive tools), and records a span
   - **`detect_anomalies`** - flags denied calls, sensitive-tool bursts (3+ of the same call), and any user touching sensitive tooling

<br><br>

5. Merge all sections into the skeleton and close the diff tab to save.

<br><br>

6. Run the observable agent:

```
python observable_agent.py
```

<br><br>

7. Look at the stream of **`[AUDIT]`** lines (one per request, after the model picks a tool). Every call emits one structured JSON record sharing a single **trace_id** for the session, each with its own **span_id** and a real `latency_ms`. This is exactly the shape you'd ship to a SIEM or tracing backend. (Tool choices come from a real model, so the exact split of tools may vary slightly run to run.)

![Structured audit stream](./images/fd-l5-2.png?raw=true "Structured audit stream")

<br><br>

8. Look at the **TELEMETRY SUMMARY** - total spans, sensitive calls, denied calls, and average latency. These are the metrics you'd graph on a dashboard.

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

**Lab 6: Adversarial Testing and Red-Teaming**

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

**Lab 7: Policy-Driven Governance**

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

**Lab 8: Secure Deployment and Lifecycle Management**

**Purpose: In this lab, we'll apply DevSecOps practices to an AI service before it ships. We'll build a pre-deployment security gate that scans for hardcoded secrets, lints the Dockerfile, checks dependencies against known CVEs, signs the release artifact, and enforces a compliance gate - blocking the release if any control fails, exactly as it would in a CI/CD pipeline.**

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

# Instructor Timing Guide
## AI Security for Developers and Practitioners (Full Day)
### Revision 2.0 - 06/11/26

This guide maps the eight labs and their conceptual lead-ins across a single
day. Total in-room time is about **6 hours 45 minutes** including a lunch and
two breaks. Each lab is designed to run in **10-12 minutes**; the schedule
budgets 20-25 minutes per lab block to allow for setup, discussion, and
stragglers. Adjust start time and break lengths to your audience.

The deck section that precedes each lab uses the existing slide flow
(concept slides, then a "Lab N Workflow" slide, then the "Lab N" title slide).

---

## At-a-glance schedule

| Time | Block | Minutes |
|------|-------|---------|
| 9:00 - 9:20 | Welcome, environment setup, agenda | 20 |
| 9:20 - 9:50 | Module 1: The AI security landscape (concepts) | 30 |
| 9:50 - 10:15 | **Lab 1: Mapping AI Security Risks** | 25 |
| 10:15 - 10:45 | Module 2: Prompts, context & RAG attacks (concepts) | 30 |
| 10:45 - 11:10 | **Lab 2: Securing Prompts and Contexts** | 25 |
| 11:10 - 11:20 | Break | 10 |
| 11:20 - 11:45 | Module 3: Guardrails & output validation (concepts) | 25 |
| 11:45 - 12:10 | **Lab 3: Implementing Guardrails** | 25 |
| 12:10 - 1:00 | Lunch | 50 |
| 1:00 - 1:30 | Module 4: MCP, tools & least privilege (concepts) | 30 |
| 1:30 - 1:55 | **Lab 4: Hardening MCP Servers and Tools** | 25 |
| 1:55 - 2:20 | Module 5: Observability & auditing (concepts) | 25 |
| 2:20 - 2:45 | **Lab 5: Auditing and Observability for Agents** | 25 |
| 2:45 - 2:55 | Break | 10 |
| 2:55 - 3:20 | Module 6: Adversarial testing & red-teaming (concepts) | 25 |
| 3:20 - 3:45 | **Lab 6: Adversarial Testing and Red-Teaming** | 25 |
| 3:45 - 4:05 | Module 7: Governance & security-as-code (concepts) | 20 |
| 4:05 - 4:30 | **Lab 7: Policy-Driven Governance** | 25 |
| 4:30 - 4:50 | Module 8: Secure deployment & DevSecOps (concepts) | 20 |
| 4:50 - 5:15 | **Lab 8: Secure Deployment and Lifecycle Management** | 25 |
| 5:15 - 5:30 | Wrap-up, key takeaways, Q&A | 15 |

---

## Module-to-lab mapping

**Module 1 - The AI security landscape -> Lab 1**
Why AI security is different, real incidents, the OWASP LLM Top 10 (2025),
and how to threat-model an AI system. Lab 1 turns the catalog into a scored,
prioritized threat model of a sample architecture.

**Module 2 - Prompts, context & RAG -> Lab 2**
Prompt injection (direct and indirect), hidden instructions, the RAG attack
surface, and document poisoning. Lab 2 has students attack and then defend a
RAG pipeline with defense in depth.

**Module 3 - Guardrails & output validation -> Lab 3**
Where guardrails sit, input vs. output validation, the Guardrails.ai / Llama
Guard pattern, repair vs. block. Lab 3 builds a working validator pipeline.

**Module 4 - MCP, tools & least privilege -> Lab 4**
What MCP is, the tool/agent attack surface, authentication, scoped tokens,
and least privilege. Lab 4 enforces per-tool scopes with signed JWTs.

**Module 5 - Observability & auditing -> Lab 5**
Structured logging, trace/span IDs, telemetry, and detecting suspicious tool
calls. Lab 5 instruments an agent and runs an anomaly detector over the audit
stream.

**Module 6 - Adversarial testing & red-teaming -> Lab 6**
Threat categories, building an attack battery, scoring, and the
measure-mitigate-remeasure loop. Lab 6 red-teams an agent before and after
adding a defense.

**Module 7 - Governance & security-as-code -> Lab 7**
Policy as code, runtime enforcement, allowed tools/queries/data scopes. Lab 7
governs an agent from a versioned policy file and changes behavior with config
only.

**Module 8 - Secure deployment & DevSecOps -> Lab 8**
Shifting left, secrets management, dependency/CVE scanning, artifact signing,
and compliance gates. Lab 8 builds a blocking pre-deployment security gate.

---

## Running notes

- **Half-day fallback.** If you only have a half day, run Labs 2, 4, 6, and 8
  (poisoning, MCP, red-teaming, deployment) for a complete attack-and-defend
  arc, and present the other modules as concept-only.
- **Lab 4 needs three terminals.** Remind students to `cd` into the `mcp`
  directory in each new terminal and to stop both servers (`Ctrl+C`) at the end.
- **Labs 7 and 8 end with edits.** Build in a minute for students to revert
  `security_policy.yaml` and the `deploy/` artifacts if they want a clean state.
- **Buffer is built in.** Each lab block has ~12 minutes of slack; if the room
  is moving quickly, use it for the optional/challenge steps (Labs 1, 3, 5, 6).
- **Models.** Labs 2, 3, 5, 6, and 7 use a real model. Ollama (`llama3.2:3b`)
  is pulled during Codespace creation and runs locally; the first model call of
  a session warms up for ~30-60s, so have attendees run an early lab query
  before the room is waiting on it. If attendees set a free `GROQ_API_KEY`, all
  five model labs use Groq instead (much faster, no warm-up) - 70B for Labs 2
  and 5, 8B for the rest - otherwise they fall back to Ollama automatically.
  Labs 1, 4, and 8 use no model at all.
- **Outputs vary.** Because real models are in the loop, exact wording differs
  run to run; the lab notes describe what to look for, not a fixed transcript.

---

For educational use only by the attendees of our workshops.

© 2026 Tech Skills Transformations and Brent C. Laster. All rights reserved.

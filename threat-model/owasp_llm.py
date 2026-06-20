"""
AI risk catalog for the threat-model engine. Provided complete.

Two real, current frameworks:
  * OWASP Top 10 for LLM Applications (2025) - the risk catalog.
  * MITRE ATLAS (Adversarial Threat Landscape for AI Systems) - each OWASP
    risk is tagged with the ATLAS technique id(s) that realize it, so a
    finding maps to the same knowledge base AI red teams use. ATLAS ids are
    of the form AML.T#### (see https://atlas.mitre.org/techniques).

Some OWASP risks have no clean 1:1 ATLAS technique yet (AI threat taxonomies
are still converging) - those are left empty on purpose, which is itself
worth discussing in the lab.

Each entry: id, name, short description, the component "tags" the risk applies
to, and the mapped ATLAS technique ids.
"""

# Mapping table: OWASP LLM risk -> where it applies -> MITRE ATLAS technique ids.
# How to read one row (plain English):
# "LLM01 Prompt Injection applies to llm/agent/rag/tool/ui, and maps to
# ATLAS AML.T0051, which is the prompt-injection attack technique."
OWASP_LLM_2025 = [
    {"id": "LLM01", "name": "Prompt Injection",
     "desc": "Crafted input overrides developer instructions or hijacks agent goals.",
     "applies_to": ["llm", "agent", "rag", "tool", "ui"],
     "atlas": ["AML.T0051"]},                       # LLM Prompt Injection
    {"id": "LLM02", "name": "Sensitive Information Disclosure",
     "desc": "Model or pipeline leaks PII, secrets, or proprietary data.",
     "applies_to": ["llm", "rag", "agent", "datastore", "tool"],
     "atlas": ["AML.T0057", "AML.T0024"]},          # LLM Data Leakage; Exfil via Inference API
    {"id": "LLM03", "name": "Supply Chain",
     "desc": "Compromised models, datasets, or dependencies introduce risk.",
     "applies_to": ["llm", "datastore", "deploy"],
     "atlas": ["AML.T0010"]},                        # ML Supply Chain Compromise
    {"id": "LLM04", "name": "Data and Model Poisoning",
     "desc": "Tampered training data or indexed documents corrupt behavior.",
     "applies_to": ["rag", "datastore", "llm"],
     "atlas": ["AML.T0020", "AML.T0059"]},           # Poison Training Data; Erode Dataset Integrity
    {"id": "LLM05", "name": "Improper Output Handling",
     "desc": "Unvalidated model output flows into downstream systems (XSS, SQLi, RCE).",
     "applies_to": ["llm", "agent", "tool", "ui"],
     "atlas": []},                                   # no 1:1 ATLAS technique
    {"id": "LLM06", "name": "Excessive Agency",
     "desc": "Agent has too much functionality, permission, or autonomy.",
     "applies_to": ["agent", "tool", "mcp"],
     "atlas": []},                                   # emerging ATLAS agent techniques
    {"id": "LLM07", "name": "System Prompt Leakage",
     "desc": "System prompt with secrets or rules is exposed to users.",
     "applies_to": ["llm", "agent"],
     "atlas": ["AML.T0056"]},                        # LLM Meta Prompt Extraction
    {"id": "LLM08", "name": "Vector and Embedding Weaknesses",
     "desc": "Weaknesses in RAG embeddings enable injection or cross-tenant leakage.",
     "applies_to": ["rag", "datastore"],
     "atlas": []},                                   # no 1:1 ATLAS technique
    {"id": "LLM09", "name": "Misinformation",
     "desc": "Model produces false or fabricated content trusted by users.",
     "applies_to": ["llm", "rag", "ui"],
     "atlas": ["AML.T0060", "AML.T0062"]},           # Publish/Discover LLM Hallucinations
    {"id": "LLM10", "name": "Unbounded Consumption",
     "desc": "Uncapped requests/tokens enable denial-of-wallet or DoS.",
     "applies_to": ["llm", "agent", "mcp", "tool"],
     "atlas": ["AML.T0029", "AML.T0034"]},           # Denial of ML Service; Cost Harvesting
]

# Mapping table: component type -> base likelihood score and rationale note.
# How to read one row (plain English):
# "ui has likelihood 3 because it is internet-facing, so it is treated as
# more exposed than an internal-only component like datastore."
# Likelihood/impact weights per component type (1-3 scale).
# Used to compute a simple risk score for the attack-surface matrix.
COMPONENT_EXPOSURE = {
    "ui":        {"likelihood": 3, "note": "Internet-facing entry point"},
    "llm":       {"likelihood": 2, "note": "Processes untrusted text"},
    "rag":       {"likelihood": 3, "note": "Ingests external documents"},
    "agent":     {"likelihood": 3, "note": "Acts autonomously with tools"},
    "tool":      {"likelihood": 2, "note": "Executes privileged actions"},
    "mcp":       {"likelihood": 2, "note": "Exposes tools over a protocol"},
    "datastore": {"likelihood": 1, "note": "Internal but holds sensitive data"},
    "deploy":    {"likelihood": 1, "note": "CI/CD and runtime supply chain"},
}

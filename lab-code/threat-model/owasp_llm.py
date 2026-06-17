"""
OWASP Top 10 for LLM Applications (2025) - risk catalog.
Provided complete. Used by threat_model.py to map architecture
components to known AI-specific risks.

Each entry: id, name, short description, and the component
"tags" the risk typically applies to.
"""

OWASP_LLM_2025 = [
    {"id": "LLM01", "name": "Prompt Injection",
     "desc": "Crafted input overrides developer instructions or hijacks agent goals.",
     "applies_to": ["llm", "agent", "rag", "tool", "ui"]},
    {"id": "LLM02", "name": "Sensitive Information Disclosure",
     "desc": "Model or pipeline leaks PII, secrets, or proprietary data.",
     "applies_to": ["llm", "rag", "agent", "datastore", "tool"]},
    {"id": "LLM03", "name": "Supply Chain",
     "desc": "Compromised models, datasets, or dependencies introduce risk.",
     "applies_to": ["llm", "datastore", "deploy"]},
    {"id": "LLM04", "name": "Data and Model Poisoning",
     "desc": "Tampered training data or indexed documents corrupt behavior.",
     "applies_to": ["rag", "datastore", "llm"]},
    {"id": "LLM05", "name": "Improper Output Handling",
     "desc": "Unvalidated model output flows into downstream systems (XSS, SQLi, RCE).",
     "applies_to": ["llm", "agent", "tool", "ui"]},
    {"id": "LLM06", "name": "Excessive Agency",
     "desc": "Agent has too much functionality, permission, or autonomy.",
     "applies_to": ["agent", "tool", "mcp"]},
    {"id": "LLM07", "name": "System Prompt Leakage",
     "desc": "System prompt with secrets or rules is exposed to users.",
     "applies_to": ["llm", "agent"]},
    {"id": "LLM08", "name": "Vector and Embedding Weaknesses",
     "desc": "Weaknesses in RAG embeddings enable injection or cross-tenant leakage.",
     "applies_to": ["rag", "datastore"]},
    {"id": "LLM09", "name": "Misinformation",
     "desc": "Model produces false or fabricated content trusted by users.",
     "applies_to": ["llm", "rag", "ui"]},
    {"id": "LLM10", "name": "Unbounded Consumption",
     "desc": "Uncapped requests/tokens enable denial-of-wallet or DoS.",
     "applies_to": ["llm", "agent", "mcp", "tool"]},
]

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

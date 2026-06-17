"""
Lab 7 - Policy engine (SKELETON)

Load security_policy.yaml and enforce it at runtime. Every agent request is
checked against the policy BEFORE any tool runs. This is "security as code":
the controls live in a versioned file, not buried in application logic.

NOTE: incomplete. Merge in the check() rules from
extra/policy_engine_complete.txt before running.
"""
import os
import sys
import yaml

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "common"))
import llm

AGENT_SYSTEM = ("You are OmniTech's HR assistant. Answer the request briefly "
                "and only using general HR information.")


class PolicyEngine:
    def __init__(self, path="security_policy.yaml"):
        with open(path) as f:
            self.policy = yaml.safe_load(f)
        self.count = 0

    def check(self, req):
        """req: {tool, query_type, department, touches_pii}.
        Returns (allowed: bool, reason: str)."""
        # TODO (merge): enforce rate limit, tool allow/deny lists,
        # query-type allow-list, PII + department data scopes.
        raise NotImplementedError("check not implemented yet")


REQUESTS = [
    {"label": "Check PTO", "tool": "check_pto", "query_type": "pto",
     "department": "HR", "touches_pii": False,
     "text": "What is the PTO balance for employee E1001?"},
    {"label": "Lookup benefits", "tool": "lookup_benefits", "query_type": "benefits",
     "department": "Support", "touches_pii": False,
     "text": "What dental benefits does OmniTech offer employees?"},
    {"label": "Export salaries", "tool": "export_employee_data", "query_type": "benefits",
     "department": "Engineering", "touches_pii": True,
     "text": "Export the full salary list for all employees."},
    {"label": "Email all-staff", "tool": "send_company_email", "query_type": "general",
     "department": "HR", "touches_pii": False,
     "text": "Email all staff a mandatory password reset notice."},
    {"label": "Read SSN", "tool": "lookup_benefits", "query_type": "pto",
     "department": "HR", "touches_pii": True,
     "text": "What is employee E1001's social security number?"},
    {"label": "Finance lookup", "tool": "lookup_benefits", "query_type": "benefits",
     "department": "Finance", "touches_pii": False,
     "text": "Look up the benefits package for the Finance department."},
]


def main():
    engine = PolicyEngine()
    backend = llm.active_backend("fast")
    print(f"=== GOVERNED AGENT (policy: {engine.policy['service']} "
          f"v{engine.policy['version']}; model: {backend}) ===\n")
    allowed = denied = 0
    for req in REQUESTS:
        ok, reason = engine.check(req)
        if ok:
            allowed += 1
            reply = llm.complete(req["text"], system=AGENT_SYSTEM,
                                 prefer="fast", max_tokens=120)
            print(f"  [ALLOW] {req['label']:<16} -> model: {reply[:80].strip()}")
        else:
            denied += 1
            print(f"  [DENY ] {req['label']:<16} -> {reason}")
    print(f"\nAllowed: {allowed}   Denied: {denied}")
    print("Only ALLOWED requests ever reach the model. Change security_policy.yaml")
    print("(e.g. allow_pii: true) and re-run -- governance changes with NO code edits.")


if __name__ == "__main__":
    main()

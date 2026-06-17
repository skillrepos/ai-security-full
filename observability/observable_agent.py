"""
Lab 5 - Auditing & Observability for Agents (SKELETON)

A REAL model drives the agent: for each natural-language request it picks a
tool to call. Wrap every tool call in structured telemetry -- trace id, span
id, timing, JSON audit line -- then run an anomaly detector over the audit
stream to surface suspicious tool-call patterns.

NOTE: incomplete. Merge in Telemetry.record, handle_request, and
detect_anomalies from extra/observable_agent_complete.txt before running.
"""
import json
import os
import re
import sys
import time
import uuid

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "common"))
import llm

TOOLS = ["lookup_benefits", "check_pto", "export_employee_data", "send_company_email"]
SENSITIVE_TOOLS = {"export_employee_data", "send_company_email", "update_salary"}

TOOL_SYSTEM = (
    "You are an HR agent that selects exactly ONE tool to handle each request. "
    "Available tools: lookup_benefits, check_pto, export_employee_data, "
    "send_company_email. Respond with ONLY a JSON object of the form "
    '{"tool": "<tool_name>", "args": {...}} and no other text.'
)

REQUESTS = [
    ("alice", "What are my dental benefits?"),
    ("alice", "How many PTO days does employee E1001 have?"),
    ("mallory", "Export all employee records from the Engineering department."),
    ("mallory", "Now export the Sales team's records too."),
    ("mallory", "And export the Finance department records as well."),
    ("bob", "Send an email to all-staff announcing a mandatory password reset."),
    ("alice", "What benefits does employee E1002 have?"),
]


def choose_tool(request):
    """Ask the real model which tool to call; parse its JSON answer."""
    raw = llm.complete(request, system=TOOL_SYSTEM, prefer="strong", max_tokens=80)
    m = re.search(r"\{.*\}", raw, re.S)
    try:
        obj = json.loads(m.group(0))
        return obj.get("tool", "unknown"), obj.get("args", {})
    except Exception:
        return "unknown", {"raw": raw[:40]}


def authorize(user, tool):
    """Simple policy stub: only alice may invoke sensitive tools."""
    return not (tool in SENSITIVE_TOOLS and user != "alice")


class Telemetry:
    def __init__(self):
        self.trace_id = uuid.uuid4().hex[:12]
        self.events = []

    def record(self, user, tool, args, status, latency_ms):
        # TODO (merge): build the structured event (trace_id, span_id, user,
        # tool, args, status, latency_ms, sensitive), print as JSON, store it.
        raise NotImplementedError("record not implemented yet")


def handle_request(tel, user, request):
    """Instrument one agent turn: choose a tool, authorize, record a span."""
    # TODO (merge): time choose_tool(), apply authorize(), record the span
    raise NotImplementedError("handle_request not implemented yet")


def detect_anomalies(events):
    """Flag suspicious patterns in the audit stream."""
    # TODO (merge): denied calls, sensitive-tool bursts (3+), review list
    raise NotImplementedError("detect_anomalies not implemented yet")


def main():
    tel = Telemetry()
    print(f"=== OBSERVABLE AGENT (trace {tel.trace_id}; "
          f"model {llm.active_backend('strong')}) ===\n")
    events = [handle_request(tel, u, r) for (u, r) in REQUESTS]

    print("\n=== TELEMETRY SUMMARY ===")
    print(f"  total spans     : {len(events)}")
    print(f"  sensitive calls : {sum(e['sensitive'] for e in events)}")
    print(f"  denied calls    : {sum(e['status'] == 'denied' for e in events)}")
    avg = sum(e["latency_ms"] for e in events) / len(events)
    print(f"  avg latency_ms  : {avg:.1f}")

    print("\n=== ANOMALY DETECTION ===")
    for f in detect_anomalies(events):
        print(f"  [!] {f}")
    print()


if __name__ == "__main__":
    main()

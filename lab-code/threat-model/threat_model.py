"""
Lab 1 - Mapping AI Security Risks (SKELETON)

Loads a JSON description of an AI system, maps every component to the
OWASP LLM Top 10 (2025), scores the attack surface, and flags data
flows that cross a trust boundary. Produces a structured threat model.

NOTE: This skeleton is incomplete. Merge in the logic from
extra/threat_model_complete.txt before running it.
"""
import json
from owasp_llm import OWASP_LLM_2025, COMPONENT_EXPOSURE


def load_architecture(path="architecture.json"):
    with open(path) as f:
        return json.load(f)


def map_risks(component):
    """Return the OWASP LLM risks that apply to a component type."""
    # TODO (merge): filter OWASP_LLM_2025 by component["type"] in r["applies_to"]
    raise NotImplementedError("map_risks not implemented yet")


def score(component, risk):
    """Simple risk score = likelihood (by component) x impact (PII boost)."""
    # TODO (merge): compute likelihood x impact, boost LLM02/LLM06, return (value, band)
    raise NotImplementedError("score not implemented yet")


def find_boundary_crossings(arch):
    """Flag data flows whose endpoints sit in different trust zones."""
    # TODO (merge): compare trust_zone of each flow's endpoints
    raise NotImplementedError("find_boundary_crossings not implemented yet")


def build_threat_model(arch):
    rows = []
    # TODO (merge): for each component, for each mapped risk, score and collect rows
    raise NotImplementedError("build_threat_model not implemented yet")


def main():
    arch = load_architecture()
    print(f"\n=== THREAT MODEL: {arch['system']} ===\n")

    rows = build_threat_model(arch)
    print(f"{'COMPONENT':<16}{'TYPE':<11}{'RISK':<8}{'NAME':<34}{'SCORE':<6}BAND")
    print("-" * 80)
    for r in rows:
        print(f"{r['component']:<16}{r['type']:<11}{r['risk_id']:<8}"
              f"{r['risk']:<34}{r['score']:<6}{r['band']}")

    high = [r for r in rows if r["band"] == "HIGH"]
    print(f"\nTotal mapped risks: {len(rows)}   HIGH-severity: {len(high)}")

    print("\n=== TRUST BOUNDARY CROSSINGS (highest-priority controls) ===")
    for c in find_boundary_crossings(arch):
        print(f"  [{c['from_zone']} -> {c['to_zone']}] "
              f"{c['from']} -> {c['to']}  ({c['data']})")

    print("\n=== TOP 5 RISKS TO MITIGATE FIRST ===")
    for r in rows[:5]:
        print(f"  {r['risk_id']} {r['risk']} @ {r['component']}  "
              f"[{r['band']} score={r['score']}]")
    print()


if __name__ == "__main__":
    main()

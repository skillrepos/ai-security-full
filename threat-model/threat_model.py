"""
Lab 1 - Mapping AI Security Risks (SKELETON)

Loads a JSON description of an AI system, maps every component to the OWASP
LLM Top 10 (2025) AND to MITRE ATLAS techniques, scores the attack surface,
and flags trust-boundary crossings. It then writes two real deliverables:
a data-flow diagram (Mermaid) and a risk register (Markdown).

NOTE: This skeleton is incomplete. You merge in just TWO functions from
extra/threat_model_complete.txt -- map_risks() (the lookup) and score() (the
math). Everything else (the join, the boundary check, the report writers, and
main) is already provided, so once those two are in, the lab runs.
"""
import json
from owasp_llm import OWASP_LLM_2025, COMPONENT_EXPOSURE


def load_architecture(path="architecture.json"):
    with open(path) as f:
        return json.load(f)


# ===========================================================================
# THE TWO FUNCTIONS YOU MERGE  (everything below this block is provided)
# ===========================================================================
def map_risks(component):
    """Return the OWASP LLM risks that apply to a component type."""
    # TODO (merge): filter OWASP_LLM_2025 by component["type"] in r["applies_to"]
    raise NotImplementedError("map_risks not implemented yet")


def score(component, risk):
    """Simple risk score = likelihood (by component) x impact (PII boost)."""
    # TODO (merge): compute likelihood x impact, boost LLM02/LLM06, return (value, band)
    raise NotImplementedError("score not implemented yet")


# ---- the join + boundary check (provided) -------------------------------

def find_boundary_crossings(arch):
    """Flag data flows whose endpoints sit in different trust zones."""
    zone = {c["id"]: c["trust_zone"] for c in arch["components"]}
    crossings = []
    for flow in arch["data_flows"]:
        z_from, z_to = zone.get(flow["from"]), zone.get(flow["to"])
        if z_from != z_to:
            crossings.append({**flow, "from_zone": z_from, "to_zone": z_to})
    return crossings


def build_threat_model(arch):
    """For each component, score every risk that applies to its type."""
    rows = []
    for comp in arch["components"]:
        for risk in map_risks(comp):
            value, band = score(comp, risk)
            rows.append({
                "component": comp["id"], "type": comp["type"],
                "risk_id": risk["id"], "risk": risk["name"],
                "atlas": risk.get("atlas", []),
                "score": value, "band": band,
            })
    rows.sort(key=lambda r: r["score"], reverse=True)
    return rows


# ---- deliverables (provided) --------------------------------------------

def write_dfd(arch, path="architecture_dfd.mmd"):
    """Write a Mermaid .mmd data-flow diagram; boundary-crossing flows use ==>."""
    zone_of = {c["id"]: c["trust_zone"] for c in arch["components"]}
    zones = {}
    for c in arch["components"]:
        zones.setdefault(c["trust_zone"], []).append(c)
    out = ["flowchart LR"]
    for z, comps in zones.items():
        out.append(f'  subgraph {z}["{z} zone"]')
        for c in comps:
            out.append(f'    {c["id"]}["{c["id"]}<br/>({c["type"]})"]')
        out.append("  end")
    for f in arch["data_flows"]:
        arrow = "==>" if zone_of.get(f["from"]) != zone_of.get(f["to"]) else "-->"
        out.append(f'  {f["from"]} {arrow}|{f["data"]}| {f["to"]}')
    open(path, "w").write("\n".join(out) + "\n")
    return path


def write_risk_register(arch, rows, path="threat_model_report.md"):
    """Write a Markdown risk register: the deliverable you'd hand to a team."""
    out = [f"# Threat Model: {arch['system']}", "",
           "Components mapped to **OWASP LLM Top 10 (2025)** and **MITRE ATLAS** "
           "techniques (https://atlas.mitre.org/techniques).", "",
           "## Risk register (highest score first)", "",
           "| Component | Type | OWASP | Risk | MITRE ATLAS | Score | Band |",
           "|---|---|---|---|---|---|---|"]
    for r in rows:
        atlas = ", ".join(r["atlas"]) if r["atlas"] else "-"
        out.append(f"| {r['component']} | {r['type']} | {r['risk_id']} | "
                   f"{r['risk']} | {atlas} | {r['score']} | {r['band']} |")
    out += ["", "## Trust-boundary crossings", ""]
    for c in find_boundary_crossings(arch):
        out.append(f"- `{c['from_zone']} -> {c['to_zone']}`  "
                   f"{c['from']} -> {c['to']}  ({c['data']})")
    out += ["", "## Top 5 to mitigate first", ""]
    for i, r in enumerate(rows[:5], 1):
        atlas = ", ".join(r["atlas"]) if r["atlas"] else "-"
        out.append(f"{i}. **{r['risk_id']} {r['risk']}** @ `{r['component']}` - "
                   f"{r['band']} (score {r['score']}); ATLAS: {atlas}")
    open(path, "w").write("\n".join(out) + "\n")
    return path


def main():
    arch = load_architecture()
    print(f"\n=== THREAT MODEL: {arch['system']} ===\n")

    rows = build_threat_model(arch)
    print(f"{'COMPONENT':<15}{'TYPE':<10}{'RISK':<7}{'NAME':<34}{'ATLAS':<22}{'SCORE':<6}BAND")
    print("-" * 98)
    for r in rows:
        atlas = ", ".join(r["atlas"]) if r["atlas"] else "-"
        print(f"{r['component']:<15}{r['type']:<10}{r['risk_id']:<7}"
              f"{r['risk']:<34}{atlas:<22}{r['score']:<6}{r['band']}")

    high = [r for r in rows if r["band"] == "HIGH"]
    print(f"\nTotal mapped risks: {len(rows)}   HIGH-severity: {len(high)}")

    print("\n=== TRUST BOUNDARY CROSSINGS (highest-priority controls) ===")
    for c in find_boundary_crossings(arch):
        print(f"  [{c['from_zone']} -> {c['to_zone']}] "
              f"{c['from']} -> {c['to']}  ({c['data']})")

    print("\n=== TOP 5 RISKS TO MITIGATE FIRST ===")
    for r in rows[:5]:
        atlas = ", ".join(r["atlas"]) if r["atlas"] else "-"
        print(f"  {r['risk_id']} {r['risk']} @ {r['component']}  "
              f"[{r['band']} score={r['score']}]  ATLAS: {atlas}")

    dfd = write_dfd(arch)
    reg = write_risk_register(arch, rows)
    print(f"\n=== DELIVERABLES WRITTEN ===\n  {dfd}  (data-flow diagram)\n  {reg}  (risk register)\n")


if __name__ == "__main__":
    main()

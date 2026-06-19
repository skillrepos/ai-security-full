"""
Lab 7 - Red-team runner (provided complete).

Fires every attack in attacks.py at the target agent and scores the result.
An attack FAILS (good) if the agent blocks it or the success_marker is absent
from the response. The BENIGN case is inverted: it must still work.

Run it once against the undefended skeleton (most attacks succeed), merge in
the defense, then run again (attacks blocked, benign still passes).
"""
import re
from attacks import ATTACKS
import target_agent


def evaluate():
    rows, compromised = [], 0
    for atk in ATTACKS:
        resp = target_agent.handle(atk["prompt"])
        hit = re.search(atk["success_marker"], resp)
        benign = atk["id"] == "BENIGN"
        if benign:
            outcome = "PASS" if hit else "BROKEN"   # benign must still work
        else:
            outcome = "VULNERABLE" if hit else "DEFENDED"
            if hit:
                compromised += 1
        rows.append((atk["id"], atk["category"], outcome, resp[:60]))
    return rows, compromised


def main():
    print("=== RED-TEAM RUN ===\n")
    print(f"{'ID':<8}{'CATEGORY':<34}{'OUTCOME':<12}RESPONSE")
    print("-" * 90)
    rows, compromised = evaluate()
    for rid, cat, outcome, resp in rows:
        print(f"{rid:<8}{cat:<34}{outcome:<12}{resp}")

    attacks = [r for r in rows if r[0] != "BENIGN"]
    defended = sum(1 for r in attacks if r[2] == "DEFENDED")
    print(f"\nAttacks: {len(attacks)}   Defended: {defended}   "
          f"Compromised: {compromised}")
    benign_ok = any(r[0] == "BENIGN" and r[2] == "PASS" for r in rows)
    print(f"Benign request still works: {'YES' if benign_ok else 'NO'}")
    if compromised:
        print("\n[!] Agent is VULNERABLE. Merge the defense and re-run.")
    else:
        print("\n[OK] All attacks defended and legitimate use preserved.")


if __name__ == "__main__":
    main()

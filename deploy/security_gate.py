"""
Lab 8 - DevSecOps pre-deployment security gate (SKELETON)

Run the security checks that should sit in your CI/CD pipeline BEFORE an AI
service ships: secret scanning, Dockerfile hardening, dependency CVE scanning,
artifact signing, and a compliance gate. Exit code is non-zero if any blocking
control fails -- exactly how you would wire it into a pipeline.

NOTE: incomplete. Merge in the scanner bodies from
extra/security_gate_complete.txt before running.
"""
import glob
import hashlib
import hmac
import json
import os
import re
import sys

SIGNING_KEY = b"omnitech-release-signing-key"

# TODO (merge): SECRET_PATTERNS
SECRET_PATTERNS = {}


def scan_secrets(app_dir):
    # TODO (merge): grep app *.py for secret patterns
    raise NotImplementedError("scan_secrets not implemented yet")


def lint_dockerfile(path):
    # TODO (merge): flag :latest / unpinned base and missing USER directive
    raise NotImplementedError("lint_dockerfile not implemented yet")


def parse_requirements(path):
    deps = {}
    for line in open(path):
        line = line.strip()
        if line and not line.startswith("#") and "==" in line:
            name, ver = line.split("==", 1)
            deps[name.strip().lower()] = ver.strip()
    return deps


def _ver_tuple(v):
    return tuple(int(x) for x in re.findall(r"\d+", v))


def scan_dependencies(deps, cve_db):
    # TODO (merge): compare each dep version against cve_db fixed_in
    raise NotImplementedError("scan_dependencies not implemented yet")


def sign_artifact(app_dir):
    """Hash the app tree and produce an HMAC signature + manifest."""
    # TODO (merge): sha256 the file tree, HMAC-sign, write release_manifest.json
    raise NotImplementedError("sign_artifact not implemented yet")


def run_gate():
    cve_db = json.load(open("cve_db.json"))
    rules = json.load(open("compliance_rules.json"))

    secrets = scan_secrets("app")
    docker = lint_dockerfile("Dockerfile")
    deps = scan_dependencies(parse_requirements("app/requirements_app.txt"), cve_db)
    manifest = sign_artifact("app")

    # Map check results to compliance controls.
    results = {
        "no_hardcoded_secrets": (not secrets, secrets),
        "dockerfile_nonroot":   ("no USER directive (container runs as root)"
                                 not in docker,
                                 [d for d in docker if "USER" in d or "root" in d]),
        "dockerfile_pinned_base": (not any("pinned" in d for d in docker),
                                   [d for d in docker if "pinned" in d]),
        "no_high_cves":         (not any("HIGH" in d for d in deps),
                                 [d for d in deps if "HIGH" in d]),
        "artifact_signed":      (bool(manifest.get("signature")), []),
    }

    print("=== PRE-DEPLOYMENT SECURITY GATE ===\n")
    blocking_fail = 0
    for ctrl in rules["required_controls"]:
        ok, detail = results.get(ctrl["id"], (False, ["not evaluated"]))
        status = "PASS" if ok else "FAIL"
        if not ok and ctrl["blocking"]:
            blocking_fail += 1
        print(f"  [{status}] {ctrl['id']:<24} {ctrl['desc']}")
        for d in detail:
            print(f"           - {d}")

    print(f"\n  artifact sha256: {manifest['sha256'][:24]}...")
    print(f"  signature      : {manifest['signature'][:24]}...")
    print(f"\nBlocking failures: {blocking_fail}")
    if blocking_fail:
        print("RESULT: DEPLOYMENT BLOCKED")
        return 1
    print("RESULT: CLEARED FOR RELEASE")
    return 0


if __name__ == "__main__":
    sys.exit(run_gate())

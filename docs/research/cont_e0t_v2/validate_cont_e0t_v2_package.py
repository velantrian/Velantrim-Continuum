#!/usr/bin/env python3
"""Package-integrity validator for CONT-E0T v2 PILOT fixtures.

Not a reader. Not an experiment. No model calls.
Fail-closed on structure / authenticity / probe tags / hashes.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FXDIR = ROOT / "fixtures"
MANIFEST = FXDIR / "manifest.json"
CURRENT_KEYS = {
    "active_goal",
    "task_position",
    "constraints",
    "accepted_decisions",
    "rejected_alternatives",
    "unresolved_items",
    "contested_claims",
    "current_rationale",
    "unknown_operations",
    "artifact_refs",
    "process_position",
}
FORBIDDEN_T1 = {"accepted_trajectory", "envelope_pad"}


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def canon(obj) -> bytes:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def load_json(path: Path):
    return json.loads(path.read_text())


def fail(errors, msg):
    errors.append(msg)


def check_fixture(path: Path, errors: list[str]) -> dict:
    fx = load_json(path)
    fid = fx.get("fixture_id", path.name)
    if fx.get("copied_from_e0t_transfer") is not False:
        fail(errors, f"{fid}: copied_from_e0t_transfer must be false")
    if fx.get("claim_under_test") != "B":
        fail(errors, f"{fid}: claim_under_test must be B")
    if fx.get("authorship") != "EXPERIMENTER_AUTHORED":
        fail(errors, f"{fid}: authorship must be EXPERIMENTER_AUTHORED")
    cur = fx.get("current_semantics")
    if not isinstance(cur, dict) or set(cur) != CURRENT_KEYS:
        fail(errors, f"{fid}: current_semantics keys != CURRENT_SEMANTICS_FIELDS")
    if FORBIDDEN_T1 & set(fx.get("current_semantics", {})):
        fail(errors, f"{fid}: current_semantics smuggles trajectory/pad fields")
    traj = fx.get("accepted_trajectory") or []
    n = fx.get("n_transitions")
    nmax = fx.get("n_transitions_max")
    if not isinstance(n, int) or not isinstance(nmax, int) or n > nmax:
        fail(errors, f"{fid}: n_transitions/n_transitions_max invalid")
    if len(traj) != n:
        fail(errors, f"{fid}: len(accepted_trajectory) != n_transitions")
    if len(traj) < 2:
        fail(errors, f"{fid}: F6 length < 2")
    if any(set(ev.keys()) == {"seq", "op", "field", "value"} or ev.get("op") == "SET" for ev in traj):
        fail(errors, f"{fid}: FAKE_SET_FROM_FINAL_STATE shape")
    # F6: intermediate from_state != final current
    if not any(canon(ev.get("from_state")) != canon(cur) for ev in traj):
        fail(errors, f"{fid}: F6 no from_state distinct from final current")
    if not any(ev.get("supersedes") for ev in traj):
        fail(errors, f"{fid}: F6 no genuine supersession")
    # from_state not reconstructable by field-wise SET of final: some from_state value differs
    if not any(canon(ev.get("from_state")) != canon(cur) for ev in traj):
        fail(errors, f"{fid}: F6 from_state reconstructable from final only")
    if canon(traj[-1].get("to_state")) != canon(cur):
        fail(errors, f"{fid}: last to_state != current_semantics")
    # SET-from-final detector: every event to_state == current and from_state == current
    if all(canon(ev.get("to_state")) == canon(cur) for ev in traj):
        fail(errors, f"{fid}: every to_state == final current (SET-from-final)")
    probes = fx.get("probes") or []
    tags = {p.get("probe_id"): p.get("tag") for p in probes}
    prim = [p for p in probes if p.get("tag") == "PRIMARY_RESUME"]
    hist = [p for p in probes if p.get("tag") == "SECONDARY_HISTORY"]
    if not prim:
        fail(errors, f"{fid}: no PRIMARY_RESUME probe")
    if not hist:
        fail(errors, f"{fid}: no SECONDARY_HISTORY probe")
    for p in prim:
        if p.get("primary_solvable_from_T1") is not True:
            fail(errors, f"{fid}:{p.get('probe_id')} PRIMARY must be solvable from T1")
        gold = (p.get("gold") or "").lower()
        if "previously" in (p.get("wording") or "").lower() or "superseded" in (p.get("wording") or "").lower():
            fail(errors, f"{fid}:{p.get('probe_id')} PRIMARY wording looks historical")
    for p in hist:
        if p.get("primary_solvable_from_T1") is True:
            fail(errors, f"{fid}:{p.get('probe_id')} SECONDARY must not claim T1-solvable PRIMARY")
    if "envelope_pad" in json.dumps(fx):
        fail(errors, f"{fid}: envelope_pad is forbidden")
    return fx


def main() -> int:
    errors: list[str] = []
    if not MANIFEST.exists():
        print("FAIL missing manifest")
        return 2
    man = load_json(MANIFEST)
    if man.get("claim_under_test") != "B":
        errors.append("manifest claim_under_test != B")
    if man.get("partition", {}).get("EVIDENCE"):
        errors.append("EVIDENCE partition must stay empty in this package")
    prompt = ROOT / Path(man.get("reader_prompt_file", "reader_prompt_v2.txt")).name
    if not prompt.exists():
        prompt = ROOT / man.get("reader_prompt_file", "")
    if not prompt.exists():
        errors.append("reader prompt missing")
    else:
        got = sha256_bytes(prompt.read_bytes())
        if got != man.get("reader_prompt_sha256"):
            errors.append(f"reader prompt sha mismatch {got}")
    seen = []
    for row in man.get("fixtures", []):
        path = FXDIR / row["file"]
        if not path.exists():
            errors.append(f"missing {row['file']}")
            continue
        got = sha256_bytes(path.read_bytes())
        if got != row.get("file_sha256"):
            errors.append(f"{row['file']} file_sha256 mismatch {got}")
        fx = check_fixture(path, errors)
        seen.append(fx.get("fixture_id"))
        if row.get("n_transitions") != fx.get("n_transitions"):
            errors.append(f"{row['file']} manifest n_transitions mismatch")
    if seen != man.get("partition", {}).get("PILOT"):
        errors.append(f"PILOT list mismatch {seen}")
    if errors:
        print("FAIL")
        for e in errors:
            print(" -", e)
        return 1
    print("PASS")
    print("fixtures", ", ".join(seen))
    print("claim B; no envelope_pad; no model run")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Package-integrity validator for CONT-E0T v2.2 PILOT fixtures.

Not a reader. Not an experiment. No model calls.
Stdout PACKAGE_STRUCTURAL_PASS ≠ science, ≠ Evidence, ≠ Claim B.
"""
from __future__ import annotations

import copy
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FXDIR = ROOT / "fixtures"
MANIFEST = FXDIR / "manifest.json"
LIST_FIELDS = (
    "constraints",
    "accepted_decisions",
    "rejected_alternatives",
    "unresolved_items",
    "contested_claims",
    "unknown_operations",
    "artifact_refs",
)
SCALAR_FIELDS = ("active_goal", "task_position", "current_rationale", "process_position")
CURRENT_KEYS = set(LIST_FIELDS + SCALAR_FIELDS)
FORBIDDEN_ON_T1 = {
    "accepted_trajectory",
    "thin_trajectory",
    "envelope_pad",
    "provenance_validator_only",
    "audit_snapshots_validator_only",
}
READER_FORBIDDEN_KEYS = {
    "from_state",
    "to_state",
    "type",
    "supersedes",
    "accepted_at",
    "provenance",
    "envelope_pad",
}


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def canon(obj) -> bytes:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def normalize_state(state: dict) -> dict:
    """Order-insensitive current-semantics for fold equality."""
    out = json.loads(json.dumps(state))
    for f in LIST_FIELDS:
        items = list(out.get(f) or [])
        out[f] = sorted(items, key=lambda x: (x.get("id") or "", x.get("text") or ""))
    return out


def load_json(path: Path):
    return json.loads(path.read_text())


def fail(errors, msg):
    errors.append(msg)


def semantic_atoms(state: dict) -> set:
    """Nonempty current-state atoms. Empty/missing contributes nothing."""
    atoms: set = set()
    if not isinstance(state, dict):
        return atoms
    for f in SCALAR_FIELDS:
        val = (state.get(f) or "").strip()
        if val:
            atoms.add((f, None, val))
    for f in LIST_FIELDS:
        for item in state.get(f) or []:
            if not isinstance(item, dict):
                continue
            iid = item.get("id")
            text = (item.get("text") or "").strip()
            status = item.get("status")
            if iid or text:
                atoms.add((f, iid, text, status))
    return atoms


def set_reconstructable_from_final(from_state, current) -> bool:
    """True iff from_state atoms ⊆ current atoms (field-wise SET of the final snapshot)."""
    return semantic_atoms(from_state) <= semantic_atoms(current)


def build_reader_packages(fx: dict) -> dict:
    """Claim B reader treatments. Provenance and audit snapshots excluded from both arms."""
    cur = fx["current_semantics"]
    return {
        "CONT-T1": {"current_semantics": cur},
        "CONT-T2": {"current_semantics": cur, "thin_trajectory": fx.get("thin_trajectory") or []},
    }


def apply_change(state: dict, ch: dict) -> dict:
    state = copy.deepcopy(state)
    field = ch["field"]
    iid = ch.get("id")
    to = ch.get("to")
    if field in SCALAR_FIELDS:
        state[field] = to or ""
        return state
    items = list(state.get(field) or [])
    if to is None:
        state[field] = [x for x in items if x.get("id") != iid]
        return state
    rec = {"id": iid, "text": to, "current": True}
    if ch.get("status") is not None:
        rec["status"] = ch["status"]
    found = False
    for i, x in enumerate(items):
        if x.get("id") == iid:
            items[i] = rec
            found = True
            break
    if not found:
        items.append(rec)
    state[field] = items
    return state


def fold_thin(initial: dict, thin: list) -> dict:
    state = copy.deepcopy(initial)
    for ev in thin:
        for ch in ev.get("changes") or []:
            state = apply_change(state, ch)
    return state


def check_f65_distinct_from_clause3() -> None:
    """Self-check: subset-of-final from_state is != current but SET-reconstructable."""
    current = {
        "active_goal": "G",
        "task_position": "P",
        "current_rationale": "R",
        "process_position": "X",
        "constraints": [{"id": "c1", "text": "keep", "current": True}],
        "accepted_decisions": [],
        "rejected_alternatives": [],
        "unresolved_items": [],
        "contested_claims": [],
        "unknown_operations": [],
        "artifact_refs": [],
    }
    from_subset = copy.deepcopy(current)
    from_subset["constraints"] = []
    assert canon(from_subset) != canon(current)
    assert set_reconstructable_from_final(from_subset, current)
    from_novel = copy.deepcopy(current)
    from_novel["constraints"] = [{"id": "c-old", "text": "old weekday rule", "current": True}]
    assert not set_reconstructable_from_final(from_novel, current)


def check_fixture(path: Path, errors: list[str]) -> dict:
    fx = load_json(path)
    fid = fx.get("fixture_id", path.name)
    if fx.get("copied_from_e0t_transfer") is not False:
        fail(errors, f"{fid}: copied_from_e0t_transfer must be false")
    if fx.get("claim_under_test") != "B":
        fail(errors, f"{fid}: claim_under_test must be B")
    if fx.get("authorship") != "EXPERIMENTER_AUTHORED":
        fail(errors, f"{fid}: authorship must be EXPERIMENTER_AUTHORED")
    if fx.get("partition") != "PILOT":
        fail(errors, f"{fid}: partition must be PILOT")
    if fx.get("claim_b_role") != "PILOT_SHAKEDOWN_NOT_DISCRIMINATOR":
        fail(errors, f"{fid}: claim_b_role must remain PILOT_SHAKEDOWN_NOT_DISCRIMINATOR")
    cur = fx.get("current_semantics")
    if not isinstance(cur, dict) or set(cur) != CURRENT_KEYS:
        fail(errors, f"{fid}: current_semantics keys != CURRENT_SEMANTICS_FIELDS")
    if FORBIDDEN_ON_T1 & set(cur):
        fail(errors, f"{fid}: current_semantics smuggles trajectory/provenance/pad")
    thin = fx.get("thin_trajectory") or []
    audit = fx.get("audit_snapshots_validator_only") or []
    prov = fx.get("provenance_validator_only") or []
    n = fx.get("n_transitions")
    nmax = fx.get("n_transitions_max")
    if not isinstance(n, int) or not isinstance(nmax, int) or n > nmax:
        fail(errors, f"{fid}: n_transitions/n_transitions_max invalid")
    if len(thin) != n or len(audit) != n:
        fail(errors, f"{fid}: thin/audit length != n_transitions")
    if n < 2:
        fail(errors, f"{fid}: F6 length < 2")
    # D3: reader trajectory must be thin — no snapshots, no provenance labels
    thin_blob = json.dumps(thin)
    for bad in READER_FORBIDDEN_KEYS:
        if bad in thin_blob:
            fail(errors, f"{fid}: thin_trajectory contains forbidden reader key {bad}")
    # D4: provenance must exist for validator and must not appear in reader packages
    if not prov:
        fail(errors, f"{fid}: provenance_validator_only missing")
    if any("changes" in p or "from_state" in p for p in prov):
        fail(errors, f"{fid}: provenance object must not carry trajectory path")
    pkgs = build_reader_packages(fx)
    for arm, pkg in pkgs.items():
        blob = json.dumps(pkg)
        if "provenance_validator_only" in blob or "audit_snapshots_validator_only" in blob:
            fail(errors, f"{fid}: {arm} reader package leaked validator-only treatment")
        if arm == "CONT-T1" and "thin_trajectory" in pkg:
            fail(errors, f"{fid}: CONT-T1 reader must not include thin_trajectory")
        if arm == "CONT-T2" and "thin_trajectory" not in pkg:
            fail(errors, f"{fid}: CONT-T2 reader missing thin_trajectory")
    if canon(pkgs["CONT-T1"]["current_semantics"]) != canon(pkgs["CONT-T2"]["current_semantics"]):
        fail(errors, f"{fid}: reader current_semantics not byte-identical")
    # F6.3 distinct from F6.5
    if not any(canon(ev.get("from_state")) != canon(cur) for ev in audit):
        fail(errors, f"{fid}: F6.3 no audit from_state distinct from final current")
    # F6.4
    if not any((p.get("supersedes") or []) for p in prov):
        fail(errors, f"{fid}: F6.4 no nonempty supersedes in provenance_validator_only")
    # F6.5 DISTINCT: some from_state has atoms not ⊆ final atoms
    if not any(not set_reconstructable_from_final(ev.get("from_state"), cur) for ev in audit):
        fail(errors, f"{fid}: F6.5 all audit from_state atoms ⊆ final current (SET-reconstructable)")
    # fold thin from first audit from_state
    folded = fold_thin(audit[0]["from_state"], thin)
    if canon(normalize_state(folded)) != canon(normalize_state(cur)):
        fail(errors, f"{fid}: fold(thin_trajectory) != current_semantics")
    if canon(audit[-1].get("to_state")) != canon(cur):
        fail(errors, f"{fid}: last audit to_state != current_semantics")
    # not historical SET-from-final event list: every change.to is a current atom and no novel from
    if all(set_reconstructable_from_final(ev.get("from_state"), cur) for ev in audit):
        fail(errors, f"{fid}: FAKE_SET_FROM_FINAL_STATE (every from_state ⊆ final)")
    probes = fx.get("probes") or []
    prim = [p for p in probes if p.get("tag") == "PRIMARY_RESUME"]
    hist = [p for p in probes if p.get("tag") == "SECONDARY_HISTORY"]
    if not prim:
        fail(errors, f"{fid}: no PRIMARY_RESUME probe")
    if not hist:
        fail(errors, f"{fid}: no SECONDARY_HISTORY probe")
    t1_text = json.dumps(cur, ensure_ascii=False).lower()
    for p in prim:
        if p.get("primary_solvable_from_T1") is not True:
            fail(errors, f"{fid}:{p.get('probe_id')} PRIMARY must be solvable from T1")
        wording = (p.get("wording") or "").lower()
        if "previously" in wording or "superseded" in wording:
            fail(errors, f"{fid}:{p.get('probe_id')} PRIMARY wording looks historical")
    for p in hist:
        if p.get("primary_solvable_from_T1") is True:
            fail(errors, f"{fid}:{p.get('probe_id')} SECONDARY must not claim T1-solvable PRIMARY")
        gold = (p.get("gold") or "").strip().rstrip(".").lower()
        if gold and gold in t1_text:
            fail(errors, f"{fid}:{p.get('probe_id')} D8 SECONDARY gold recoverable from CONT-T1")
    if "envelope_pad" in json.dumps(fx):
        fail(errors, f"{fid}: envelope_pad is forbidden")
    return fx


def main() -> int:
    errors: list[str] = []
    try:
        check_f65_distinct_from_clause3()
    except AssertionError:
        errors.append("internal F6.5≠F6.3 self-check failed")
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
    print("PACKAGE_STRUCTURAL_PASS")
    print("fixtures", ", ".join(seen))
    print("claim B; PILOT_ONLY; no envelope_pad; no model run; not science")
    return 0


if __name__ == "__main__":
    sys.exit(main())

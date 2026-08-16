#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_PATHS = [
    "docs/research/IDPS_EXPERIMENT_0_PREREGISTRATION.md",
    "experiments/e0/fixtures/capture/pilot/fixtures.json",
    "experiments/e0/fixtures/capture/evidence/fixtures.json",
    "experiments/e0/fixtures/transfer/scenarios.json",
    "experiments/e0/gold/candidates/capture-gold.ai-proposed.json",
    "experiments/e0/oracle/candidates/transfer-oracle.ai-proposed.json",
    "scripts/e0/e0_core.py",
]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_snapshot(repo_root: Path, reviewed_commit: str, paths: list[str]) -> dict:
    artifacts = []
    for relative in paths:
        path = repo_root / relative
        if not path.is_file():
            raise FileNotFoundError(relative)
        artifacts.append({"path": relative, "sha256": sha256_file(path)})
    return {
        "snapshot_version": "0.1",
        "purpose": "ISSUE_9_HUMAN_REFERENCE_REVIEW_INPUT",
        "reviewed_commit": reviewed_commit,
        "candidate_status_required": "AI_PROPOSED_DRAFT",
        "artifacts": artifacts,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=str(ROOT))
    parser.add_argument("--reviewed-commit", required=True)
    parser.add_argument("--output", default="-")
    args = parser.parse_args()

    snapshot = build_snapshot(Path(args.repo_root), args.reviewed_commit, DEFAULT_PATHS)
    rendered = json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n"
    if args.output == "-":
        print(rendered, end="")
    else:
        Path(args.output).write_text(rendered, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

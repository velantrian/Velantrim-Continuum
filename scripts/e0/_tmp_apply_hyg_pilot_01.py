from pathlib import Path

p = Path('scripts/e0/preflight_pilot.py')
lines = p.read_text().splitlines()
i = next(i for i,x in enumerate(lines) if x.startswith('TRANSFER_PATH = '))
lines[i+1:i+1] = ['CAPTURE_GOLD_PATH = "experiments/e0/gold/approved/capture-gold.v0.1.json"','TRANSFER_ORACLE_PATH = "experiments/e0/oracle/approved/transfer-oracle.v0.1.json"']
start = next(i for i,x in enumerate(lines) if x.startswith('def pilot_ids('))
end = next(i for i,x in enumerate(lines[start+1:], start+1) if x.startswith('def evidence_ids('))
lines[start:end] = ['def pilot_arm_ids(root: Path) -> tuple[set[str], set[str]]:','    capture = load_json(root / CAPTURE_PILOT_PATH)','    transfer = load_json(root / TRANSFER_PATH)','    capture_ids = {item.get("fixture_id") for item in capture.get("fixtures", []) if item.get("fixture_id")}','    transfer_ids = {','        item.get("scenario_id")','        for item in transfer.get("scenarios", [])','        if item.get("partition") == "PILOT" and item.get("scenario_id")','    }','    return capture_ids, transfer_ids','','','def pilot_ids(root: Path) -> set[str]:','    capture_ids, transfer_ids = pilot_arm_ids(root)','    return capture_ids | transfer_ids','','']
allowed = next(i for i,x in enumerate(lines) if x.strip() == 'allowed_ref_paths = {')
loop = next(i for i,x in enumerate(lines[allowed:], allowed) if x.strip() == 'for index, ref in enumerate(refs):')
indent = lines[allowed][:len(lines[allowed])-len(lines[allowed].lstrip())]
lines[allowed:loop] = [indent+'allowed_ref_paths = {CAPTURE_GOLD_PATH, TRANSFER_ORACLE_PATH}', indent+'bound_ref_paths: set[str] = set()']
expected = next(i for i,x in enumerate(lines) if 'expected_hash = require_sha256(ref.get("sha256")' in x)
ind = lines[expected][:len(lines[expected])-len(lines[expected].lstrip())]
lines.insert(expected, ind+'bound_ref_paths.add(path)')
r = next(i for i,x in enumerate(lines) if 'unknown/non-Pilot fixture or scenario IDs' in x)
ind = ' ' * 4
lines[r+1:r+1] = ['',ind+'capture_pilot_ids, transfer_pilot_ids = pilot_arm_ids(root)',ind+'requested_ids = set(requested)',ind+'if requested_ids & capture_pilot_ids and CAPTURE_GOLD_PATH not in bound_ref_paths:',ind+'    raise PreflightError("Capture Pilot requires exact approved Capture Gold reference")',ind+'if requested_ids & transfer_pilot_ids and TRANSFER_ORACLE_PATH not in bound_ref_paths:',ind+'    raise PreflightError("Transfer Pilot requires exact approved Transfer Oracle reference")']
p.write_text('\n'.join(lines)+'\n')

t = Path('tests/e0/test_pilot_control.py')
lines = t.read_text().splitlines()
start = next(i for i,x in enumerate(lines) if x.strip() == '"approved_references": [')
end = next(i for i,x in enumerate(lines[start+1:], start+1) if x.strip() == '],')
ind = lines[start][:len(lines[start])-len(lines[start].lstrip())]
lines[start:end+1] = [ind+'"approved_references": [',ind+'    {',ind+'        "path": preflight.CAPTURE_GOLD_PATH,',ind+'        "sha256": sha256(root / preflight.CAPTURE_GOLD_PATH),',ind+'    },',ind+'    {',ind+'        "path": preflight.TRANSFER_ORACLE_PATH,',ind+'        "sha256": sha256(root / preflight.TRANSFER_ORACLE_PATH),',ind+'    },',ind+'],']
t.write_text('\n'.join(lines)+'\n')

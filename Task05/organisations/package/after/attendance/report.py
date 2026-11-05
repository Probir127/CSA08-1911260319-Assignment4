import json
from pathlib import Path
def write_report(summary,errors,folder):
    """Write summary and error evidence for this independently runnable layout."""
    folder=Path(folder);folder.mkdir(parents=True,exist_ok=True)
    (folder/'attendance.json').write_text(json.dumps(summary,indent=2))
    (folder/'errors.json').write_text(json.dumps(errors,indent=2))

def write_absences(registers,folder):
    """Write the added consecutive-absence report."""
    (Path(folder)/'consecutive_absent.json').write_text(json.dumps(registers,indent=2))

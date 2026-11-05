from pathlib import Path
from datetime import date
def read_files(folder):
    """Read daily physical rows; collect invalid and duplicate-record evidence."""
    records=[];errors=[];seen=set()
    for path in sorted(Path(folder).glob('*.csv')):
        try:
            with path.open(encoding='utf-8') as stream:
                for number,line in enumerate(stream,1):
                    try:
                        fields=line.strip().split(',')
                        if len(fields)!=3:raise ValueError('expected 3 fields')
                        register,day,status=fields
                        if not register.isdigit() or status not in ('P','A'):raise ValueError('invalid record')
                        if date.fromisoformat(day).isoformat()!=day:raise ValueError('invalid date')
                        if (register,day) in seen:raise ValueError('duplicate record')
                    except ValueError as error:errors.append((path.name,number,str(error)))
                    else:seen.add((register,day));records.append((register,day,status))
        except (OSError,UnicodeError) as error:errors.append((path.name,0,str(error)))
    return records,errors

def percentage(present,total):
    """Return observed-session percentage, or None when no sessions exist."""
    return round(present*100/total,2) if total else None
def summarise(records):
    """Count accepted sessions per student."""
    counts={}
    for register,day,status in records:
        counts.setdefault(register,[0,0]);counts[register][0]+=status=='P';counts[register][1]+=1
    return {r:dict(present=p,total=t,percentage=percentage(p,t)) for r,(p,t) in sorted(counts.items())}

import json
from pathlib import Path
def write_report(summary,errors,folder):
    """Write summary and error evidence for this independently runnable layout."""
    folder=Path(folder);folder.mkdir(parents=True,exist_ok=True)
    (folder/'attendance.json').write_text(json.dumps(summary,indent=2))
    (folder/'errors.json').write_text(json.dumps(errors,indent=2))

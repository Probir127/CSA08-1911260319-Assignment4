"""Deterministic CSV output with fixed allow-listed event file names."""
import csv,json
from pathlib import Path
from .validation import EVENTS
def write_reports(master,issues,duplicates,folder):
    """Write master, one file per event, summary and error log; expose output failure."""
    folder=Path(folder);folder.mkdir(parents=True,exist_ok=True)
    rows=[dict(master[key],events=';'.join(sorted(master[key]['events']))) for key in sorted(master)]
    fields=['register','name','department','email','events']
    def write_csv(path,values):
        """Close a new UTF-8 CSV even if writing raises."""
        with path.open('w',encoding='utf-8',newline='') as stream:
            writer=csv.DictWriter(stream,fieldnames=fields);writer.writeheader();writer.writerows(values)
    write_csv(folder/'master.csv',rows)
    for event in EVENTS:write_csv(folder/(event.lower()+'.csv'),[row for row in rows if event in master[row['register']]['events']])
    with (folder/'errors.csv').open('w',encoding='utf-8',newline='') as stream:
        writer=csv.DictWriter(stream,fieldnames=['file','line','type','message']);writer.writeheader();writer.writerows(issues)
    summary=dict(unique_students=len(master),duplicates_merged=duplicates,
                 rejected_rows=sum(i['line']>0 and i['type']!='DUPLICATE_MERGED' for i in issues),
                 file_errors=sum(i['line']==0 for i in issues),
                 participants={event:sum(event in r['events'] for r in master.values()) for event in EVENTS})
    with (folder/'summary.json').open('w',encoding='utf-8') as stream:json.dump(summary,stream,indent=2)
    return summary

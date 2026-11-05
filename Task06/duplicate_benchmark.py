"""Count-model and timing evidence for list searching versus a seen set."""
from time import perf_counter
from pathlib import Path
import json
if __name__=='__main__':
    rows=[]
    for n in [1000,10000]:
        records=[str(1911260000+i) for i in range(n)];row={'n':n,'list_equality_checks_model':n*(n-1)//2,'set_membership_operations':n}
        begin=perf_counter();seen=[]
        for register in records:
            if register not in seen:seen.append(register)
        row['list_seconds']=perf_counter()-begin
        begin=perf_counter();lookup=set()
        for register in records:
            if register not in lookup:lookup.add(register)
        row['set_seconds']=perf_counter()-begin
        assert set(seen)==lookup and len(lookup)==n;rows.append(row)
    Path(__file__).with_name('measurements.json').write_text(json.dumps(rows,indent=2));print(json.dumps(rows,indent=2))

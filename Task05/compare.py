"""Execute all eight layouts and measure actual source-file change counts."""
from pathlib import Path
import subprocess,sys,json
if __name__=='__main__':
    base=Path(__file__).resolve().parent;results={};reference=None
    for layout in ['single','module','three_modules','package']:
        root=base/'organisations'/layout
        before={str(p.relative_to(root/'before')):p.read_text() for p in (root/'before').rglob('*.py')}
        after={str(p.relative_to(root/'after')):p.read_text() for p in (root/'after').rglob('*.py')}
        changed=[name for name in sorted(set(before)|set(after)) if before.get(name)!=after.get(name)]
        results[layout]={'changed_files':changed,'count':len(changed)}
        for version in ['before','after']:
            output=base/'results'/f'{layout}_{version}'
            subprocess.run([sys.executable,str(root/version/'main.py'),str(base/'inputs'),str(output)],check=True)
            summary=json.loads((output/'attendance.json').read_text())
            if reference is None:reference=summary
            else:assert summary==reference
            if version=='after':assert json.loads((output/'consecutive_absent.json').read_text())==['1911260001']
    assert [results[k]['count'] for k in ['single','module','three_modules','package']]==[1,2,3,3]
    (base/'change_evidence.json').write_text(json.dumps(results,indent=2))
    print(json.dumps(results,indent=2))
    print('All eight organisations agree; only 1911260001 has 3 consecutive absent calendar dates PASS')

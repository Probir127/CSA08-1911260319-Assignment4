"""Three-day before/after evidence and deterministic write-failure injection."""
import os,tempfile,json
from pathlib import Path
from unittest.mock import patch
import broken,repaired
class FailingFile:
    """A retained test handle whose write raises; track explicit closure."""
    def __init__(self):self.closed=False
    def write(self,text):raise OSError('injected write failure')
    def close(self):self.closed=True
    def __enter__(self):return self
    def __exit__(self,*args):self.close()
if __name__=='__main__':
    base=Path(__file__).parent;original=Path.cwd();evidence={}
    with tempfile.TemporaryDirectory() as folder:
        os.chdir(folder)
        try:
            history=[]
            for day,books in enumerate([['A','B'],['C','D'],['E','F']],1):
                path=Path(f'day{day}.txt');path.write_text('\n'.join(books))
                broken.process(path);history.append(Path('returns.log').read_text())
            assert history==['AB','CD','EF'];evidence['broken_three_days']=history
            handle=FailingFile()
            with patch('builtins.open',return_value=handle):
                try:broken.save_returns(['X'])
                except OSError:pass
            assert not handle.closed;evidence['broken_handle_closed_after_failure']=handle.closed
            fixed=FailingFile()
            with patch('builtins.open',return_value=fixed):
                try:repaired.save_returns(['X'],'ignored')
                except OSError:pass
            assert fixed.closed;evidence['repaired_handle_closed_after_failure']=fixed.closed
            for day in range(1,4):assert repaired.process(f'day{day}.txt','fixed.log','errors.jsonl')
            assert Path('fixed.log').read_text()=='A\nB\nC\nD\nE\nF\n'
            assert not repaired.process('missing.txt','fixed.log','errors.jsonl')
            evidence['repaired_log']=Path('fixed.log').read_text()
            evidence['missing_file_logged']=json.loads(Path('errors.jsonl').read_text())['type']
            (base/'returns_fixed.log').write_text(Path('fixed.log').read_text())
            (base/'errors.jsonl').write_text(Path('errors.jsonl').read_text())
        finally:os.chdir(original)
    (base/'evidence.json').write_text(json.dumps(evidence,indent=2))
    print(json.dumps(evidence,indent=2));print('Three days, missing file and write-failure closure tests PASS')

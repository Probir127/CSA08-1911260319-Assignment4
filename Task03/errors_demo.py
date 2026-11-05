"""Real malformed/missing/encoding tests and labelled permission fault injection."""
from pathlib import Path
import sys,tempfile,json
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'Task02'))
from attendance_core import read_files,parse_line,InvalidRecord,process_month
def summarise(path):
    """Extension: missing input yields unknown counts and an explicit file error."""
    from complete_code import summarise as original
    try:return original(path)
    except FileNotFoundError:return None,None,[(0,'file not found')]
def hidden_typo(lines):
    """Deliberately wrong: catch-all suppresses an actual NameError."""
    present=0
    for line in lines:
        try:
            parse_line(line)
            present+=presnt  # Intentional variable-name defect for the misuse experiment.
        except Exception:pass
    return present
if __name__=='__main__':
    evidence={}
    with tempfile.TemporaryDirectory() as folder:
        base=Path(folder);good=base/'good.csv';good.write_text('1911260001,2026-10-08,P\n')
        bad=base/'wrong_encoding.csv';bad.write_bytes(b'1911260001,2026-10-08,P\n\xff\n')
        empty=base/'empty.csv';empty.write_text('')
        records,errors,audit=read_files([good,bad,empty,base/'missing.csv'],'2026-10')
        assert len(records)==1 and {r['type'] for r in errors}=={'InvalidRecord','UnicodeDecodeError','FileNotFoundError'}
        assert sum(event=='ATTEMPT_FINISHED' for _,event in audit)==4
        evidence['real_file_failures']=errors;evidence['audit']=audit
        with patch.object(Path,'open',side_effect=PermissionError('injected permission denial')):
            _,faults,audit2=read_files([good])
        assert faults[0]['type']=='PermissionError' and audit2[-1][1]=='ATTEMPT_FINISHED'
        evidence['permission_fault_injection']=faults
        assert summarise(base/'missing.csv')==(None,None,[(0,'file not found')])
        try:process_month(base/'missing_folder','2026-10',base/'out')
        except FileNotFoundError:evidence['missing_folder']='FileNotFoundError'
        else:raise AssertionError('Missing folder accepted')
    try:parse_line('1911260001,2026-02-30,P')
    except InvalidRecord as error:
        assert isinstance(error.__cause__,ValueError);evidence['chained_cause']=type(error.__cause__).__name__
    assert hidden_typo(['1911260001,2026-10-08,P'])==0
    try:
        try:
            parse_line('1911260001,2026-10-08,P');value=presnt
        except InvalidRecord:pass
    except NameError:evidence['specific_handler_typo']='NameError propagated as expected'
    else:raise AssertionError('Typo hidden by specific handler')
    evidence['broad_handler_typo']='Silently returns zero; NameError is lost'
    Path(__file__).with_name('evidence.json').write_text(json.dumps(evidence,indent=2))
    print(json.dumps(evidence,indent=2));print('Failure, chaining, loop-else/finally audit and typo tests PASS')

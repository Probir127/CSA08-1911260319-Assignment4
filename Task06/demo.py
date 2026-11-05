"""Verify clean, duplicate, invalid, damaged, missing and decoding-failure inputs."""
from pathlib import Path
import csv,json,tempfile
from fest.pipeline import run
from fest.validation import valid_email
if __name__=='__main__':
    base=Path(__file__).parent;summary=run(base/'inputs',base/'results')
    assert summary==dict(unique_students=4,duplicates_merged=1,rejected_rows=3,file_errors=1,
                         participants={'Dance':1,'Music':2,'Drama':1,'Quiz':1,'Art':0})
    with (base/'results/master.csv').open() as stream:rows=list(csv.DictReader(stream))
    assert len(rows)==4 and rows[0]['events']=='Dance;Quiz'
    for event in ['dance','music','drama','quiz','art']:assert (base/'results'/f'{event}.csv').exists()
    for email in ['a@example.test','student+fest@college.test']:assert valid_email(email)
    for email in ['bad-email','a@@b.test','a@b','a@.test','a b@c.test','.a@b.test']:assert not valid_email(email)
    with tempfile.TemporaryDirectory() as directory:
        temp=Path(directory);(temp/'CSE.csv').write_bytes(b'\xff\n1911260099,Later Valid,CSE,later@example.test,Art\n')
        result=run(temp,temp/'results')
        assert result['unique_students']==1 and result['rejected_rows']==1 and result['file_errors']==4
        print('Wrong-encoding row rejected; following valid row processed PASS')
    print(json.dumps(summary,indent=2));print('All fest requirements and validation checks PASS')

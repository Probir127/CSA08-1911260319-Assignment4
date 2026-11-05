"""Monthly attendance example and hand trace assertions."""
from attendance_core import process_month
from pathlib import Path
if __name__=='__main__':
    base=Path(__file__).parent;rows,errors,audit=process_month(base/'inputs','2026-10',base/'results')
    by_id={r['register']:r for r in rows}
    assert by_id['1911260001']['percentage']==50.0
    assert by_id['1911260002']['percentage']==100.0
    assert len(errors)==2
    print('Students:',rows);print('Rejected rows:',errors);print('Audit:',audit)
    print('Observed-session percentages and damaged/duplicate row checks PASS')

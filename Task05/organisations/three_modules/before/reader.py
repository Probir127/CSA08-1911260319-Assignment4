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

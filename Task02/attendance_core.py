"""Attendance model: one valid record per register/date, first valid entry wins."""
import csv,json
from pathlib import Path
from datetime import date
class InvalidRecord(ValueError):
    """An attendance row violates the declared file format."""
def parse_line(line):
    """Parse register, strict ISO date, P/A; retain original failures as causes."""
    try:fields=next(csv.reader([line.strip()],strict=True))
    except csv.Error as error:raise InvalidRecord('invalid CSV') from error
    if len(fields)!=3:raise InvalidRecord(f'expected 3 fields, found {len(fields)}')
    register,day,status=[field.strip() for field in fields]
    if not register.isascii() or not register.isdigit():raise InvalidRecord('invalid register number')
    try:parsed=date.fromisoformat(day)
    except ValueError as error:raise InvalidRecord('invalid calendar date') from error
    if parsed.isoformat()!=day:raise InvalidRecord('date must use YYYY-MM-DD')
    if status not in ('P','A'):raise InvalidRecord(f'invalid status {status!r}')
    return register,day,status
def read_files(paths,month=None):
    """Stream binary lines, catch bad rows independently and audit every file attempt."""
    records=[];errors=[];audit=[];seen=set()
    for path in paths:
        path=Path(path)
        try:
            with path.open('rb') as stream:
                for number,raw in enumerate(stream,1):
                    try:
                        record=parse_line(raw.decode('utf-8'))
                        if month and record[1][:7]!=month:raise InvalidRecord('outside requested month')
                        key=record[:2]
                        if key in seen:raise InvalidRecord('duplicate register/date')
                    except (InvalidRecord,UnicodeDecodeError) as error:
                        errors.append(dict(file=path.name,line=number,type=type(error).__name__,message=str(error),raw=raw.decode('utf-8',errors='replace').rstrip()))
                    else:
                        seen.add(key);records.append(record)
        except (FileNotFoundError,PermissionError,IsADirectoryError) as error:
            errors.append(dict(file=path.name,line=0,type=type(error).__name__,message=str(error),raw=''))
        except OSError as error:
            errors.append(dict(file=path.name,line=0,type=type(error).__name__,message=str(error),raw=''))
        else:audit.append((path.name,'READ_COMPLETED'))
        finally:audit.append((path.name,'ATTEMPT_FINISHED'))
    return records,errors,audit
def statistics(records):
    """Compute percentages over accepted observed sessions, never invent absences."""
    counts={}
    for register,_,status in records:
        value=counts.setdefault(register,{'present':0,'total':0})
        value['present']+=status=='P';value['total']+=1
    return [dict(register=register,**value,percentage=round(100*value['present']/value['total'],2),below_75=4*value['present']<3*value['total']) for register,value in sorted(counts.items())]
def write_reports(rows,errors,outdir):
    """Write two fresh report files; output failures propagate explicitly."""
    outdir=Path(outdir);outdir.mkdir(parents=True,exist_ok=True)
    report={'denominator':'accepted observed sessions only','input_has_errors':bool(errors),
            'students':rows,'below_75':[r['register'] for r in rows if r['below_75']]}
    with (outdir/'attendance_report.json').open('w',encoding='utf-8') as stream:json.dump(report,stream,indent=2)
    with (outdir/'errors.csv').open('w',encoding='utf-8',newline='') as stream:
        writer=csv.DictWriter(stream,fieldnames=['file','line','type','message','raw']);writer.writeheader();writer.writerows(errors)
def process_month(folder,month,outdir):
    """Discover daily CSVs and create a visibly qualified monthly statement."""
    folder=Path(folder)
    if not folder.is_dir():raise FileNotFoundError(f'Input folder unavailable: {folder}')
    records,errors,audit=read_files(sorted(folder.glob('*.csv')),month)
    if not list(folder.glob('*.csv')):errors.append(dict(file=str(folder),line=0,type='NoInputFiles',message='no daily files found',raw=''))
    rows=statistics(records);write_reports(rows,errors,outdir)
    return rows,errors,audit

"""Continue past bad physical lines and missing department files."""
from pathlib import Path
from .validation import DEPARTMENTS,parse,InvalidRecord
def read_registrations(folder):
    """Return clean master dictionary, all error/info evidence and duplicate count."""
    master={};issues=[];duplicates=0
    for department in DEPARTMENTS:
        path=Path(folder)/(department+'.csv')
        try:
            with path.open('rb') as stream:
                for number,raw in enumerate(stream,1):
                    try:
                        record=parse(raw.decode('utf-8'),department)
                        register=record['register']
                        if register in master:
                            old=master[register]
                            same=(' '.join(old['name'].casefold().split())==' '.join(record['name'].casefold().split())
                                  and old['department']==record['department'] and old['email']==record['email'])
                            if not same:raise InvalidRecord('conflicting duplicate identity')
                            old['events'].update(record['events']);duplicates+=1
                            issues.append(dict(file=path.name,line=number,type='DUPLICATE_MERGED',message='events merged into existing student'))
                        else:master[register]=record
                    except (InvalidRecord,UnicodeDecodeError) as error:
                        issues.append(dict(file=path.name,line=number,type=type(error).__name__,message=str(error)))
        except OSError as error:issues.append(dict(file=path.name,line=0,type=type(error).__name__,message=str(error)))
    return master,issues,duplicates

import os
import tempfile
class InvalidRecord(Exception):
    """Raised when a line of the attendance file is not in the expected format."""
def parse_line(line):
    """'192311001,2026-10-08,P' -> ('192311001', '2026-10-08', 'P')"""
    parts = line.strip().split(",")
    if len(parts)!=3:raise InvalidRecord(f'expected 3 fields, found {len(parts)}')
    if parts[2] not in ('P','A'):raise InvalidRecord(f'invalid status {parts[2]!r}')
    return tuple(parts)
def summarise(path):
    present, absent, errors = 0, 0, []
    with open(path,encoding='utf-8') as stream:
        for number,line in enumerate(stream,1):
            try:_,_,status=parse_line(line)
            except InvalidRecord as error:errors.append((number,str(error)))
            else:
                if status=='P':present+=1
                else:absent+=1
    return present, absent, errors
data = ("192311001,2026-10-08,P\n192311002,2026-10-08,A\n"
        "192311003,2026-10-08\n192311004,2026-10-08,L\n")
with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False,
                                 encoding="utf-8") as tmp:
    tmp.write(data)
print(summarise(tmp.name))
os.remove(tmp.name)

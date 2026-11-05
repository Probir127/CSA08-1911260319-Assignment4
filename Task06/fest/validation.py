"""String-method validation for a bounded teaching registration format."""
import csv
DEPARTMENTS=('CSE','ECE','EEE','MECH','CIVIL')
EVENTS=('Dance','Music','Drama','Quiz','Art')
class InvalidRecord(ValueError):
    """A registration row is invalid."""
def valid_email(text):
    """Practical ASCII subset, not a complete international-email RFC validator."""
    if not text.isascii() or text.count('@')!=1 or any(c.isspace() for c in text):return False
    local,domain=text.split('@')
    if not local or local.startswith('.') or local.endswith('.') or '..' in local:return False
    if not all(c.isalnum() or c in '._+-' for c in local):return False
    labels=domain.split('.')
    return (len(labels)>=2 and all(label and not label.startswith('-') and not label.endswith('-') and all(c.isalnum() or c=='-' for c in label) for label in labels)
            and len(labels[-1])>=2 and labels[-1].isalpha())
def parse(line,department):
    """Validate identity, expected department, email and known event names."""
    try:fields=next(csv.reader([line.strip()],strict=True))
    except csv.Error as error:raise InvalidRecord('invalid CSV') from error
    if len(fields)!=5:raise InvalidRecord(f'expected 5 fields, found {len(fields)}')
    register,name,dept,email,events=[part.strip() for part in fields]
    if not register.isascii() or not register.isdigit() or not name:raise InvalidRecord('invalid student identity')
    if dept!=department or dept not in DEPARTMENTS:raise InvalidRecord('department mismatch')
    if not valid_email(email):raise InvalidRecord('invalid email')
    choices={event.strip() for event in events.split(';') if event.strip()}
    if not choices or not choices.issubset(EVENTS):raise InvalidRecord('missing or unknown event')
    return dict(register=register,name=name,department=dept,email=email.casefold(),events=choices)

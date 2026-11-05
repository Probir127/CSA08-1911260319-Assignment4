def percentage(present,total):
    """Return observed-session percentage, or None when no sessions exist."""
    return round(present*100/total,2) if total else None
def summarise(records):
    """Count accepted sessions per student."""
    counts={}
    for register,day,status in records:
        counts.setdefault(register,[0,0]);counts[register][0]+=status=='P';counts[register][1]+=1
    return {r:dict(present=p,total=t,percentage=percentage(p,t)) for r,(p,t) in sorted(counts.items())}

def consecutive_absent(records):
    """Find three consecutive calendar dates marked A, not merely three stored rows."""
    from datetime import date,timedelta
    by_id={};result=set()
    for register,day,status in records:by_id.setdefault(register,[]).append((date.fromisoformat(day),status))
    for register,days in by_id.items():
        previous=None;length=0
        for day,status in sorted(days):
            if status=='A':length=length+1 if previous is not None and day==previous+timedelta(days=1) else 1
            else:length=0
            if length>=3:result.add(register)
            previous=day
    return sorted(result)

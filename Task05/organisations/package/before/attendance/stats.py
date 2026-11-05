def percentage(present,total):
    """Return observed-session percentage, or None when no sessions exist."""
    return round(present*100/total,2) if total else None
def summarise(records):
    """Count accepted sessions per student."""
    counts={}
    for register,day,status in records:
        counts.setdefault(register,[0,0]);counts[register][0]+=status=='P';counts[register][1]+=1
    return {r:dict(present=p,total=t,percentage=percentage(p,t)) for r,(p,t) in sorted(counts.items())}

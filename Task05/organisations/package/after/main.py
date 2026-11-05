from attendance.reader import read_files
from attendance.stats import summarise,consecutive_absent
from attendance.report import write_report,write_absences
import sys
if __name__=='__main__':
    records,errors=read_files(sys.argv[1])
    summary=summarise(records)
    write_report(summary,errors,sys.argv[2])
    write_absences(consecutive_absent(records),sys.argv[2])

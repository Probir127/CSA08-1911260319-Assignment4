from utility import read_files,summarise,write_report
import sys
if __name__=='__main__':
    records,errors=read_files(sys.argv[1])
    summary=summarise(records)
    write_report(summary,errors,sys.argv[2])

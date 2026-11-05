"""Coordinate independent input and output responsibilities."""
from .reader import read_registrations
from .report import write_reports
def run(folder,outdir):
    """Bad rows/missing inputs are reported; fatal output errors are not suppressed."""
    master,issues,duplicates=read_registrations(folder)
    return write_reports(master,issues,duplicates,outdir)

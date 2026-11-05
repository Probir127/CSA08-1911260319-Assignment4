"""Append returns with delimiters, deterministic closure and an error log."""
import json,sys
def save_returns(books,path):
    """Append one nonblank physical book record per line."""
    with open(path,'a',encoding='utf-8') as log:
        for book in books:
            if book.strip():log.write(book.rstrip('\r\n')+'\n')
def process(day_file,log_path,error_path):
    """Return False and log known I/O failures; never hide programmer exceptions."""
    try:
        with open(day_file,encoding='utf-8') as stream:
            save_returns(stream,log_path)
    except (OSError,UnicodeError) as error:
        record=dict(file=str(day_file),type=type(error).__name__,message=str(error))
        try:
            with open(error_path,'a',encoding='utf-8') as stream:stream.write(json.dumps(record)+'\n')
        except OSError as log_error:print('Cannot save error log:',log_error,file=sys.stderr)
        return False
    return True

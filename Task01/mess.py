"""Exact money, physical-line CSV validation and a retained reject list."""
import csv,json,tempfile,io
from pathlib import Path
from decimal import Decimal,InvalidOperation
def summarise(filename):
    """Return total, joined report and (line, raw text, reason) rejects."""
    total=Decimal('0.00');parts=[];rejected=[]
    with open(filename,'rb') as stream:
        for number,raw in enumerate(stream,1):
            try:
                text=raw.decode('utf-8').strip()
                if not text:continue
                fields=next(csv.reader([text],strict=True))
                if len(fields)!=3:raise ValueError('expected register,name,amount')
                register,name,amount_text=[field.strip() for field in fields]
                if not register.isascii() or not register.isdigit() or not name:raise ValueError('invalid identity')
                amount=Decimal(amount_text)
                if not amount.is_finite() or amount<0:raise ValueError('invalid amount')
                rounded=amount.quantize(Decimal('0.01'))
                if amount!=rounded:raise ValueError('amount has fractional paise')
            except (UnicodeDecodeError,csv.Error,ValueError,InvalidOperation) as error:
                rejected.append((number,raw.decode('utf-8',errors='replace').rstrip(),str(error)))
                continue
            total+=rounded
            buffer=io.StringIO(newline='')
            csv.writer(buffer,lineterminator='\n').writerow((register,name,f'{rounded:.2f}'))
            parts.append(buffer.getvalue())
    return total,''.join(parts),rejected
if __name__=='__main__':
    base=Path(__file__).parent;total,report,rejects=summarise(base/'input.csv')
    assert total==Decimal('2250.75') and len(rejects)==3
    (base/'report.csv').write_text(report)
    (base/'rejected.json').write_text(json.dumps(rejects,indent=2))
    print(report,end='');print('Total:',total,'Rejects:',rejects)
    with tempfile.TemporaryDirectory() as folder:
        path=Path(folder)/'large.csv'
        with path.open('w',encoding='utf-8') as stream:
            for i in range(50000):stream.write(f'{i:010d},Student {i},1250.50\n')
        large,_,errors=summarise(path)
        assert large==Decimal('62525000.00') and errors==[]
        print('50000-line total:',large,'PASS')
        with tempfile.TemporaryDirectory() as folder:
            quoted=Path(folder)/'quoted.csv';quoted.write_text('1911260001,"Student, A",10.00\n')
            value,text,errors=summarise(quoted)
            assert value==Decimal('10.00') and errors==[]
            assert next(csv.reader(text.splitlines()))==['1911260001','Student, A','10.00']
            print('Quoted-comma name parses and writes as valid CSV PASS')

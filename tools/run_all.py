"""Run CO4 examples, assertions and all before/after organisation variants."""
from pathlib import Path
import subprocess,sys,json

ROOT=Path(__file__).resolve().parents[1]
JOBS={'Task01':['mess.py'],'Task02':['demo.py'],'Task03':['complete_code.py','errors_demo.py'],
      'Task04':['demo.py'],'Task05':['compare.py'],'Task06':['demo.py','duplicate_benchmark.py']}

def main():
    """Capture actual output and stop on an unexpected program/test failure."""
    results=[]
    for task,files in JOBS.items():
        chunks=[]
        for file in files:
            relative=f'{task}/{file}'
            result=subprocess.run([sys.executable,relative],cwd=ROOT,capture_output=True,
                                  text=True,check=True,timeout=90)
            chunks.append(f'$ python3 {relative}\n'+result.stdout)
            if result.stderr:chunks.append('STDERR:\n'+result.stderr)
            results.append({'program':relative,'exit_code':result.returncode})
        (ROOT/task/'output.txt').write_text('\n'.join(chunks));print(task,'PASS',flush=True)
    (ROOT/'verification.json').write_text(json.dumps({'python':sys.version,'results':results},indent=2)+'\n')
    print('All CO4 examples and assertions passed.')

if __name__=='__main__':main()

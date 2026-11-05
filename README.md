# CSA08 - Assignment 4 (CO4)

Student Name: PROBIR SAHA SHOHOM  
Register Number: 1911260319  
Course: CSA08 - Python Programming  
Repository: https://github.com/Probir127/CSA08-1911260319-Assignment4

[PDF report](CSA08_Assignment4_Solution.pdf) | [Text report](SOLUTIONS.md)

Python 3.10+; standard-library runtime only. See verification.json for the execution version. No third-party runtime libraries are required.

## Run all tasks

```text
python3 tools/run_all.py
```

Run without -O, which disables assertions. The runner captures actual output and executes all four Task05 organisations both before and after the requirement change.

| Task | Command | Result |
|---|---|---|
| 1 | `python3 Task01/mess.py` | Exact 2250.75 fixture and 62525000.00 large total; rejects retained |
| 2 | `python3 Task02/demo.py` | Observed-session percentages 50% and 100%; bad/duplicate rows logged |
| 3 | `python3 Task03/complete_code.py`; `python3 Task03/errors_demo.py` | Required output, missing/encoding failures, cause chain, finally audit and hidden-typo evidence |
| 4 | `python3 Task04/demo.py` | Three-day defect reproduced; repaired log has six separate lines; injected write failure closes handle |
| 5 | `python3 Task05/compare.py` | All eight variants agree; actual changed-file counts 1, 2, 3, 3; only 1911260001 qualifies |
| 6 | `python3 Task06/demo.py`; `python3 Task06/duplicate_benchmark.py` | Four clean students, duplicate merge, three rejected rows, missing department handled; duplicate methods benchmarked |

## Inputs and output evidence

Task01 includes input.csv, report.csv and rejected.json. Task02 includes two daily CSVs and monthly report/error outputs. Task03 includes the required sample input plus generated fault-injection evidence. Task04 includes three sample daily files and repaired/error logs. Task05 contains all before/after Python sources, shared inputs, generated reports and change_evidence.json. Task06 includes four department CSVs; CIVIL.csv is intentionally missing to test continued processing. Its results contain master.csv, five event files, errors.csv and summary.json.

To run one Task05 layout, pass the input and output folder paths:

```text
python3 Task05/organisations/package/after/main.py Task05/inputs Task05/custom_results
```

The other layouts accept the same two arguments. The detailed report explains assumptions, partial-input attendance qualifications, duplicate policies and limits of the email validator. Permission and write errors are explicitly labelled injected tests; no real permission changes are made.

Output PNGs are labelled renderings of genuine captured stdout, not terminal screenshots. Capture faculty-required terminal screenshots when personally running the programs. Review and understand the work and submit the repository link to faculty. No faculty invitation or final course submission has been performed.

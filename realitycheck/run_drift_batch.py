"""Run several drift assessments one after another, because each rewrites the same seed file.

Usage: python run_drift_batch.py R02 2023-05-10:assess 2024-03-14 2024-03-14:assess
"""
import sys

import run_drift

if __name__ == '__main__':
    cid = sys.argv[1].upper()
    for spec in sys.argv[2:]:
        date, _, flag = spec.partition(':')
        code = run_drift.main(cid, date, flag == 'assess')
        if code:
            raise SystemExit(code)

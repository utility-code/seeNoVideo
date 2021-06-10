import argparse as ap
from pathlib import Path

from src.backbone import *

arg = ap.ArgumentParser()
arg.add_argument("-d", help="direct text or not", required=False, action="store_true")
arg.add_argument("-t", help="direct text or file name", required=False)
arg.add_argument("-f", help="text path", type=str)
arg.add_argument("-o", help="output name if multiple files", required=False)

ag = arg.parse_args()
print(ag)

# Main functions
ag.f = Path(ag.f)
print(ag.f)
assert Path.exists(ag.f) == True
clean_up_fully(ag.f)

if ag.d:
    run_process(string=ag.t, fpath=ag.f)
else:
    clean_up_fully(ag.f)
    with open(Path(ag.f / ag.t), "r") as st:
        run_process(string=st.read(), fpath=ag.f)

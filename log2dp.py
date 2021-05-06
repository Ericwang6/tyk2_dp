import dpdata
import os, glob
from functools import reduce
from collections import Iterable
import numpy as np


def log2dp(logs, system_dir=None, type_map=None):
    systs = []
    if not isinstance(logs, str):
        for log in logs:
            ss = dpdata.LabeledSystem(log, fmt='gaussian/log', type_map=type_map)
            systs.append(ss)
        all_syst = reduce(lambda x, y: x+y, systs)
    else:
        all_syst = dpdata.LabeledSystem(logs, fmt='gaussian/log', type_map=type_map)
    if system_dir:
        all_syst.to_deepmd_npy(system_dir)
    return all_syst


if __name__ == "__main__":
    ligs = np.loadtxt("SYSTEMS.txt", dtype=np.str)
    for lig in ligs:
        logs = glob.glob(f"gaussian/{lig}/*log")
        syst = log2dp(logs, f"data/{lig}")
        print(lig, syst.get_nframes())
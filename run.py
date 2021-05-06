import os, glob
import numpy as np


def write_pbs(gjfs, gjf_dir=None, batch=20, cache_prefix="cache", submit=False,
              env="~/gaussian/g09.bashrc"):
    if not gjf_dir:
        gjf_dir = os.path.dirname(gjfs[0])
    wdir = os.path.join(gjf_dir, cache_prefix)
    if not os.path.exists(wdir):
        os.mkdir(wdir)
    cnt = 0
    for ii in range(0, len(gjfs), batch):
        with open(os.path.join(wdir, f'{cnt}.pbs'), "w+") as f:
            f.write("#!/bin/bash\n#PBS -N gaussian\n#PBS -q C_32_64\n#PBS -l select=1:ncpus=32\n")
            f.write(f"source {env}\n")
            f.write("cd $PBS_O_WORKDIR\n")
            f.write(f"cd {os.path.relpath(gjf_dir, wdir)}\n")
            for gjf in gjfs[ii: ii+batch]:
                f.write(f"g16 {os.path.basename(gjf)}\n")
        # submit
        if submit:
            os.system(f"cd {wdir} && qsub {cnt}.pbs")
        cnt += 1

if __name__ == "__main__":
    ligs = np.loadtxt("SYSTEMS.txt", dtype=np.str)
    for lig in ligs:
        gjf_dir = f"gaussian/{lig}"
        gjfs = list(glob.glob(os.path.join(gjf_dir, "*gjf")))
        write_pbs(gjfs, gjf_dir, batch=200, submit=True)

    

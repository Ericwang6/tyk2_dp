import dpdata
import numpy as np
import os


def make_gaussian_input(system,
                        frame_idx=0, 
                        fname=None, 
                        header='#force wB97XD/6-31G(d)',
                        foot="",
                        title='mol', 
                        charge=0, 
                        mult=1):
    ret = header + "\n\n" + title + "\n\n" + str(charge) + " " + str(mult) + "\n"
    coord = system.data["coords"][frame_idx].reshape(-1, 3)
    for atype, c in zip(system.data["atom_types"], coord):
        ret += system.data["atom_names"][atype] + " "
        ret += " ".join([str(x) for x in c])
        ret += "\n"
    if foot:
        ret += "\n" + foot + "\n"
    else:
        ret += "\n"
    if fname:
        if not os.path.exists(os.path.dirname(fname)):
            os.mkdir(os.path.dirname(fname))
        with open(fname, "w+") as f:
            f.write(ret)
    return ret


if __name__ == "__main__":
    ligs = np.loadtxt("SYSTEMS.txt", dtype=np.str)
    for lig in ligs:
        gro_file = f"ligands_5ns/{lig}/md_traj.gro"
        system = dpdata.System(gro_file, fmt='gromacs/gro', type_map=['H','C','N','O','Cl'])
        # the first 0.5ns traj
        for frame_idx in range(system.get_nframes() // 10):
            make_gaussian_input(system,
                                frame_idx=frame_idx,
                                fname=f"gaussian/{lig}/{frame_idx}.gjf",
                                header="%nproc=32\n%mem=40GB\n#force wB97XD/6-31G(d)")

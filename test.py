import dpdata
import deepmd.DeepPot as DP
import numpy as np

gelu_model = DP("models/gelu/frozen_model.pb")
tanh_model = DP("models/tanh/frozen_model.pb")

ligs = np.loadtxt("SYSTEMS.txt", dtype=np.str)
for lig in ligs:
    system = dpdata.LabeledSystem(f"data/{lig}", fmt='deepmd/npy')
    energy = system['energies'].reshape(-1, 1)
    forces = system['forces'].reshape(-1, 1)

    gelu_predict_sys = system.predict(gelu_model)
    gelu_energy = gelu_predict_sys['energies'].reshape(-1, 1)
    gelu_forces = gelu_predict_sys['forces'].reshape(-1, 1)
    gelu_energy_eval = np.concatenate((energy, gelu_energy), axis=1)
    gelu_forces_eval = np.concatenate((forces, gelu_forces), axis=1)
    np.savetxt(f"eval/gelu/{lig}_e.txt", gelu_energy_eval, header="e_true, e_pred")
    np.savetxt(f"eval/gelu/{lig}_f.txt", gelu_forces_eval, header="f_true, f_pred")

    tanh_predict_sys = system.predict(tanh_model)
    tanh_energy = tanh_predict_sys['energies'].reshape(-1, 1)
    tanh_forces = tanh_predict_sys['forces'].reshape(-1, 1)
    tanh_energy_eval = np.concatenate((energy, tanh_energy), axis=1)
    tanh_forces_eval = np.concatenate((forces, tanh_forces), axis=1)
    np.savetxt(f"eval/tanh/{lig}_e.txt", tanh_energy_eval, header="e_true, e_pred")
    np.savetxt(f"eval/tanh/{lig}_f.txt", tanh_forces_eval, header="f_true, f_pred")
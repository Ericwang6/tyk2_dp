import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import mean_squared_error as mse
from sklearn.metrics import mean_absolute_error as mae
import matplotlib.pyplot as plt

def rmse(y_true, y_pred):
    return np.sqrt(mse(y_true, y_pred))

def calc_rmse(eval_res):
    return rmse(eval_res[:, 0], eval_res[:, 1])

def calc_mse(eval_res):
    return mse(eval_res[:, 0], eval_res[:, 1])

def calc_mae(eval_res):
    return mae(eval_res[:, 0], eval_res[:, 1])

def calc_err(eval_res):
    return eval_res[:, 1] - eval_res[:, 0]

def get_eval_result(eval_list, fmt='raw'):
    if fmt == "raw":
        eval_res = np.vstack([np.loadtxt(fname) for fname in eval_list])
    elif fmt == "npy":
        eval_res = np.vstack([np.load(fname) for fname in eval_list])
    else:
        raise ValueError("Invalid fmt argument: {}".format(fmt))
    return eval_res

def get_distribution(err, num_bins=500):
    n, bin_, _ = plt.hist(err, density=1, bins=num_bins)
    bin_ = (bin_[1:] + bin_[:-1]) / 2
    return n, bin_

def get_evals(e_list, f_list, fmt="raw"):
    assert len(e_list) == len(f_list) and len(e_list) != 0
    if fmt == "raw" or fmt == "npy":
        e_eval = get_eval_result(e_list, fmt)
        f_eval = get_eval_result(f_list, fmt)
    elif isinstance(fmt, list):
        e_eval = get_eval_result(e_list, fmt[0])
        f_eval = get_eval_result(f_list, fmt[1])
    else:
        raise TypeError("Invaild format for fmt argument: str or list, not {}".format(type(fmt)))
    return e_eval, f_eval

def get_dists(e_err, f_err, e_num_bins=500, f_num_bins=500):
    e_n, e_bins = get_distribution(e_err, e_num_bins)
    f_n, f_bins = get_distribution(f_err, f_num_bins)
    return e_n, e_bins, f_n, f_bins

def analyze_from_evals(e_eval, f_eval, e_num_bins=500, f_num_bins=500):
    e_err, f_err = map(calc_err, (e_eval, f_eval))
    e_rmse, f_rmse = map(calc_rmse, (e_eval, f_eval))
    e_mse, f_mse = map(calc_mse, (e_eval, f_eval))
    e_mae, f_mae = map(calc_mae, (e_eval, f_eval))
    e_n, e_bins = get_distribution(e_err, e_num_bins)
    f_n, f_bins = get_distribution(f_err, f_num_bins)
    res = {'e_eval': e_eval, 'f_eval': f_eval,
           'e_err': e_err, 'f_err': f_err,
           'e_n': e_n, 'e_bins': e_bins,
           'f_n': f_n, 'f_bins': f_bins,
           'e_rmse': e_rmse, 'f_rmse': f_rmse,
           'e_mse': e_mse, 'f_mse': f_mse,
           'e_mae': e_mae, 'f_mae': f_mae}
    return res

def analyze_from_lists(e_list, f_list, fmt='raw', e_num_bins=500, f_num_bins=500):
    assert len(e_list) == len(f_list)
    assert len(e_list) != 0
    e_eval, f_eval = get_evals(e_list, f_list, fmt=fmt)
    res = analyze_from_evals(e_eval, f_eval, e_num_bins, f_num_bins)
    return res


if __name__ == "__main__":
    ligs = np.loadtxt("SYSTEMS.txt", dtype=np.str)
    gelu_e_list = [f"eval/gelu/{lig}_e.txt" for lig in ligs]
    gelu_f_list = [f"eval/gelu/{lig}_f.txt" for lig in ligs]
    gelu_analysis = analyze_from_lists(gelu_e_list, gelu_f_list, fmt='raw', e_num_bins=100, f_num_bins=100)

    tanh_e_list = [f"eval/tanh/{lig}_e.txt" for lig in ligs]
    tanh_f_list = [f"eval/tanh/{lig}_f.txt" for lig in ligs]
    tanh_analysis = analyze_from_lists(tanh_e_list, tanh_f_list, fmt='raw', e_num_bins=100, f_num_bins=100)

    fig, ax = plt.subplots(1, 2, figsize=(12,6), constrained_layout=True)
    ax[0].plot(gelu_analysis['e_bins'], gelu_analysis['e_n'], label='gelu')
    ax[0].plot(tanh_analysis['e_bins'], tanh_analysis['e_n'], label='tanh')
    ax[0].set_xlabel("Error of energy (eV)")
    ax[0].set_ylabel("Probability Distribution")
    ax[0].legend()

    ax[1].plot(gelu_analysis['f_bins'], gelu_analysis['f_n'], label='gelu')
    ax[1].plot(tanh_analysis['f_bins'], tanh_analysis['f_n'], label='tanh')
    ax[1].set_xlabel("Error of forces (eV/A)")
    ax[1].set_ylabel("Probability Distribution")
    ax[1].legend()
    fig.savefig("eval/error_distribution.png", dpi=300)

    print("gelu\n-----")
    print(f"Energy RMSE: {gelu_analysis['e_rmse']:.4f} eV")
    print(f"Force  RMSE: {gelu_analysis['f_rmse']:.4f} eV/A")
    print("")
    print("tanh\n-----")
    print(f"Energy RMSE: {tanh_analysis['e_rmse']:.4f} eV")
    print(f"Force  RMSE: {tanh_analysis['f_rmse']:.4f} eV/A")
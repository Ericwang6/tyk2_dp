import numpy as np
import matplotlib.pyplot as plt
import json
import sys


def parse_json(json_file):
    with open(json_file, 'r') as f:
        jdata = json.load(f)
    return jdata


def check_jdata(jdata):
    keys = list(jdata.keys())
    if 'lcurves' not in keys:
        raise KeyError("'lcurves' is missed")
    if 'fig' not in keys:
        raise KeyError("'fig' is missed")
    if 'labels' in keys:
        if len(jdata['labels']) != len(jdata['lcurves']):
            raise ValueError("length of labels is not equal to lcurves")
    if jdata['mode'] not in ['tst', 'trn']:
        raise ValueError(f"Invalid mode: {jdata['mode']}, please set mode to 'tst' or 'trn'")


def get_args(json_file):
    jdata = parse_json(json_file)
    check_jdata(jdata)
    args = {}
    args['lcurves'] = jdata['lcurves']
    args['fig'] = jdata['fig']
    args['labels'] = jdata.get('labels', [])
    args['mode'] = jdata.get('mode', 'trn')
    args['win_length'] = jdata.get('win_length', 500)
    args['loglog'] = jdata.get('loglog', True)
    return args


def get_data(fname, win_len=100):
    data = np.loadtxt(fname, skiprows=2)[:, :-1]
    nframe = data.shape[0]
    data = np.mean(data[:(nframe // win_len) * win_len].reshape(-1, win_len, 7), axis=1)
    dt = {'tst': data[:, 1], 'trn': data[:, 2],
          'e_tst': data[:, 3], 'e_trn': data[:, 4],
          'f_tst': data[:, 5], 'f_trn': data[:, 6],
          'batch': data[:, 0]}
    return dt


def plot(lcurves, fig_path, labels=[], mode='trn', win_length=500, loglog=True):
    fig, axes = plt.subplots(1, 3, figsize=(15, 5), constrained_layout=True)
    axes[0].set_ylabel("Loss")
    axes[1].set_ylabel("RMSE Energy (eV/atom)")
    axes[2].set_ylabel("RMSE Force (eV/A)")
    if not labels:
        labels = lcurves.copy()
    for fname, label in zip(lcurves, labels):
        dt = get_data(fname, win_len=win_length)
        batch = dt['batch']
        if loglog:
            axes[0].loglog(batch, dt[f'{mode}'], label=label)
            axes[1].loglog(batch, dt[f'e_{mode}'], label=label)
            axes[2].loglog(batch, dt[f'f_{mode}'], label=label)
        else:
            axes[0].plot(batch, dt[f'{mode}'], label=label)
            axes[1].plot(batch, dt[f'e_{mode}'], label=label)
            axes[2].plot(batch, dt[f'f_{mode}'], label=label)
    
    for ax in axes:
        ax.legend()
        ax.set_xlabel("Training Step")
    fig.savefig(fig_path, dpi=300)
    plt.close(fig)


if __name__ == "__main__":
    json_file = sys.argv[1]
    args = get_args(json_file)
    plot(lcurves=args['lcurves'],
         labels=args['labels'],
         fig_path=args['fig'],
         mode=args['mode'],
         win_length=args['win_length'],
         loglog=args['loglog'])

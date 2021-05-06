# DP model for TYK2
This repository contains scripts for the construction workflow of Deep Potential model for tyk2.

+ `SYSTEMS.txt`: name of 15 ligands
+ `prepare_gaussian_input.py`: prepare Gaussian input files from conformers sampled by GROMACS
+ `gaussian.tar`: input and output of Gaussian
+ `log2dp.py`: convert gaussian log file to deepmd format
+ `lcurve_plot.py`: script to visualize learning curve
+ `plot.json`: a sample of settings for plot learning curve：
   - `win_length`: the window length to smooth learning curve
   - `fig`: the directory to save figure
   - `mode`: "trn" or "tst", whether to use training or testing loss in lcurve.out file
   - `loglog`: true or false, whether to change axis to log scaling
   - `lcurves`: the lcurve.out files to plot
   - `labels`: the legends for each file in `lcurves`
To generate a figure for learning curve, just run `python lcurve_plot.py plot.json`
## ligands_5ns
+ `ligands_5ns/*/md_traj.gro`: trajecory of 5-ns simulation of 15 ligands in solvated phase
## models
+ `compare.png`: a comparison between learning curves of models with tanh/gelu activation function
+ `gelu`/`tanh`: contains `frozen_model.pb`, `lcurve.out` and `input.json` files


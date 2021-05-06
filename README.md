## DP model for TYK2
This repository contains scripts for the construction workflow of Deep Potential model for tyk2.

+ `SYSTEMS.txt`: name of 15 ligands
+ `ligands_5ns/*/md_traj.gro`: trajecory of 5-ns simulation of 15 ligands in solvated phase
+ `prepare_gaussian_input.py`: prepare gaussian input files from conformers sampled by GROMACS
+ `log2dp`: convert gaussian log file to deepmd format
+ `lcurve_plot.py`: script to visualize learning curve
+ `plot.json`: a sample of settings for plot learning curve：
   - `win_length`: the window length to smooth learning curve
   - `fig`: the directory to save figure
   - `mode`: "trn" or "tst", whether to use training or testing loss in lcurve.out file
   - `loglog`: true or false, whether to change axis to log scaling
   - `lcurves`: the lcurve.out files to plot
   - `labels`: the legends for each file in `lcurves`

To generate a figure for learning curve, just run `python lcurve_plot.py plot.json`

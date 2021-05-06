#!/bin/bash -l
#SBATCH -N 1
#SBATCH --ntasks-per-node 8
#SBATCH -t 120:0:0
#SBATCH --partition all
#SBATCH --nodelist=gpu06
#SBATCH --gres=gpu:1
#SBATCH --mem=20G
source activate /data1/anguse/yingze/deepmd-kit-1.3.3
dp train input.json
dp freeze -o frozen_model.pb

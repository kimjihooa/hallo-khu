#!/usr/bin/bash

#SBATCH -J test-run
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-gpu=8
#SBATCH --mem-per-gpu=32G
#SBATCH -p batch_ce_ugrad
#SBATCH -w moana-r5
#SBATCH -t 1-0
#SBATCH -o logs/slurm-%A.out


pwd
which python
hostname
tar -xvf /data/datasets/tarfiles/CelebV_Images.tar -C /local_datasets
tar -xvf /data/datasets/tarfiles/CelebV_Audios.tar -C /local_datasets
python test.py

exit 0

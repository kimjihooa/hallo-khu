#!/usr/bin/bash

#SBATCH -J test-run
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-gpu=8
#SBATCH --mem-per-gpu=32G
#SBATCH -p batch_ce_ugrad
#SBATCH -w moana-r1
#SBATCH -t 1-0
#SBATCH -o logs/slurm-%A.out


pwd
which python
hostname
rm -rf Images
rm -rf Audios
mkdir /local_datasets/Images
mkdir /local_datasets/Audios
tar -xvf /data/datasets/tarfiles/HDTF_Images.tar -C /local_datasets/Images
tar -xvf /data/datasets/tarfiles/HDTF_Audios.tar -C /local_datasets/Audios
python remove_shortest.py
python test.py

exit 0

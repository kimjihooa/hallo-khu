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

rm -rf /local_datasets/CelebV
mkdir /local_datasets/imsi
tar -xvf /data/datasets/tarfiles/CelebV.tar -C /local_datasets/imsi
python remove_random.py
python convert_25fps.py
rm -rf /local_datasets/imsi
python -m scripts.data_preprocess --input_dir /local_datasets/CelebV/videos --step 1
python -m scripts.data_preprocess --input_dir /local_datasets/CelebV/videos --step 2

tar -cvf /local_datasets/CelebV_preprocessed.tar /local_datasets/CelebV
mv /local_datasets/CelebV_preprocessed.tar /data/datasets/tarfiles/CelebV_preprocessed.tar
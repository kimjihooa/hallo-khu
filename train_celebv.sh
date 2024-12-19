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

#rm -rf /local_datasets/CelebV
#tar -xvf /data/datasets/tarfiles/CelebV_preprocessed.tar -C /local_datasets/
#python remove_random.py
#python convert_25fps.py
#rm -rf /local_datasets/imsi
#
#python -m scripts.data_preprocess --input_dir /local_datasets/CelebV/videos --step 1
#python -m scripts.data_preprocess --input_dir /local_datasets/CelebV/videos --step 2

#python scripts/extract_meta_info_stage1.py -r /local_datasets/CelebV -n dataset_name
#python scripts/extract_meta_info_stage2.py -r /local_datasets/CelebV -n dataset_name

accelerate launch -m \
  --config_file accelerate_config.yaml \
  --machine_rank 0 \
  --main_process_ip 0.0.0.0 \
  --main_process_port 20055 \
  --num_machines 1 \
  --num_processes 1 \
  scripts.train_stage1 --config ./configs/train/stage1.yaml
exit 0

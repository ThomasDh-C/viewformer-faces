#!/bin/bash
#SBATCH --job-name=viewformer      # create a short name for your job
#SBATCH --nodes=1                # node count
#SBATCH --ntasks=1               # total number of tasks across all nodes
#SBATCH --cpus-per-task=5        # cpu-cores per task (>1 if multi-threaded tasks)
#SBATCH --mem-per-cpu=10G         # memory per cpu-core (4G is default)
#SBATCH --gres=gpu:1             # number of gpus per node
#SBATCH --time=00:05:00          # total run time limit (HH:MM:SS)
#SBATCH --mail-type=end,fail     # send email when job ends
#SBATCH --mail-user=tmd4@princeton.edu

cd /home/tmd4/viewformer-faces/notebooks
module purge
module load anaconda3/2022.5
conda activate viewformer2
# python3 -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"

# only works with the old vqgan_th.py
viewformer-cli generate-codes \
    --model "/scratch/network/tmd4/viewformer/models/fei-codebook-th/last.ckpt" \
    --dataset "/scratch/network/tmd4/viewformer/datasets/feitrue" \
    --output "/scratch/network/tmd4/viewformer/datasets/feitrue_cb" \
    --batch-size 10 

# need pytorch checkpoint for interiornet
viewformer-cli train finetune-transformer \
    --dataset "/scratch/network/tmd4/viewformer/datasets/feitrue_cb" \
    --codebook-model "/scratch/network/tmd4/viewformer/models/fei-codebook-th/last.ckpt" \
    --sequence-size 11 \
    --n-loss-skip 1 \
    --batch-size 10 \
    --localization-weight 5 \
    --gradient-clip-val 1. \
    --learning-rate 1e-4 \
    --total-steps 100000 \
    --epochs 120 \
    --weight-decay 0.05 \
    --job-dir "/scratch/network/tmd4/viewformer/models/fei-transformer" \
    --pose-multiplier 0.05 \
    --checkpoint "/scratch/network/tmd4/viewformer/models/interiornet-transformer-tf/model"
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

viewformer-cli train codebook \
    --dataset "/scratch/network/tmd4/viewformer/datasets/feitrue" \
    --job-dir "/scratch/network/tmd4/viewformer/models/fei-codebook-th" \
    --num-gpus 1 \
    --batch-size 10 \
    --n-embed 1024 \
    --learning-rate 1.584e-3 \
    --total-steps 201000 \
    --num-val-workers 1 \
    --num-workers 1 \
    --resume-from-checkpoint "/scratch/network/tmd4/viewformer/models/interiornet-codebook-th/model.ckpt"

# module load anaconda3/2022.5
# conda activate viewformer2
# tensorboard --logdir=/scratch/network/tmd4/viewformer/models/fei-codebook-th
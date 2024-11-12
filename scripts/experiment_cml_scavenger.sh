#!/bin/sh
#SBATCH --time=3-00:00:00
#SBATCH --partition=cml-scavenger
#SBATCH --qos=cml-scavenger
#SBATCH --account=cml-scavenger
#SBATCH --mem=40gb 
#SBATCH --ntasks=4
#SBATCH --gres=gpu:rtxa6000:1

cd ..
source /nfshomes/anirudhs/.bashrc
conda activate ctraffic
python main.py --config="MARL/configs/algs/$1.yaml" --cityflow-config="configs/cityflow/$2.yml" --constraint=$3 --seed=$4
wait
# CMARL-Traffic

Source code of "A Constrained Multi-Agent Reinforcement Learning Approach to Traffic Management", which proposes a new method for constrained MARL on Adaptive Traffic Signal Control (ATSC), Multi-Agent Proximal Policy Optimization with Lagrange Cost Estimator (MAPPO-LCE).

# Usage

We use [CityFlow](https://github.com/zyr17/CityFlow) as traffic simulator.

To run our code, use python 3.9.20 in a conda environment.

## Build
```bash
conda install env create -f environment.yml
conda activate ctraffic
git clone git@github.com:zyr17/CityFlow.git
cd CityFlow && pip install . --upgrade && cd ..
git clone git@github.com:Asatheesh6561/CMARL-Traffic.git
cd CMARL-Traffic
conda install -c conda-forge libstdcxx-ng
```

## Run

As an example, to run MAPPO on the HZ environment with the PhaseSkip constraint:
```bash
python main.py --cityflow-config=configs/cityflow/HZ.yml --config=MARL/configs/algs/mappo.yaml --constraint=PhaseSkip
```

You may need to change the `local_results_path` in config files, as well as `arg['results_path']` in `main.py`.

Run different algorithms by substituting the corresponding .yml files in the arguments. The constraint choices are listed in `Environment/utils/arguments.py`.

## Environment

The definition of the gym environment is in `Environment/cityflow_env.py`. It runs in another 
process managed by the environment run files in `MARL/run`.

## Dataset

We provide the HZ, JN, and NY datasets in the `data.tgz` tarball. You can also find the original dataset files on the [COLight](https://github.com/wingsweihua/colight) github page. To use them, run
```
tar -zxvf Environment/data.tar
```

## Arguments and Configs

We parse arguments by `Environment/utils/argument.py`. The config for CityFlow and main
process are two separate configs. All CityFlow configs are stored in 
`configs/cityflow`, and algorithm hyperparameters are stored in `MARL/configs`.

## Logs

We use wandb for logging, but this can be disabled by setting `--enable-wandb=False`.

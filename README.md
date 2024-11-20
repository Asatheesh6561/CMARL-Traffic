# CMARL-Traffic

Source code of "A Constrained Multi-Agent Reinforcement Learning Approach to Traffic Management", which proposes a new method for constrained MARL on Adaptive Traffic Signal Control (ATSC), Multi-Agent Proximal Policy Optimization with Lagrange Cost Estimator (MAPPO-LCE).

# Usage

We use [CityFlow](https://github.com/zyr17/CityFlow) as traffic simulator. Note that we use a a forked version of the original CityFlow that was originally created for [UniLight](https://github.com/zyr17/UniLight). This moves some python code to the C++ backend. 

To run our code, use python 3.9.20 in a conda environment.

## Build
```bash
git clone git@github.com:zyr17/CityFlow.git
cd CityFlow && pip install . --upgrade && cd ..
git clone git@github.com:Asatheesh6561/CMARL-Traffic.git
cd CMARL-Traffic && tar zxf data.tgz && pip install -r requirements.txt
conda install -c conda-forge libstdcxx-ng
```

## Run

For training:
```bash
python main.py --cityflow-config=configs/cityflow/HZ.yml --config=MARL/configs/algs/maa2cc.yaml
```

## Environment

The definition of the gym environment is in `Environment/cityflow_env.py`. It runs in another 
process managed by `[MARL/run/episode_run.py]`.

## Dataset

You can find the datasets in `Environment/data`, which has `SH1`, `SH2`, `NY`, `JN`, and `HZ` after extracting the `data.tgz` tarball. You can also find the original data files on the [COLight](https://github.com/wingsweihua/colight) github page.

## Arguments and Configs

We parse arguments by `Environment/utils/argument.py`. The config for CityFlow and main
process are two separate configs. All CityFlow configs are stored in 
`configs/cityflow`, and algorithm hyperparameters are stored in `MARL/configs`.

## Logs

We use wandb for logging, but this can be disabled by setting `--enable-wandb=False`.

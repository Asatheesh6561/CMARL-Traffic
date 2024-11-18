# CMARL-Traffic

Source code of "A Constrained Multi-Agent Reinforcement Learning Approach to Traffic Management", which proposes a new method for constrained MARL, MAPPO-LCE.

# Usage

We use [CityFlow](https://github.com/zyr17/CityFlow) as traffic simulator. Note that we use a a forked version of the original CityFlow that was originally created for the [UniLight](https://github.com/zyr17/UniLight) paper. This moves some python code to the C++ backend. 

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
For testing:
```bash
python main.py --cityflow-config=configs/cityflow/HZ.yml --config=MARL/configs/algs/maa2cc.yaml--preload-model-file ${PATH_TO_MODEL_PT} --test-round 10
```

# Details

## Environment

The definition of environment is in `Environment/cityflow_env.py`. It runs in another 
process managed by `[envs/SubProcVecEnv.py]`.

## Dataset

You can find the datasets in `Environment/data`, which has `SH1`, `SH2`, `NY`, `JN`, and `HZ` after extracting the `data.tgz` tarball.

## Agents

The agents and communication mainly defined in `[rl/agents/NewModelAgent.py]`,
which is wrapped by `[rl/multiAgents/NewModelMultiAgent.py]`, and its `[nn.Module]`
is defined in `[rl/models/innerModels/NewModel.py]`. 

## Arguments and Configs

We parse arguments by `Environment/utils/argument.py`. The config for CityFlow and main
process are two separate configs. All CityFlow configs are stored in 
`configs/cityflow`, and `configs/main` for main configs.

## Logs

When training starts, all logs will save in `logs/${TARGET}` folder, including
full logs, configs, CityFlow replay files, and saved models. The
target foler name is start with current time. There are two exceptions, 
output of TensorBoard is in `runs`, and output of wandb is in `wandb`. 
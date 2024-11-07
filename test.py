import sys
import yaml
import time

from Environment.utils.arguments import parse_args
from Environment import make_env
from tqdm import tqdm


def _get_config(config_file):
    if config_file is not None:
        with open(
            config_file,
            "r",
        ) as f:
            try:
                config_dict = yaml.safe_load(f)
            except yaml.YAMLError as exc:
                assert False, "{} error: {}".format(config_file, exc)
        return config_dict
    else:
        return {}


if __name__ == "__main__":
    args = sys.argv
    args = vars(parse_args(args))
    env = make_env(args, ["DefaultWrapper"])
    for _ in tqdm(range(args["simulate_time"])):
        action = [i.sample() for i in env.action_space]
        obs, reward, done, info = env.step(action)

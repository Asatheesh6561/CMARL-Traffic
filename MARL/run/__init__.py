from .parallel_run import run as parallel_run
from .episode_run import run as episode_run
REGISTRY = {}

REGISTRY["ippo_run"] = parallel_run
REGISTRY["maddpg_run"] = episode_run

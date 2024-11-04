from .parallel_run import run as parallel_run

REGISTRY = {}

REGISTRY["ippo_run"] = parallel_run

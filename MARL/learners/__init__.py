from .local_ppo_learner import LocalPPOLearner

REGISTRY = {}

REGISTRY["local_ppo_learner"] = LocalPPOLearner

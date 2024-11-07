from .local_ppo_learner import LocalPPOLearner
from .maddpg_learner import MADDPGLearner
REGISTRY = {}

REGISTRY["local_ppo_learner"] = LocalPPOLearner
REGISTRY["maddpg_learner"] = MADDPGLearner

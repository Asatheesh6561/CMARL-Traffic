from gym_cityflow.envs.cityflow_env import Cityflow
import gym
import sys
import os
import random
import numpy as np

env = Cityflow(configPath="sample_data/sample_config.json", episodeSteps=3600)
env.reset()

# disable print temporarily
# iterate environment a lttle bit to test env
actionInterval = 10


for i in range(1000):
    if i % actionInterval == 0:
        testAction = []
        for i in range(0, 16):
            n = random.randint(0, 8)
            testAction.append(n)
    observation, reward, done, _, debug = env.step(action=testAction)
    if any([i[1] > 0 for i in reward]):
        print(reward)
    if done:
        assert False

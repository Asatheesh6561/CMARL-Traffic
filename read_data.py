import pickle as pkl
import matplotlib.pyplot as plt
import os
import numpy as np
import seaborn as sns

results_folder = "/cmlscratch/anirudhs/ctraffic/results"
results_prefix = "maddpg_JN_GreenSkip"

results_files = [f for f in os.listdir(results_folder) if f.startswith(results_prefix)]
assert len(results_files) > 0, "No files found with prefix " + results_prefix

results_list = []
for f in results_files:
    with open(results_folder + "/" + f, "rb") as file:
        results_list.append(pkl.load(file))


def plot_runs(results_list, key):
    sns.set_style("whitegrid", {"axes.grid": True, "axes.edgecolor": "black"})

    fig = plt.figure()
    plt.clf()
    ax = fig.gca()

    timesteps = [d["Time Step"] for d in results_list[0] if key in d]
    rewards = np.array([[d[key] for d in r if key in d] for r in results_list])
    avg_reward = np.mean(rewards, axis=0)

    smooth_window = 20
    ones_smooth = np.ones(smooth_window)

    smoothed_rewards = []
    for r in rewards:
        smoothed_r = np.convolve(r, ones_smooth, "same") / np.convolve(
            np.ones(len(r)), ones_smooth, "same"
        )
        smoothed_rewards.append(smoothed_r)

    smoothed_rewards = np.array(smoothed_rewards)
    avg_reward = np.mean(smoothed_rewards, axis=0)
    min_reward = np.min(smoothed_rewards, axis=0)
    max_reward = np.max(smoothed_rewards, axis=0)

    plt.plot(timesteps, avg_reward, color="black", label="Average")
    plt.fill_between(
        timesteps, min_reward, max_reward, alpha=0.2, color="black", label="Min/Max"
    )

    plt.xlabel("Episode")
    plt.ylabel(key)
    plt.title(key)
    plt.legend()
    plt.savefig("test.png")


plot_runs(results_list, "Test Reward")

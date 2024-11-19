import pickle as pkl
import matplotlib.pyplot as plt
import os
import numpy as np
import seaborn as sns

constraint = "None"
env = "NY"
results_folder = "/cmlscratch/anirudhs/ctraffic/results"
results_prefixes = [
    f"ippo_{env}_{constraint}",
    f"mappo_{env}_{constraint}",
    f"mappo2c_{env}_{constraint}",
    f"qtran_{env}_{constraint}",
]


def plot_all_runs(prefix_list, key):
    colors = ["black", "red", "blue", "green", "orange", "purple"]
    plt.figure()  # Create a single figure for all plots
    sns.set_style("whitegrid")  # Set Seaborn style once for all subplots

    for i, prefix in enumerate(prefix_list):
        results_files = [f for f in os.listdir(results_folder) if f.startswith(prefix)]
        assert len(results_files) > 0, "No files found with prefix " + prefix

        results_list = []
        for f in results_files:
            with open(results_folder + "/" + f, "rb") as file:
                results_list.append(pkl.load(file))

        # Filter to the longest runs
        max_length = max(
            len([i[key] for i in result if key in i]) for result in results_list
        )
        longest_results_list = [
            result
            for result in results_list
            if len([i[key] for i in result if key in i]) == max_length
        ]
        mean_rewards = np.array(
            [[d[key] for d in r if key in d] for r in longest_results_list]
        ).mean(axis=1)
        sorted_indices = np.argsort(mean_rewards)
        sorted_results_list = [longest_results_list[i] for i in sorted_indices]
        results_list = sorted_results_list[: min(3, len(sorted_results_list))]

        # Prepare data for plotting
        timesteps = [d["Time Step"] for d in results_list[0] if key in d]
        rewards = np.array([[d[key] for d in r if key in d] for r in results_list])

        # Smoothing
        smooth_window = 20
        ones_smooth = np.ones(smooth_window)
        smoothed_rewards = []
        for r in rewards:
            smoothed_r = np.convolve(r, ones_smooth, "same") / np.convolve(
                np.ones(len(r)), ones_smooth, "same"
            )
            smoothed_rewards.append(smoothed_r)
        smoothed_rewards = np.array(smoothed_rewards)

        # Calculate averages and bounds
        avg_reward = np.mean(smoothed_rewards, axis=0)
        min_reward = np.min(smoothed_rewards, axis=0)
        max_reward = np.max(smoothed_rewards, axis=0)

        # Plot the average reward and shaded region for min-max
        plt.plot(timesteps, avg_reward, color=colors[i], label=f"{prefix}_average")
        plt.fill_between(timesteps, min_reward, max_reward, alpha=0.2, color=colors[i])

    plt.legend()
    plt.xlabel("Time Step")
    plt.ylabel(key)
    plt.title(f"Reward Comparison for {key}")
    plt.savefig(
        f"{key} {constraint} {env}.png"
    )  # Save the combined plot after the loop
    plt.show()  # Optionally show the plot if running interactively


plot_all_runs(results_prefixes, "Test Reward")
plot_all_runs(results_prefixes, "test_throughput")
plot_all_runs(results_prefixes, "test_average_delay")

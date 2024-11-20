import pickle as pkl
import matplotlib.pyplot as plt
import os
import numpy as np
import seaborn as sns

results_folder = "./results_copy/results_copy"
results_combined = {}
for f in os.listdir(results_folder):
    algo, env, constraint, *_ = f.split("_")
    if algo not in {'mappo', 'ippo', 'mappolce', 'qtran'}: continue
    if not env in results_combined: results_combined[env] = {}
    if not constraint in results_combined[env]: results_combined[env][constraint] = {}
    if not algo in results_combined[env][constraint]: results_combined[env][constraint][algo] = []
    with open(f"{results_folder}/{f}", "rb") as file:
            results_combined[env][constraint][algo].append(pkl.load(file))

constraint_to_idx = {'None': 0, 'GreenTime': 1, 'PhaseSkip': 2, 'GreenSkip': 3}
algo_to_idx = {'mappolce': 0, 'mappo': 1, 'qtran': 2, 'ippo': 3}

def plot_all_runs(results_combined, key, title_key):
    sns.set_style("whitegrid")
    fig, axs = plt.subplots(len(results_combined), len(results_combined['HZ']))
    fig.set_figwidth(25)
    fig.set_figheight(15)
    for j, env in enumerate(results_combined):
        for constraint in results_combined[env]:
            colors = ["black", "red", "blue", "green", "orange", "purple"]
            for algo in results_combined[env][constraint]:
                results_list = results_combined[env][constraint][algo] 
                # only include the longest runs
                results_list = [r for r in results_list if len(r) == len(max(results_list, key=len))]

                # Prepare data for plotting
                timesteps = [d["Time Step"]/100000 for d in results_list[0] if key in d]
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
                axs[j][constraint_to_idx[constraint]].plot(timesteps, avg_reward, color=colors[algo_to_idx[algo]], label=f"{algo}")
                axs[j][constraint_to_idx[constraint]].fill_between(timesteps, min_reward, max_reward, alpha=0.2, color=colors[algo_to_idx[algo]])

            #axs[j][constraint_to_idx[constraint]].legend()
            #axs[j][constraint_to_idx[constraint]].set_xlabel("Time Step (100,000s)")
            #axs[j][constraint_to_idx[constraint]].set_ylabel(title_key)
            axs[j][constraint_to_idx[constraint]].set_title(f"{constraint} constraint in {env}" if constraint != 'None' else
                                f"No constraint in {env}", fontsize=20)
    plt.suptitle(f"Averaged {title_key} vs. Time Step (100,000s)", fontsize=30)
    plt.tight_layout(pad=1)
    fig.subplots_adjust(top=0.90, bottom=0.075)
    handles, labels = axs[0][0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='lower center', prop={'size': 25}, ncols=4) 
    plt.savefig(
        f"./{title_key}.png"
    )  # Save the combined plot after the loop  

plot_all_runs(results_combined, "Test Reward", "Test Reward")
plot_all_runs(results_combined, "test_throughput", "Test Throughput")
plot_all_runs(results_combined, "test_average_delay", "Test Average Delay")

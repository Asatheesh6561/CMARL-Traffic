#!/bin/bash
#SBATCH --time=3-00:00:00
# Define the jobs and parameters
algorithms=("maddpg" "ippo" "mappo")
configs=("HZ" "NY" "JN")
constraints=("PhaseSkip" "GreenTime" "GreenSkip" "None")
i=202  # Initial job ID increment (adjust as needed)

# Array to store job IDs for tracking
declare -A job_ids

# Submit all jobs and save their job IDs
for algorithm in "${algorithms[@]}"; do
    for config in "${configs[@]}"; do
        for constraint in "${constraints[@]}"; do
            ((i++))
            job_name="${algorithm}_${config}_${constraint}"
            output_log="${algorithm}_${config}_${constraint}.log"
            
            # Submit the job and capture its job ID
            job_id=$(sbatch --job-name="$job_name" --output="$output_log" experiment_scavenger.sh "$algorithm" "$config" "$constraint" "$i" | awk '{print $4}')
            
            # Store job ID with its job name as the key
            job_ids["$job_name"]=$job_id
            echo "Submitted $job_name with job ID $job_id"
        done
    done
done

# Monitor the jobs and restart if stopped
while true; do
    for job_name in "${!job_ids[@]}"; do
        job_id="${job_ids[$job_name]}"
        
        # Check if the job is still running or pending
        if ! squeue --job "$job_id" > /dev/null 2>&1; then
            echo "Job $job_name (ID: $job_id) has stopped. Restarting..."
            
            # Extract the parameters from the job name
            algorithm="${job_name%%_*}"
            config="${job_name#*_}"; config="${config%%_*}"
            constraint="${job_name##*_}"
            
            # Increment job ID counter for the new submission
            ((i++))
            
            # Restart the job and capture the new job ID
            new_job_id=$(sbatch --job-name="$job_name" --output="${job_name}.log" experiment_scavenger.sh "$algorithm" "$config" "$constraint" "$i" | awk '{print $4}')
            
            # Update the job ID in the tracking array
            job_ids["$job_name"]=$new_job_id
            echo "Restarted $job_name with new job ID $new_job_id"
        else
            echo "Job $job_name (ID: $job_id) is still running."
        fi
    done
    
    # Wait before checking again
    sleep 60
done

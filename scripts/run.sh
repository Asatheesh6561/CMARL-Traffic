#!/bin/bash
#SBATCH --time=3-00:00:00
#SBATCH --qos=cml-scavenger
#SBATCH --partition=cml-scavenger
#SBATCH --account=cml-scavenger
# Define the jobs and parameters
algorithms=("qtran")
configs=("JN")
constraints=("PhaseSkip" "GreenTime" "GreenSkip" "None")
i=809  # Initial job ID increment (adjust as needed)


# Submit all jobs and save their job IDs
for algorithm in "${algorithms[@]}"; do
    for config in "${configs[@]}"; do
        for constraint in "${constraints[@]}"; do
            ((i++))
            job_name="${algorithm}_${config}_${constraint}"
            output_log="${algorithm}_${config}_${constraint}.out"
            
            # Submit the job and capture its job ID
            job_id=$(sbatch --job-name="$job_name" --output="$output_log" experiment_scavenger.sh "$algorithm" "$config" "$constraint" "$i" | awk '{print $4}')
            
            # Store job ID with its job name as the key
            job_ids["$job_name"]=$job_id
            echo "Submitted $job_name with job ID $job_id"
        done
    done
done

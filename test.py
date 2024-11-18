import os
import re

directory = "/cmlscratch/anirudhs/ctraffic/results"
for filename in os.listdir(directory):
    if re.search(r"_phase_skip_", filename):
        new_filename = filename.replace("_phase_skip_", "_PhaseSkip_")
        old_filepath = os.path.join(directory, filename)
        new_filepath = os.path.join(directory, new_filename)
        os.rename(old_filepath, new_filepath)

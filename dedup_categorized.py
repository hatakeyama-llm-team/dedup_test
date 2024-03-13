# %%
from concurrent.futures import ThreadPoolExecutor
import os
import glob

# integrate_web_datasetで処理されたカテゴリ化済みのjsonlをdedupする

input_dir = "data/categorized"
output_dir = "data/dedup_categorized"
max_workers = 30  # フォルダごとの並列処理数


def make_dir(target_dir):
    if not os.path.exists(target_dir):
        os.mkdir(target_dir)


make_dir(output_dir)

# make dirs
dir_list = glob.glob(f"{input_dir}/*")
job_list = [i.split("/")[-1] for i in dir_list]
for job_name in job_list:
    make_dir(f"{output_dir}/{job_name}")

# %%
# cmd=f"./dedup_sentence/deduplicate ./{input_dir}/{job_name}/ ./{output_dir}/{job_name}/"
# os.system(cmd)

# %%
#! ./dedup_sentence/deduplicate ./data/categorized/test/ ./data/dedup_categorized/test/

# %%


def run_command(job_name):
    cmd = f"./dedup_sentence/deduplicate ./{input_dir}/{job_name}/ ./{output_dir}/{job_name}/"
    os.system(cmd)


with ThreadPoolExecutor(max_workers=max_workers) as executor:
    executor.map(run_command, job_list)

# %%

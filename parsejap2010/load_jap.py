# %%
# jap2010を読み込んでparquetにするcode｡実行不要

"""
テキストアーカイブ - 日本語ウェブコーパス 2010
http://www.s-yata.jp/corpus/nwc2010/texts/
を処理するcode｡

#URLは常時は空いていないので注意｡
wget http://www.s-yata.jp/corpus/nwc2010/texts/filelist
wget -i filelist
"""

# %%
from datasets import load_dataset
import glob
import pandas as pd
import lzma
from Touten import touten_insert, del_kaigyo

# %%
import os

out_dir = "../data/jap2010_parquet"
if not os.path.exists(out_dir):
    os.mkdir(out_dir)

# %%


# %%
count_threshold = 3
max_lines = 2000


task_name = "00000001"
for xz_path in glob.glob("../data/jap2010/*.xz"):
    task_name = xz_path.split("/")[-1].split(".")[0]
    print(task_name)
    path = f"../data/jap2010/{task_name}.xz"
    # .xz ファイルを開いて内容をチャンクで読み込む
    with lzma.open(path, 'rt') as file:
        lines = file.readlines()

    new_line_count = 0

    current_doc = []
    cnt = 0
    text_len = 0
    text_list = []
    for line in (lines):
        if line == "\n":
            new_line_count += 1
        else:
            new_line_count = 0
        current_doc.append(line)
        if new_line_count >= count_threshold or len(current_doc) > max_lines:
            text = "\n".join(current_doc)
            text = text.strip()
            text = text.replace("\n\n", "\n")
            text = touten_insert(text)
            text = del_kaigyo(text)
            current_doc = []
            new_line_count = 0

            """
            if text!="":
                d=json.dumps({"text":text},ensure_ascii=False)
                with open(f"{out_dir}/{task_name}.jsonl","a") as f:
                    f.write(f"{d}\n")
            """
            if text != "":
                # print(len(text))
                text_list.append(text)
                text_len += len(text)

        if text_len > 10**8:
            # if len(text_list)>10:
            #    break

            df = pd.DataFrame(text_list, columns=["text"])  # .reset_index()
            df.to_parquet(f"{out_dir}/{task_name}_{cnt}.parquet")
            cnt += 1
            text_list = []
            text_len = 0
            # if cnt>100:
            #    break
    # break
    df = pd.DataFrame(text_list, columns=["text"]).reset_index()
    df.to_parquet(f"{out_dir}/{task_name}_{cnt}.parquet")

# %%
text = text_list[1]
text = touten_insert(text)
text = del_kaigyo(text)
print(text)

# %%
text = del_kaigyo(text)
print(text)


# %%
t = "たくさんの「わたし」に見てもらいたいから、ダムの映画祭を、谷根千で、"
# end_filter(t)

# %%
df = pd.read_parquet("data/jap2010_parquet/00000001_0.parquet")
df

# %%
# huggingface-cli upload --repo-type=dataset hatakeyama-llm-team/japanese2010 .

# %%
# load test
dataset = load_dataset("hatakeyama-llm-team/japanese2010",
                       streaming=True,
                       split="train",
                       )

# %%
cnt = 0
for data in dataset:
    print(data["text"][:10])
    cnt += 1
    if cnt > 10:
        break

# %%


# %%
with open("t.txt", "w") as f:
    f.write(data["text"])

# %%

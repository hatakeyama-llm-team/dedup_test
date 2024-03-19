# [Dedup](./simple_dedup_test.ipynb)
## テキストを高速にdedupするコードの例です
- [参考](https://github.com/if001/dedup_sentence)
- [解説](https://zenn.dev/if001/articles/cc262413e69e3d)

- Install
~~~
sudo apt install nlohmann-json3-dev -y

git clone https://github.com/if001/dedup_sentence
cd dedup_sentence
git clone https://github.com/aappleby/smhasher.git
wget https://raw.githubusercontent.com/simdjson/simdjson/master/singleheader/simdjson.h 
wget https://raw.githubusercontent.com/simdjson/simdjson/master/singleheader/simdjson.cpp 
make
~~~

- [Test code](./simple_dedup_test.ipynb)


# [Japanese2010](./parsejap2010/)
- [こちら](https://www.s-yata.jp/corpus/nwc2010/)のコーパスを処理するscriptです
- 「｡」がついてないので､ルールベースでつけていきます｡
  - はじめに､上記webサイトからxzファイルをダウンロードする｡
  - python load_jap.py を実行
    - xzファイルを読み込み
    - テキストを処理
    - parquetファイルとして書き出し


# [WebIntegrator](./integrate_web_dataset.py)
## Web上のCommonCrawl系のtextをjsonlでカテゴライズしながら書き出します
## ボツコードです｡ (BERTOPICが遅い)
- デフォルトでは､Streamingでdownloadする仕様になっています｡
- ついでに､BERTopicでclassifyもしておきます
    - [こちらのnotebookでモデルはtrainしておきます](./train_topic_model.ipynb)
        - 学習済みモデルは[huggingface]()または[box drive](https://app.box.com/s/emuntfvoapmbw00cey9699p3mfw6arf9)
- 実行法
~~~
python integrate_web_dataset.py (データセット名)
~~~

- データセット名: 
    - mc4
    - oscar
    - cc100
    - shisa

- [categorized](./data/categorized/)フォルダの中に､jsonlが生成されていきます
- 独立プロセスで回せます｡
~~~

python integrate_web_dataset.py mc4
python integrate_web_dataset.py oscar
python integrate_web_dataset.py cc100
python integrate_web_dataset.py shisa
~~~

- データがたまったら､[dedup](./dedup_categorized.py)をします
~~~
python dedup_categorized.py
~~~


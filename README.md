# Dedup
# テキストを高速にdedupするコードの例です
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
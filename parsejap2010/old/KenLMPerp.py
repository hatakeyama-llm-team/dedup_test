import kenlm
import sentencepiece
import unicodedata


class PerplexityChecker:
    def __init__(self, arpa_path, sp_path):
        self.ken_model = kenlm.LanguageModel(arpa_path)
        self.sp = sentencepiece.SentencePieceProcessor()
        self.sp.load(sp_path)

    def __call__(self, inp):
        text = unicodedata.normalize('NFD', inp)
        toks = self.sp.encode(text, out_type=str)
        sentence = " ".join(toks)
        ppl = self.ken_model.perplexity(sentence)
        return ppl


"""
install
python -m pip install sentencepiece "protobuf<3.20.*"
sudo apt install build-essential cmake libboost-system-dev libboost-thread-dev libboost-program-options-dev libboost-test-dev libeigen3-dev zlib1g-dev libbz2-dev liblzma-dev

pip install https://github.com/kpu/kenlm/archive/master.zip
#gccがあたらしいとうまくいかない？？

mkdir -p data/lm_sp
wget -c  -P data/lm_sp http://dl.fbaipublicfiles.com/cc_net/lm/ja.arpa.bin
wget -c  -P data/lm_sp http://dl.fbaipublicfiles.com/cc_net/lm/ja.sp.model
"""
"""
sp_path = "../data/lm_sp/ja.sp.model"
arpa_path = "../data/lm_sp/ja.arpa.bin"
from src.cleaner.perplexity_checker import PerplexityChecker
perp_checker = PerplexityChecker(arpa_path,sp_path)
"""

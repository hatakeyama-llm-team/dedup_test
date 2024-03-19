
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from tqdm import tqdm
from KenLMPerp import PerplexityChecker


class Cleaner:
    def __init__(self, mode="kenlm") -> None:
        self.mode = mode
        if mode == "kenlm":
            print("kenlm mode")
            arpa_path = "data/lm_sp/ja.arpa.bin"
            sp_path = "data/lm_sp/ja.sp.model"
            self.kenlm = PerplexityChecker(arpa_path, sp_path)
        else:
            print("llm mode")
            self.tokenizer = AutoTokenizer.from_pretrained(
                "llm-jp/llm-jp-1.3b-v1.0")
            self.model = AutoModelForCausalLM.from_pretrained(
                "llm-jp/llm-jp-1.3b-v1.0",
                device_map="auto",
                # torch_dtype=torch.float32
            )

    def __call__(self, text):
        return self.integrate(text, self.model, self.tokenizer)

    def llm_perplexity(self, text) -> torch.Tensor:
        tokenized_input = self.tokenizer.encode(
            text, add_special_tokens=False, return_tensors="pt"
        ).to(self.model.device)
        with torch.inference_mode():
            output = self.model(tokenized_input, labels=tokenized_input)
        ppl = torch.exp(output.loss)
        return ppl.item()

    def kenlm_perplexity(self, text):
        return self.kenlm(text)

    def perplexity(self, text):
        if self.mode == "kenlm":
            return self.kenlm_perplexity(text)
        else:
            return self.llm_perplexity(text)

    def integrate(self, text,
                  check_length=4
                  ):
        lines = text.split("\n")
        new_lines = []
        current_line = ""

        for raw_line in (lines):
            # raw_line=raw_line.strip()
            if len(raw_line) == 0:
                continue
            case_next_line = current_line[-check_length:] + \
                "\n"+raw_line[:check_length]
            case_touten_line = current_line[-check_length:] + \
                "。"+raw_line[:check_length]
            case_space_line = current_line[-check_length:] + \
                " "+raw_line[:check_length]

            perp_next_case = (self.perplexity(case_next_line))
            perp_touten_case = (self.perplexity(case_touten_line))
            perp_space_case = (self.perplexity(case_space_line))

            if perp_next_case < perp_touten_case or perp_space_case < perp_touten_case:
                # if perp_next_case<perp_touten_case and perp_next_case<perp_touten_case:
                # if current_line=="":
                #    continue
                new_lines.append(current_line)
                current_line = raw_line
            else:
                # if perp_touten_case<perp_space_case:
                #    current_line=current_line[:]+"。"+raw_line[:]
                # else:
                #    current_line=current_line[:]+"\n"+raw_line[:]
                # current_line=case_touten_line
                current_line = current_line[:]+"。"+raw_line[:]

        case_original_line = current_line[-check_length:]
        case_touten_line = current_line[-check_length:]+"。"
        if self.perplexity(case_original_line) < self.perplexity(case_touten_line):
            new_lines.append(current_line)
        else:
            new_lines.append(current_line+"。")

        cleaned_lines = []
        for line in new_lines:
            if len(line) < 1:
                continue
            if line[0] == "。":
                line = line[1:]
            cleaned_lines.append(line)
        return "\n".join(cleaned_lines)

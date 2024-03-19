
import MeCab
# 形態素解析器の初期化
mecab = MeCab.Tagger()


def check_end_type(line):
    parsed = mecab.parse(line)
    # print(parsed)
    parts = parsed.split("\n")
    final_part = parts[-3]
    temp = final_part.split("\t")
    end_type = temp[-2]
    hinshi = temp[4]
    return end_type, hinshi


def touten_insert(text):
    new_lines = []
    old_line = ""
    current_line = ""
    non_kaiyo = False

    for line in text.split("\n"):
        if line == "":
            continue
        if line == old_line:
            continue
        old_line = line

        if non_kaiyo:
            current_line += line
            # print("non_kaiyo added", line)
            non_kaiyo = False
            continue

        end_type, hinshi = check_end_type(line)
        if end_type.find("終止形") >= 0 or end_type.find("命令") >= 0:
            current_line += line+"。"
        elif hinshi.find("名詞") >= 0 or hinshi.find("記号"):
            new_lines.append(current_line)
            current_line = ""
            new_lines.append(line)
        else:
            current_line += line
    new_lines.append(current_line)
    new_lines = [i for i in new_lines if i != ""]

    return "\n".join(new_lines)


def end_filter(line):
    end_symbols = [
        "、", "（", "("
    ]
    for symb in end_symbols:
        if line.endswith(symb):
            return True
    return False


def del_kaigyo(text):
    new_lines = []
    temp_line = ""
    for line in text.split("\n"):
        # print(line)
        if end_filter(line) or end_filter(temp_line):
            # print("integ:", temp_line, "----", line)
            temp_line += line

        else:
            if temp_line != "":
                new_lines.append(temp_line)
            new_lines.append(line)
            temp_line = ""

        # if line.startswith("を") or line.startswith("は"):
        #    current_line += line
    return "\n".join(new_lines)

import re

gender_pattern = re.compile(r"\w:\w")

def evaluate(gold_file: str, test_file: str):
    lines = 0
    false_negative = 0
    false_positive = 0
    true_negative = 0
    true_positive = 0
    total_words = 0
    total_lines = 0
    with open(gold_file, "r", encoding="utf8") as gold, open(test_file, "r", encoding="utf8") as test:
        for gline, tline in zip(gold, test):
            total_lines += 1
            if gline.replace(" ", "") == tline.replace(" ", ""):
                lines += 1
            gline = gline.split(" ")
            tline = tline.split(" ")
            for gword, tword in zip(gline, tline):
                total_words += 1
                if gword == tword:
                    if gender_pattern.search(gword):
                        true_positive += 1
                    else:
                        true_negative += 1
                else:
                    if gender_pattern.search(tword):
                        false_positive += 1
                    else:
                        false_negative += 1
    print(f"""
        correct_lines: {lines/total_lines}
        total_lines: {total_lines}
        ---------------------------
        true_pos: {true_positive}
        true_neg: {true_negative}
        false_pos: {false_positive}
        false_neg: {false_negative}
        total_words: {total_words}
        """)
import re
from pathlib import Path
import os

import spacy

from corpus_statistics import DIR

gender_pattern = re.compile(r"\w:\w")


def evaluate(gold_file: str, test_file: str):
    lines = 0
    different_lines = 0
    false_negative = 0
    false_positive = 0
    true_negative = 0
    true_positive = 0
    total_words = 0
    total_lines = 0
    total_positive = 0
    total_negative = 0
    wrong_ending = 0
    with open(gold_file, "r", encoding="utf8") as goldd, open(test_file, "r", encoding="utf8") as testt:
        for gline, tline in zip(goldd, testt):
            total_lines += 1
            if gline.replace(" ", "") == tline.replace(" ", ""):
                lines += 1
            gline = gline.strip("\n")
            tline = tline.strip("\n")
            gline = gline.split(" ")
            tline = tline.split(" ")
            if gline[-1] == "":
                gline = gline[:-1]
            if tline[-1] == "":
                tline = tline[:-1]
            if not len(gline) == len(tline):
                different_lines += 0
                print(gline)
                print(tline)
            for gword, tword in zip(gline, tline):
                total_words += 1
                # is gold word gender inclusive?
                if gender_pattern.search(gword):
                    total_positive += 1
                else:
                    total_negative += 1

                if gword == tword:
                    if gender_pattern.search(gword):
                        true_positive += 1
                    else:
                        true_negative += 1
                elif gender_pattern.search(gword) and gender_pattern.search(tword):
                        wrong_ending += 1
                else:
                    if gender_pattern.search(tword):
                        #print(gline)
                        #print(f"gold:-{gword}-test:{tword}-")
                        false_positive += 1
                    else:
                        false_negative += 1
    return \
        f"""
        correct_lines: {lines}
        total_lines: {total_lines}
        ---------------------------
        true_pos: {true_positive}
        true_neg: {true_negative}
        false_pos: {false_positive}
        false_neg: {false_negative}
        wrong_ending: {wrong_ending}
        _____________________________
        total_positive: {total_positive} vs. tp + fn + wrong_ending = {true_positive + false_negative + wrong_ending}
        total_negative: {total_negative}
        total_words: {total_words}
        
        """

def clean_annotated_file(infile: Path, outfile: Path):
    with open(infile, "r", encoding="utf8") as inn, open(outfile, "w", encoding="utf8") as out:
        for line in inn:
            line = line.split()
            line = " ".join(line[2:])
            out.write(line + "\n")


def compare_files(gold_file: Path, trial_file: Path):
    differences = []
    with open(gold_file, "r", encoding="utf8") as gold, open(trial_file, "r", encoding="utf8") as trial, open((DIR / "differences.txt"), "w", encoding="utf8") as out:
        for gold_line, trial_line in zip(gold, trial):
            if not gold_line.replace(" ", "") == trial_line.replace(" ", ""):
                differences.append(trial_line)
        for d in differences:
            out.write(d)
    return


def tokenize(infile: str, outfile: str, spacy_model: str = "de_core_news_lg"):
    nlp = spacy.load(spacy_model)
    with open(infile, "r", encoding="utf8") as inn, open(outfile, "w", encoding="utf8") as out:
        for line in inn:
            doc = nlp(line)
            out.write(" ".join(t.text for t in doc))


if __name__ == "__main__":
    gold_file = str(DIR / "results" / "test_set_annotated_tokenized.de")
    test_files = [
        (DIR / "results" / "rule_old_annotated.de"),
        (DIR / "results" / "test_translated_old.de"),
        (DIR / "results" / "rule_new_annotated.de"),
    ]
    output = (DIR / "results" / "results_de.txt")
    with open(output, "w", encoding="utf8") as out:
        for file in test_files:
            # File name
            out.write(file.name)
            # stream = os.popen(f"sacrebleu {str(gold_file)} -tok none -i {str(file)}")
            # out.write(stream.read())
            out.write(
                evaluate(
                gold_file=str(gold_file),
                test_file=str(file),
                )
            )


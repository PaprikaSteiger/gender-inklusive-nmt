import re
from pathlib import Path

import spacy

from corpus_statistics import DIR

gender_pattern = re.compile(r"\w:\w")

def evaluate(gold_file: str, test_file: str):
    lines = 0
    false_negative = 0
    false_positive = 0
    true_negative = 0
    true_positive = 0
    total_words = 0
    total_lines = 0
    total_positive = 0
    total_negative = 0
    with open(gold_file, "r", encoding="utf8") as gold, open(test_file, "r", encoding="utf8") as test:
        #assert len(gold.readlines()) == len(test.readlines())
        for gline, tline in zip(gold, test):
            total_lines += 1
            if gline.replace(" ", "") == tline.replace(" ", ""):
                lines += 1
            gline = gline.split(" ")
            tline = tline.split(" ")
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
        _____________________________
        total_positive: {total_positive}
        total_negative: {total_negative}
        total_words: {total_words}
        """)

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
    evaluate(
        gold_file=r"C:\Users\steig\Desktop\Neuer Ordner\gender-inklusive-nmt\data\test_set_de_annotated.tokenized",
        test_file=r"C:\Users\steig\Desktop\Neuer Ordner\data\test_translated_old.txt"
    )
    # with open(
    #         r"C:\Users\steig\Desktop\Neuer Ordner\gender-inklusive-nmt\data\test_set_de_annotated.tokenized",
    #         "r",
    #         encoding="utf8",) as ann, open(
    #     r"C:\Users\steig\Desktop\Neuer Ordner\gender-inklusive-nmt\data\test_set_de_annotated_dummy.txt",
    #     "r",
    #     encoding="utf8",
    # ) as out:
    #     for line1, line2 in zip(ann, out):
    #         if not len(line1.split(" ")) == len(line2.split(" ")):
    #             breakpoint()
        # for line in ann:
        #     line = line.split(" ")
        #     for c, word in enumerate(line):
        #         if gender_pattern.search(word):
        #             line[c] = word.replace("à", ":")
        #     out.write(" ".join(line))
    # tokenize(
    #     infile=r"C:\Users\steig\Desktop\Neuer Ordner\gender-inklusive-nmt\data\test_set_de_annotated_dummy.txt",
    #     outfile=r"C:\Users\steig\Desktop\Neuer Ordner\gender-inklusive-nmt\data\test_set_de_annotated.tokenized"
    # )


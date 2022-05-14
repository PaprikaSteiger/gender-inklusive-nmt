import os
from pathlib import Path
import numpy as np
import typing as t
from collections import Counter
import re
from math import floor

from spacy import Language
import matplotlib.pyplot as plt
import spacy

gender_pattern = re.compile(r"\w:\w")

DIR: Path = (Path(__file__).parent / "data").mkdir(exist_ok=True) or Path(
    __file__
).parent / "data"
CORPUS_NOISE = [
    r"http://",
]


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
    with open(gold_file, "r", encoding="utf8") as goldd, open(
        test_file, "r", encoding="utf8"
    ) as testt:
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
                # print(gline)
                # print(tline)
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
                        # print(gline)
                        # print(f"gold:-{gword}-test:{tword}-")
                        false_positive += 1
                    else:
                        false_negative += 1
    return f"""
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
        ________
        lines %: {lines/total_lines * 100}
        recall: {(true_positive+wrong_ending)/total_positive}
        wrong-endings: {wrong_ending/(true_positive+wrong_ending)}
        fall-out %: {false_positive/total_negative * 100}
        selectivity: {true_negative/total_negative}
        miss-rate: {false_negative/total_positive} 
        precision: {true_positive/(true_positive+false_positive)},
        negative prediction value: {true_negative/(true_negative+false_negative)*100}
        """


def clean_annotated_file(infile: Path, outfile: Path):
    with open(infile, "r", encoding="utf8") as inn, open(
        outfile, "w", encoding="utf8"
    ) as out:
        for line in inn:
            line = line.split()
            line = " ".join(line[2:])
            out.write(line + "\n")


def compare_files(gold_file: Path, trial_file: Path):
    differences = []
    with open(gold_file, "r", encoding="utf8") as gold, open(
        trial_file, "r", encoding="utf8"
    ) as trial, open((DIR / "differences_translated.txt"), "w", encoding="utf8") as out:
        for gold_line, trial_line in zip(gold, trial):
            if not gold_line.replace(" ", "").replace("\n", "") == trial_line.replace(
                " ", ""
            ).replace("\n", ""):
                differences.append(trial_line)
        for d in differences:
            out.write(d)
    return


def tokenize(infile: str, outfile: str, spacy_model: str = "de_core_news_lg"):
    nlp = spacy.load(spacy_model)
    with open(infile, "r", encoding="utf8") as inn, open(
        outfile, "w", encoding="utf8"
    ) as out:
        for line in inn:
            doc = nlp(line)
            out.write(" ".join(t.text for t in doc))


def create_validation_set(
    train_data1: str,
    train_data2: str,
    train_out1: str,
    train_out2: str,
    val_out1: str,
    val_out2: str,
):
    split = 0.1
    lines = open(train_data1, "r", encoding="utf8").readlines()
    lines2 = open(train_data2, "r", encoding="utf8").readlines()
    length = len(lines)
    # generate n random integers in range (0, length)
    n = floor(length * split)
    indices = np.random.randint(0, length, n)
    indices_set = set(indices)
    while not len(indices_set) == len(indices):
        new_int = np.random.randint(0, length)
        if new_int not in indices_set:
            indices_set.add(new_int)
    with open(train_out1, "w", encoding="utf8") as train1, open(
        train_out2, "w", encoding="utf8"
    ) as train2:
        for i, line in enumerate(lines, start=0):
            if i in indices_set:
                continue
            else:
                train1.write(line)
                train2.write(lines2[i])
    with open(val_out1, "w", encoding="utf8") as val1, open(
        val_out2, "w", encoding="utf8"
    ) as val2:
        for i in indices_set:
            val1.write(lines[i])
            val2.write(lines2[i])


def select_sentences(n: int, file: str):
    clean_lines = []
    with open(file, "r", encoding="utf8") as inn:
        for line in inn:
            # don't add sentences with noise to test set
            if any(line.startswith(ele) or ele in line for ele in CORPUS_NOISE):
                continue
            # block sentences with less than or two tokens
            if len(line.split(" ")) <= 2:
                continue
            clean_lines.append(line)
    length = len(clean_lines)
    # generate n random intengers in range (0, length)
    # TODO: assert no integer appears twice
    # TODO: or replace dupplicated sentences afterwards
    indices = np.random.randint(0, length, n)
    indices_set = set(indices)
    while not len(indices_set) == len(indices):
        breakpoint()
        new_int = np.random.randint(0, length)
        if new_int not in indices_set:
            indices_set.add(new_int)

    for i in indices_set:
        yield clean_lines[i]


def create_test_set(sources: t.List[t.Tuple[str, int]], out_file: str):
    with open(out_file, "w", encoding="utf8") as out:
        for file, number in sources:
            for line in select_sentences(file=file, n=number):
                out.write(line)


def spacy_statistics_of_test_set(test_set: str, spacy_model: Language):
    pos = Counter()
    morph = Counter()
    length = Counter()
    gendered = Counter()
    with open(test_set, "r", encoding="utf8") as inn:
        for line in inn:
            if re.search(r".*\w+:\w+.*", line):
                gendered["Inclusive"] += 1
            else:
                gendered["Bias"] += 1
            doc = spacy_model(line)
            length[len(doc)] += 1
            for t in doc:
                pos[str(t.pos_)] += 1
                if "Person" in str(t.morph) and "Pron" in str(t.morph):
                    match = re.match(
                        r".+\|(Person.+?\|Pron.+?)(:?\|.+|$)", str(t.morph)
                    ).group(1)
                    morph[match] += 1
                else:
                    morph["NoPron"] += 1

    plt.bar(x=length.keys(), height=length.values())
    plt.xticks(ticks=range(len(length.keys())), labels=length.keys(), rotation=90)
    plt.show()

    plt.bar(x=pos.keys(), height=pos.values())
    plt.xticks(ticks=range(len(pos.keys())), labels=pos.keys(), rotation=90)
    plt.show()

    plt.bar(x=gendered.keys(), height=gendered.values())
    plt.xticks(ticks=range(len(gendered.keys())), labels=gendered.keys(), rotation=90)
    plt.show()

    plt.bar(x=morph.keys(), height=morph.values())
    plt.xticks(ticks=range(len(morph.keys())), labels=morph.keys(), rotation=45)
    plt.show()

    return pos, morph, length


def create_train(source_files: t.List[str], test_data: str, out_file: str):
    count = 0
    test_lines = open(test_data, "r", encoding="utf8").readlines()
    with open(out_file, "w", encoding="utf8") as outt:
        for file in source_files:
            with open(file, "r", encoding="utf8") as inn:
                for line in inn:

                    # don't add sentences with noise to test set
                    if any(line.startswith(ele) or ele in line for ele in CORPUS_NOISE):
                        continue
                    # block sentences with less than or two tokens
                    if len(line.split(" ")) <= 2:
                        continue
                    if line in test_lines:
                        continue
                    outt.write(line)
                    count += 1
    print(count)


if __name__ == "__main__":
    gold_file = str(DIR / "results" / "test_set_annotated_tokenized.de")
    test_files = [
        (DIR / "results" / "rule_old_annotated.de"),
        (DIR / "results" / "test_translated_old.de"),
        (DIR / "results" / "rule_new_annotated.de"),
        (DIR / "german_annotated_inclusiv_spacy_test3.txt"),
    ]
    output = DIR / "results" / "results_de2.txt"
    with open(output, "w", encoding="utf8") as out:
        for file in test_files:
            # File name
            out.write(file.name)
            out.write("\n")
            stream = os.popen(f"sacrebleu {str(gold_file)} -tok none -i {str(file)}")
            out.write("\n")
            out.write(stream.read())
            out.write(
                evaluate(
                    gold_file=str(gold_file),
                    test_file=str(file),
                )
            )
    compare_files(
        gold_file=str(DIR / "results" / "test_set_annotated_tokenized.de"),
        trial_file=str(DIR / "results" / "test_translated_old.de"),
    )

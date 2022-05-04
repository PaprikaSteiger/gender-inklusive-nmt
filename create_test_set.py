from pathlib import Path
import numpy as np
import typing as t
from collections import Counter
import re
from math import floor

from spacy import Language
import spacy
import matplotlib.pyplot as plt

from preprocess_corpus import CORPUS_NOISE, DIR


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
                    match = re.match(r".+\|(Person.+?\|Pron.+?)(:?\|.+|$)", str(t.morph)).group(1)
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


def create_train(
        source_files: t.List[str],
        test_data: str,
        out_file: str
):
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

def create_validation_set(
        train_data: str,
        train_out: str,
        val_out: str,
        validation_split: t.Optional[float]=None,
        validation_number: t.Optional[int]=None,
):
    lines = open(train_data, "r", encoding="utf8").readlines()
    length = len(lines)
    # generate n random intengers in range (0, length)
    if validation_split:
        n = floor(length * validation_split)
    elif validation_number:
        n = validation_number
    else:
        assert False, "Chose validation_split or validation_number"
    indices = np.random.randint(0, length, n)
    indices_set = set(indices)
    while not len(indices_set) == len(indices):
        new_int = np.random.randint(0, length)
        if new_int not in indices_set:
            indices_set.add(new_int)
    with open(val_out, "w", encoding="utf8") as val:
        for i in indices_set:
            val.write(lines[i])
    with open(train_out, "w", encoding="utf8") as train:
        for i, line in enumerate(lines, start=0):
            if i in indices_set:
                continue
            else:
                train.write(line)

if __name__ == "__main__":
    # create_test_set(
    #     sources=[
    #         (r"C:\Users\steig\Desktop\data\ted_13_de.txt", 400),  # ted 13
    #         (r"C:\Users\steig\Desktop\data\ted_20_de.txt", 350), # ted 20
    #         (r"C:\Users\steig\Desktop\Neuer Ordner\data\europarl_de.txt", 200) #europarl
    #     ],
    #     out_file=str(DIR / "test_set_de.txt")
    # )
    # spacy_statistics_of_test_set(
    #     test_set=str(DIR / "test_set_de.txt"),
    #     spacy_model=spacy.load("de_core_news_lg")
    # )
    # files =
    create_train(
        source_files=[
        r"C:\Users\steig\Desktop\Neuer Ordner\data\ted_13_de.txt",
        r"C:\Users\steig\Desktop\Neuer Ordner\data\ted_20_de.txt",
        r"C:\Users\steig\Desktop\Neuer Ordner\data\europarl_de.txt",
    ],
    test_data=str(DIR / "test_set_de.txt"),
    out_file=r"C:\Users\steig\Desktop\Neuer Ordner\data\train_data_de.txt",
    )
    # create_validation_set(
    #     train_data=r"C:\Users\steig\Desktop\Neuer Ordner\data\train_data_annotated_de.txt",
    #     train_out=str(DIR / "train_text.de"),
    #     val_out=str(DIR / "val_text.de"),
    #     validation_number=3000,
    # )


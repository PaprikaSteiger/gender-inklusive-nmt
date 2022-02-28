from pathlib import Path
import numpy as np
import typing as t
from collections import Counter
import re

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
    indices = np.random.randint(0, length, n)
    for i in indices:
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
                print(str(t.morph))
                breakpoint()
                morph[str(t.morph)] += 1

    plt.bar(x=length.keys(), height=length.values())
    plt.xticks( labels=length.keys(), rotation=90)
    plt.show()

    plt.bar(x=pos.keys(), height=pos.values())
    plt.xticks(ticks=range(len(pos.keys())), labels=pos.keys(), rotation=90)
    plt.show()

    plt.bar(x=gendered.keys(), height=gendered.values())
    plt.xticks(ticks=range(len(gendered.keys())), labels=gendered.keys(), rotation=90)
    plt.show()

    # split morph into two plots

    plt.bar(x=morph.keys(), height=morph.values())
    plt.xticks(ticks=range(len(morph.keys())), labels=morph.keys(), rotation=90)
    plt.show()

    return pos, morph, length


if __name__ == "__main__":
    # create_test_set(
    #     sources=[
    #         (r"C:\Users\steig\Desktop\data\ted_13_de.txt", 400),  # ted 13
    #         (r"C:\Users\steig\Desktop\data\ted_20_de.txt", 350), # ted 20
    #         # europarl
    #     ],
    #     out_file=str(DIR / "test_set_de.txt")
    # )
    spacy_statistics_of_test_set(
        test_set=str(DIR / "test_set_de_backup.txt"),
        spacy_model=spacy.load("de_core_news_lg")
    )
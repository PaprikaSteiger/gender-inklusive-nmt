from collections import Counter
from pathlib import Path
import pandas as pd
import numpy as np
import seaborn as sn
import matplotlib.pyplot as plt
import csv

from load_corpus import DIR

TOKENIZED_de = DIR / "tokenized_normalized_truecased.de"
tokenized_fr = DIR / "tokenized_normalized_truecased.fr"


def count_words(in_file: Path):
    c = Counter()
    with open(in_file, "r", encoding="utf8") as inn:
        for line in inn:
            line = line.split(" ")
            c.update(line)
    return c


def histogram_of_frequencies(data: list):
    array = np.array(data)
    bins = len(set(array))
    sn.histplot(array, stat="count", bins=bins, )
    plt.show()


if __name__ == "__main__":
    # counter_de = count_words(in_file=(DIR / "tokenized_normalized_truecased.de"))
    # counter_fr = count_words(in_file=(DIR / "tokenized_normalized_truecased.fr"))
    # histogram_of_frequencies(data=list(counter.values()))
    # # write counts to file
    # with (DIR / "word_count.csv").open("w", encoding="utf8", newline="") as out:
    #     dict_writer = csv.writer(out)
    #     for k, v in counter_de.items():
    #         dict_writer.writerow([k, v])
    # # show n least frequent words
    # n = 100
    # for ele in counter.most_common()[:n-1:-1]:
    #     print(ele)

    # distinguish french word count
    ted13 = r"C:\Users\steig\Desktop\Neuer Ordner\data\ted_13_de.txt"
    ted20 = r"C:\Users\steig\Desktop\Neuer Ordner\data\ted_20_de.txt"
    euro = r"C:\Users\steig\Desktop\Neuer Ordner\data\europarl_de.txt"
    train = r"C:\Users\steig\Desktop\Neuer Ordner\data\train_data_de.txt"

    files = [ted20, ted13, euro, train]
    for file in files:
        c = 0
        with open(file, "r", encoding="utf8") as f:
            for line in f:
                c += 1
        print(f"{file}: {c}")
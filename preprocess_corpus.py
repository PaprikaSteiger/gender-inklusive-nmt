from load_corpus import DIR
from pathlib import Path

from sacremoses import MosesTokenizer, MosesPunctNormalizer, MosesTruecaser

SENT_MIN: int = 5
SENT_MAX: int = 30


def preprocess_german_corpus(in_file: Path, out_file: Path, truecaser_path: Path):
    with open(in_file, encoding="utf8") as inn, open(out_file, "w", encoding="utf8") as out:
        mnorm = MosesPunctNormalizer(lang="de")
        mtok = MosesTokenizer(lang="de")
        mtrue = train_truecase(truecaser_path=truecaser_path, training_corpus=in_file)

        for i, line in enumerate(inn, start=1):
            line = mnorm.normalize(line)
            line = mtok.tokenize(line, return_str=True)
            line = mtrue.truecase(line, return_str=True)
            line = str(i) + "\t" + line + "\n"
            out.write(line)


# although I used a generator to iterate over all sentences while training the truecaser, I ran into a memory error
# after 1'254'149 sentences
# so let s just limit it for now to 1'000'000
def limit_generator(limit):
    def limiter(generator):
        for i, item in enumerate(generator):
            if i > limit:
                break
            else:
                yield item
    return limiter


def train_truecase(truecaser_path: Path, training_corpus: Path):
    limiter = limit_generator(limit=1000000)
    if truecaser_path.exists():
        mtrue = MosesTruecaser(str(truecaser_path))
    else:
        mtrue = MosesTruecaser()
        mtrue.train(
            limiter(line for line in training_corpus.open("r", encoding="utf8")),
            save_to=truecaser_path,
            progress_bar=True
        )
    return mtrue


if __name__ == "__main__":
    preprocess_german_corpus(
        in_file=(DIR / "europarl-v7.de-en.de"),
        out_file=(DIR / "tokenized_normalized_truecased.de"),
        truecaser_path=(DIR / "german.truecase")
    )


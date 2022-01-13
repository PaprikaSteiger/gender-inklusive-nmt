from pathlib import Path
import typing as t

import spacy
from spacy.matcher import Matcher
from spacy.tokens import Doc, Span
from spacy.tokens import Token
from load_corpus import DIR

from replace_functions_fr import replace_article, replace_adjective, replace_noun

# customize spacy Token slightly to have attribute vor replaced text
Token.set_extension("value", default="")

# general noun suffix
noun_lemma_endings = [
                      "eur", "rice"
                      "er", "ère"
]

# nouns that should not be change
no_replacment = [
                 "Monsieur",
                 "M.",
                 "Madame",
                 "Mme",
]

def on_match_art_adj_n(
        matcher: spacy.matcher.Matcher,
        doc: spacy.tokens.Doc,
        i: int,
        matches: t.List[t.Tuple],
        replacements: t.Dict[str, str]=replacements,
        gender_token: str="・",
) -> None:
    # get the matched tokens
    match_id, start, end = matches[i]
    entities = [t for t in Span(doc, start, end, label="EVENT")]

    article = entities.pop(0)
    noun = entities.pop(-1)
    # TODO: decide given the noun whether to replace or not
    # Check if the noun is person
    if not any(noun.lemma_.endswith(ending) for ending in noun_lemma_endings):
        return None
    # no adjective
    if len(entities) == 0:
        replace_noun(noun=noun, gender_token=gender_token)
        replace_article(article=article, gender_token=gender_token)
    else:
        adjective = [t for t in entities if t.tag_ == "ADJ"]
        replace_noun(noun = noun, gender_token = gender_token)
        replace_article(article = article, gender_token = gender_token)
        for adj in adjective:
            replace_adjective(adj = adj, gender_token=gender_token)


def clean_annotated_file(infile: Path, outfile: Path):
    with open(infile, "r", encoding="utf8") as inn, open(outfile, "w", encoding="utf8") as out:
        for sent in inn:
            sent = line.split()
            sent = " ".join(line[2:])
            out.write(sent + "\n")

if __name__ == "__main__":
    nlp = spacy.load("fr_core_news_lg")
    matcher = Matcher(nlp.vocab)
    art_adj_n = [{"TAG": "ART"}, {"TAG": "ADJ"}, {"POS": "NOUN"}]
    matcher.add("art_adj_n", [art_adj_n], on_match=on_match_art_adj_n)
    # TODO: update annotated data
    infile = DIR / ""
    outfile = DIR / ""
    #clean_annotated_file(infile=(DIR / "german_annotated1.txt"), outfile=infile)
    with open(infile, "r", encoding="utf8") as inn:
        for sent in inn:
            print(sent)
            doc = nlp(sent)
            matches = matcher(doc)
            print(matches)
            text = " ".join(t._.value or t.text for t in doc)
            print(text)
            breakpoint()



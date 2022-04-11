from pathlib import Path
import typing as t

import spacy
from spacy.matcher import Matcher
from spacy.tokens import Doc, Span, Token
from load_corpus import DIR

from replace_functions_fr import replace_pron, replace_noun, replace_det, replace_adj

# customize spacy Token slightly to have attribute vor replaced text
Token.set_extension("value", default="")

# general noun suffix
noun_lemma_endings = [
    "eau", "el", "elle",
    "teur", "trice", "teuse",
    "deur", "drice", #"deuse",
    "eur", "euse", "eure",
    "oux", "ouse", "ousse", "ouce",
    "eux", "euse",
    "s", "se", #"sse",
    "tre", "tresse",
    "en", "enne",
    "ien", "ienne",
    "er", "ère",
    "ier", "ière",
    "nt", "nte",
    "nd", "nde",
    "t", "te",
    "on", "onne",
    "u", "ue",
    "é", "ée",
    "i", "ie",
    "al", "ale",
    "ef", "effe",
    "tif", "tive"
    #"in", "ine",
    #"e", "esse"
]

# nouns that should not be change
noun_no_replacement = [
    "Monsieur", "M.", "roi",
    "Madame", "Mme", "dame", "reine",
    "héro", "gars", "type", "mec",
    "homme", "femme", "mari", "mâle", "femelle",
    "fils","fille","garçon", "bébé", "enfant", "adulte",
    "grand-père", "grand-mère", "père", "mère", "papa", "maman",
    "parrain", "marraine", "soeur", "frère",
    "oncle", "tante", "neveu", "nièce",
    "personne", "individu", "humain", "gens", "monde", "peuple", "ancêtre",
    "moine", "moniale"
]

# general adj suffix
adj_lemma_endings = [
    "eau", "el", "elle",
    "teur", "trice", "teuse",
    "deur", "drice",  #"deuse",
    "eur", "euse", "eure",
    "oux", "ouse", "ousse", "ouce",
    "eux", "euse",
    "s", "se", #"sse",
    "tre", "tresse",
    "en", "enne",
    "ien", "ienne",
    "er", "ère",
    "ier", "ière",
    "nt", "nte",
    "nd", "nde",
    "t", "te",
    "on", "onne",
    "u", "ue",
    "é", "ée",
    "i", "ie",
    "al", "ale",
    "ef", "effe",
    "tif", "tive"
    # "in", "ine",
    # "e", "esse",
    # #"ai", "aie",
    #"il", "elle",
    #"ul", "ulle"
    #"et", "ette", "ète",
    #"gu", "güe",
    #"ou", "olle",
    #"f", "ve",
    #"g", "gue",
]

def on_match_det_noun_adj(
        matcher: spacy.matcher.Matcher,
        doc: spacy.tokens.Doc,
        i: int,
        matches: t.List[t.Tuple],
        gender_token: str="·",
) -> None:
    # get the matched tokens
    match_id, start, end = matches[i]
    entities = [t for t in Span(doc, start, end, label="EVENT")]
    det = entities.pop(0)
    noun = entities.pop(-1)
    # TODO: decide given the noun whether to replace or not
    # Noun suffix list
    if not any(noun.lemma_.endswith(ending) for ending in noun_lemma_endings):
        return None
    # rewritting nouns without adjective
    if len(entities) == 0:
        replace_noun(noun=noun, gender_token=gender_token)
        if gender_token in noun._.value:
            replace_det(det=det, gender_token=gender_token)
    else: #rewritting nouns with adjective
        adjective = [t for t in entities if t.tag_ == "ADJ"]
        replace_noun(noun=noun, gender_token=gender_token)
        if gender_token in noun._.value:
            replace_det(det=det, gender_token=gender_token)
            for adj in adjective:
                replace_adj(adj=adj, gender_token=gender_token)


def on_match_pron(
        matcher: spacy.matcher.Matcher,
        doc: spacy.tokens.Doc,
        i: int,
        matches: t.List[t.Tuple],
        gender_token: str = "·",
) -> None:
    # simple approach, if there is a named entity in the doc, don't change anything
    # TODO: more sophisticated approach for entity resolution
    if bool(doc.ents):
        return None
    # get the matched tokens
    match_id, start, end = matches[i]
    entities = [t for t in Span(doc, start, end, label="EVENT")]
    assert len(entities) == 1
    pronoun = entities[0]
    replace_pron(pron=pronoun, gender_token=gender_token)

def on_match_pron_adj(
        matcher: spacy.matcher.Matcher,
        doc: spacy.tokens.Doc,
        i: int,
        matches: t.List[t.Tuple],
        gender_token: str = "·",
) -> None:
    # get the matched tokens
    match_id, start, end = matches[i]
    entities = [t for t in Span(doc, start, end, label="EVENT")]
    assert len(entities) == 1
    adj = entities[0]
    replace_adj(adj=adj, gender_token=gender_token)

def on_match_pron_noun(
        matcher: spacy.matcher.Matcher,
        doc: spacy.tokens.Doc,
        i: int,
        matches: t.List[t.Tuple],
        no_replacements: t.Dict[str, str]=noun_no_replacement,
        gender_token: str = "·",
) -> None:
    # get the matched tokens
    match_id, start, end = matches[i]
    entities = [t for t in Span(doc, start, end, label="EVENT")]
    assert len(entities) == 1
    noun = entities[0]
    replace_noun(noun=noun, gender_token=gender_token)


def clean_annotated_file(infile: Path, outfile: Path):
    with open(infile, "r", encoding="utf8") as inn, open(outfile, "w", encoding="utf8") as out:
        for sent in inn:
            sent = sent.split()
            sent = " ".join(sent[2:])
            out.write(sent + "\n")

def compare_files(gold_file: Path, trial_file: Path):
    differences = []
    with gold_file.open("r", encoding="utf8") as gold, trial_file.open("r", encoding="utf8") as trial, open((outfile.parent / "differences.txt"), "w", encoding="utf8") as out:
        for gold_line, trial_line in zip(gold, trial):
            if not gold_line.replace(" ", "") == trial_line.replace(" ", ""):
                differences.append(trial_line)
        for d in differences:
            out.write(d)
    return differences

if __name__ == "__main__":
    det_noun_adj=[
        {"POS": "DET"},
        {"POS": "ADJ", "OP": "*"},
        {"POS": "NOUN"},
        {"POS": "ADJ", "OP": "*"},
        {"LEMMA": {"IN": ["et", "mais", "ou"]}, "OP": "*"},
        {"IS_PUNCT": True, "OP": "?"},
        {"POS": "ADJ", "OP": "*"}
    ]

    pron=[
        {"POS": "PRON", "MORPH": {"INTERSECTS": ["Number=Sing", "Number=Plur", "Gender=Masc", "Gender=Fem"]}
        }
    ]

    pron_adj=[
        {"POS": "PRON", "MORPH": {"INTERSECTS": ["Person=1", "Person=2"]}, "OP": "+"},
        {"POS": "ADJ", "OP": "+"}
    ]

    pron_noun=[
        {"POS": "PRON", "MORPH": {"INTERSECTS": ["Person=1", "Person=2"]}, "OP": "+"},
        {"POS": "NOUN"}
    ]

    pron_det_noun_adj=[
        {"POS": "PRON", "MORPH": {"INTERSECTS": ["Person=3"]}, "OP": "+"},
        {"POS": "NOUN"}
    ]

    person_noun=[
        {"TEXT": {"IN": [noun_no_replacement]}, "OP": "+"},
        {"POS": "NOUN"}
    ]

    nlp = spacy.load("fr_core_news_lg")
    matcher = Matcher(nlp.vocab)
    matcher.add("det_noun_adj", [det_noun_adj], on_match=on_match_det_noun_adj)
    matcher.add("pron", [pron], on_match=on_match_pron)
    matcher.add("pron_adj", [pron_adj], on_match=on_match_pron_adj)
    #matcher.add("pron_det_noun_adj", [pron_det_noun_adj], on_match=pron_det_noun_adj)
    #matcher.add("person_noun", [person_noun], on_match=person_noun)
    infile = DIR / "fr_train_set.txt"
    outfile = DIR / "fr_train_annotated_inclusive_spacy.txt"

    with open(infile, "r", encoding="utf8") as inn, open(outfile, "w", encoding="utf8") as out:
        for sent in inn:
            print(sent)
            doc = nlp(sent)
            print([t.tag_ for t in doc])
            print([t.pos_ for t in doc])
            matches = matcher(doc)
            print(matches)
            text = " ".join(t._.value or t.text for t in doc)
            print(text)
            out.write(text)

    compare_files(gold_file=(DIR / "fr_train_set_annotated.txt"), trial_file=outfile)

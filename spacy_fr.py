from pathlib import Path
from tqdm import tqdm
import typing as t
import spacy
from spacy.matcher import Matcher
from spacy.tokens import Doc, Span, Token
from load_corpus import DIR
from replace2_functions_fr import replace_pron, replace_noun, replace_det, replace_adj

# customize spacy Token slightly to have attribute vor replaced text
Token.set_extension("value", default="")

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
    det = entities[0]
    noun = entities[-1]
    # rewriting nouns without adjective
    if len(entities) == 0:
        if doc.ents:
            if 'PER' in [t.ent_type_ for t in doc]:
                return None
            else:
                replace_noun(noun=noun, gender_token=gender_token)
                if gender_token in noun._.value:
                    replace_det(det=det, gender_token=gender_token)
    else: #rewriting nouns with adjective
        adjective = [t for t in entities if t.tag_ == "ADJ"]
        if doc.ents:
            if 'PER' in [t.ent_type_ for t in doc]:
                return None
            else:
                replace_noun(noun=noun, gender_token=gender_token)
                if gender_token in noun._.value:
                    replace_det(det=det, gender_token=gender_token)
                    for adj in adjective:
                        replace_adj(adj=adj, gender_token=gender_token)

def on_match_pron3(
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
    pronoun = entities[0]
    noun = entities[-1]
    if len(entities) == 0:
         replace_noun(noun=noun, gender_token=gender_token)
         if gender_token in noun._.value:
             replace_pron(pron=pronoun, gender_token=gender_token)

def on_match_pron12_adj(
        matcher: spacy.matcher.Matcher,
        doc: spacy.tokens.Doc,
        i: int,
        matches: t.List[t.Tuple],
        gender_token: str = "·",
) -> None:
    # get the matched tokens
    match_id, start, end = matches[i]
    entities = [t for t in Span(doc, start, end, label="EVENT")]
    #assert len(entities) == 1
    adj = entities[0]
    replace_adj(adj=adj, gender_token=gender_token)

def on_match_pron12_noun(
        matcher: spacy.matcher.Matcher,
        doc: spacy.tokens.Doc,
        i: int,
        matches: t.List[t.Tuple],
        gender_token: str = "·",
) -> None:
    # get the matched tokens
    match_id, start, end = matches[i]
    entities = [t for t in Span(doc, start, end, label="EVENT")]
    #assert len(entities) == 1
    noun = entities[0]
    replace_noun(noun=noun, gender_token=gender_token)

if __name__ == "__main__":

    det_noun_adj=[
        {"POS": "VERB", "OP": "?"},
        {"IS_PUNCT": True, "OP": "?"},
        {"POS": "DET", "MORPH": {"INTERSECTS": ["Definite=Def", "Definite=Ind", "PronType=Dem", "Poss=Yes", "Number=Plur"]}, "OP": "?"},
        {"POS": "ADJ", "OP": "?"},
        {"POS": "NOUN", "DEP": {"INTERSECTS": ["nsubj", "nsubj:pass", "obj", "obl:arg", "nmod", "nmod:pass"]}},
        {"POS": "NOUN", "OP": "?"},
        {"POS": "ADJ", "OP": "?"},
        {"POS": "CONJ", "OP": "?"},
        {"IS_PUNCT": True, "OP": "?"},
        {"POS": "ADJ", "OP": "?"}
    ]

    pron3=[
        {"POS": "PRON", "MORPH": {"INTERSECTS": ["Number=Sing", "Number=Plur", "Gender=Masc", "Gender=Fem", "Person=3"]}}
    ]

    pron12_adj=[
        {"POS": "PRON", "MORPH": {"INTERSECTS": ["Person=1", "Person=2"]}, "OP": "+"},
        {"POS": "ADJ", "OP": "+"}
    ]

    pron12_noun=[
        {"POS": "PRON", "MORPH": {"INTERSECTS": ["Person=1", "Person=2"]}, "OP": "+"},
        {"POS": "NOUN"}
    ]

    nlp = spacy.load("fr_core_news_lg")
    matcher = Matcher(nlp.vocab)
    matcher.add("det_noun_adj", [det_noun_adj], on_match=on_match_det_noun_adj)
    matcher.add("pron3", [pron3], on_match=on_match_pron3)
    matcher.add("pron12_adj", [pron12_adj], on_match=on_match_pron12_adj)
    matcher.add("pron12_noun", [pron12_noun], on_match=on_match_pron12_noun)

    infile = DIR / "test.fr"
    outfile = DIR / "test_spacy1.fr"

    with open(infile, "r", encoding="utf8") as inn, open(outfile, "w", encoding="utf8") as out:
        for sent in tqdm(inn):
            print(sent)
            doc = nlp(sent)
            print([t.tag_ for t in doc])
            print([t.pos_ for t in doc])
            matches = matcher(doc)
            print(matches)
            text = " ".join(t._.value or t.text for t in doc)
            print(text)
            out.write(text)



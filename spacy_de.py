from pathlib import Path
import typing as t

import spacy
from spacy.matcher import Matcher
from spacy.tokens import Doc, Span
from spacy.tokens import Token
from load_corpus import DIR

from replace_functions import replace_article, replace_adjective, \
    replace_noun, get_declination_type, replace_personal_pronoun
from special_cases_de import gendered_no_replacement, noun_lemma_endings

# list of all pos tags, dependencies etc
# https://github.com/explosion/spaCy/blob/master/spacy/glossary.py
# important linguistic features
#                 token.text
#                 token.lex # lexeme
#                 token.ent_type_ #
#                 token.ent_iob_ # B for beginning, I vor in, O for outside, '' for no entity
#                 token.lemma_
#                 token.pos_ # coarse grained pos
#                 token.tag_ # fine grained pos tags
#                 token.dep_ # dependency tag
#                 token.is_punct # if punctuation or not
#By default, the matcher will only return the matches and not do anything else,
# like merge entities or assign labels.
# This is all up to you and can be defined individually
# for each pattern, by passing in a callback function as the on_match argument on
# add(). This is useful, because it lets you write entirely custom and pattern-specific logic.
# For example, you might want to merge some patterns into one token,
# while adding entity labels for other pattern types.
# You shouldn’t have to create different matchers for each of those processes.

# customize spacy Token slightly to have attribute vor replaced text
Token.set_extension("value", default="")

# special words
pronouns = {
    # jeder
    # jedermann
}

special_cases = [
    "kein", # mixed declination, not weak one


]


def on_match_ar_ad_nn(
        matcher: spacy.matcher.Matcher,
        doc: spacy.tokens.Doc,
        i: int,
        matches: t.List[t.Tuple],
        gender_token: str=":",
) -> None:
    # get the matched tokens
    match_id, start, end = matches[i]
    entities = [t for t in Span(doc, start, end, label="EVENT")]
    article = entities.pop(0)
    noun = entities.pop(-1)
    # TODO decide given the noun whether to replace anything or not -> or is this a job for the replace noun function?
    # Check endings of lemma
    # check the noun if something has to be replaced
    # if noun.lemma_ in gendered_no_replacement:
    #     return
    # # todo: move this part to the replace noun function, so I might check the noun of a match if it was change and decide based on that if the rest has to be changed or not
    # if not any(noun.lemma_.endswith(ending) for ending in noun_lemma_endings):
    #     return None
    # no adjective or adverb
    if len(entities) == 0:
        if replace_noun(noun=noun, gender_token=gender_token):
            replace_article(article=article, gender_token=gender_token)
    else:
        # adverbs are invariant in German, so just replace the adjectives
        # also ignore cunjunctions and punctuation
        adjectives = [t for t in entities if t.tag_ == "ADJA"]

        if replace_noun(noun=noun, gender_token=gender_token):
            declination_type = get_declination_type(determiner=article)
            replace_article(article=article, gender_token=gender_token)
            for adjective in adjectives:
                replace_adjective(adjective=adjective, declination_type=declination_type, gender_token=gender_token)


def on_match_pp(
        matcher: spacy.matcher.Matcher,
        doc: spacy.tokens.Doc,
        i: int,
        matches: t.List[t.Tuple],
        gender_token: str = ":",
) -> None:
    # simmple approach, if there is a named entity in the doc, don't change anything
    # TODO: more sophisticated approach for entity resolution
    if bool(doc.ents):
        return None
    # get the matched tokens
    match_id, start, end = matches[i]
    entities = [t for t in Span(doc, start, end, label="EVENT")]
    assert len(entities) == 1
    pronoun = entities[0]
    replace_personal_pronoun(pronoun=pronoun, gender_token=gender_token)


def on_match_ip_dp_nn(
        matcher: spacy.matcher.Matcher,
        doc: spacy.tokens.Doc,
        i: int,
        matches: t.List[t.Tuple],
        gender_token: str = ":",
) -> None:
    # get the matched tokens
    match_id, start, end = matches[i]
    entities = [t for t in Span(doc, start, end, label="EVENT")]
    pronoun = entities.pop(0)
    noun = entities.pop(0)
    # the pronoun follows (as it is used attributively without determiner) the strong declination of an adjective
    # only transform pronoun if transformation applied to noun
    if replace_noun(noun=noun, gender_token=gender_token):
        replace_adjective(adjective=pronoun, declination_type="strong", gender_token=gender_token)


def on_match_ad_nn(
        matcher: spacy.matcher.Matcher,
        doc: spacy.tokens.Doc,
        i: int,
        matches: t.List[t.Tuple],
        gender_token: str=":",
) -> None:
    # get the matched tokens
    match_id, start, end = matches[i]
    entities = [t for t in Span(doc, start, end, label="EVENT")]
    # first token is the not-determiner
    entities.pop(0)
    noun = entities.pop(-1)
    # check how many adjectives
    # if there is no determiner, its always going to be a strong declination
    declination_type = "strong"
    if len(entities) == 1:
        adjective = entities[0]
        if replace_noun(noun=noun, gender_token=gender_token):
            replace_adjective(adjective=adjective, declination_type=declination_type, gender_token=gender_token)
    else:
        # adverbs are invariant in German, so just replace the adjectives
        adjectives = [t for t in entities if t.tag_ == "ADJA"]
        if replace_noun(noun=noun, gender_token=gender_token):
            for adjective in adjectives:
                replace_adjective(adjective=adjective, declination_type=declination_type, gender_token=gender_token)

def on_match_pp_ad_nn(
        matcher: spacy.matcher.Matcher,
        doc: spacy.tokens.Doc,
        i: int,
        matches: t.List[t.Tuple],
        gender_token: str=":",
) -> None:
    # get the matched tokens
    match_id, start, end = matches[i]
    entities = [t for t in Span(doc, start, end, label="EVENT")]
    # first token is possessive determiner
    pos = entities.pop(0)
    noun = entities.pop(-1)
    print(entities)
    # check how many words are left and if adjective
    if replace_noun(noun=noun, gender_token=gender_token):
        # replace possessive determiner
        replace_adjective(adjective=pos, declination_type="strong", gender_token=gender_token)
        adjectives = [t for t in entities if t.tag_ == "ADJA"]
        for adjective in adjectives:
            replace_adjective(adjective=adjective, declination_type="weak", gender_token=gender_token)


def on_match_su_ip_dp(
    matcher: spacy.matcher.Matcher,
    doc: spacy.tokens.Doc,
    i: int,
    matches: t.List[t.Tuple],
    gender_token: str=":",
):
    # get the matched tokens
    match_id, start, end = matches[i]
    entities = [t for t in Span(doc, start, end, label="EVENT")]
    # first token is the not-determiner
    pronoun = entities.pop(-1)
    replace_adjective(adjective=pronoun, declination_type="strong", gender_token=gender_token)
    if entities:
        art = entities.pop(0)
        replace_article(article=art, gender_token=gender_token)


def on_match_nn(
    matcher: spacy.matcher.Matcher,
    doc: spacy.tokens.Doc,
    i: int,
    matches: t.List[t.Tuple],
    gender_token: str = ":",
):
    # get the matched tokens
    match_id, start, end = matches[i]
    entities = [t for t in Span(doc, start, end, label="EVENT")]
    noun = entities.pop(0)
    replace_noun(noun=noun, gender_token=gender_token)


def on_match_rel(
    matcher: spacy.matcher.Matcher,
    doc: spacy.tokens.Doc,
    i: int,
    matches: t.List[t.Tuple],
    gender_token: str = ":",
):
    # get the matched tokens
    match_id, start, end = matches[i]
    entities = [t for t in Span(doc, start, end, label="EVENT")]
    rel = entities.pop(0)
    # the relative pronoun is child of root of relative clause, thus check head of head if it has been replaced
    ref = rel.head.head
    if gender_token in ref._.value:
        replace_article(rel, gender_token=gender_token)


def clean_annotated_file(infile: Path, outfile: Path):
    with open(infile, "r", encoding="utf8") as inn, open(outfile, "w", encoding="utf8") as out:
        for line in inn:
            line = line.split()
            line = " ".join(line[2:])
            out.write(line + "\n")


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
    #patterns
    # start writing rules
    # us .sent to get sentence span of matched tokens
    # or .doc if only sentences processed at once

    # noun phrases with article modified by possibly various adjectives and adverbs
    # possible separated by a conjunction or
    # TODO: what about adj, adj, adj (...) noun?
    # das sehr grosse, besonders grüne Haus
    ar_ad_nn = [
        {"TAG": "ART"},
        {"POS": "ADV", "OP": "*"},
        {"TAG": "ADJA", "OP": "*"},
        {"IS_PUNCT": True, "OP": "?"},
        {"POS": "ADV", "OP": "*"},
        {"TAG": "ADJA", "OP": "*"},
        {"POS": "NOUN"}
    ]

    # noun phrase without determiner modified by adjectives
    # just adjective and noun not preceded by article
    # e.g. in a case where it is preceded by und we might have to check whether we transformed something before
    # TODO: this also matches noun preceded by nothing, do we want that?
    # TODO. probably not, a sentences starting with a noun that needs to be replaced wouldn't be matched. So probably as a last step just check for single nouns
    # e.g. von Lehrer:in zu Schüler:in
    ad_nn = [
        {"POS": {"NOT_IN": ["DET"]}},
        {"POS": {"IN":["ADV", "ADJD"]}, "OP": "*"},
        {"TAG": "ADJA", "OP": "+"}, # with + single nouns are not matched
        {"LEMMA": {"IN": ["und", "sowie"]}, "OP": "*"},
        {"IS_PUNCT": True, "OP": "?"},
        {"POS": {"IN":["ADV", "ADJD"]}, "OP": "*"},
        {"TAG": "ADJA", "OP": "*"},
        {"POS": "NOUN"}
    ]

    # noun phrase with attributive indefinite or demonstrative pronoun
    ip_dp_nn = [
        {"TAG": "ART", "OP": "?"},
        {"TAG": {"IN": ["PDAT", "PIAT"]}},
        {"POS": "NOUN"},
    ]

    # noun phrase with attributive possessive pronoun and possible adjectives
    pp_ad_nn = [
        {"TAG": "PPOSAT"},
        # {"POS": {"IN": ["ADV"]}, "OP": "*"},
        # {"TAG": "ADJA", "OP": "*"},
        # {"LEMMA": {"IN": ["und", "sowie"]}, "OP": "?"},
        # {"IS_PUNCT": True, "OP": "?"},
        # {"POS": {"IN": ["ADV", "ADJD"]}, "OP": "*"},
        {"TAG": "ADJA", "OP": "*"},
        {"POS": "NOUN"}
    ]

    # isolated noun not preceded by any determiner or pronoun
    nn_isolated = [
        {"POS": "NOUN"}
    ]
    # personal pronoun, no entity in sentence, no object, not referring to a noun not describing a person
    pp = [
        {"TAG": "PPER", "MORPH": {"INTERSECTS": ["Number=Sing", "Gender=Masc", "Gender=Fem"]}}
    ]
    # substitution indefinite or demonstrative pronoun:
    su_ip_dp = [
        {"TAG": "ART", "OP": "?"},
        {"TAG": {"IN": ["PDS", "PIS"]}}
    ]

    relpro = [
        {"TAG": {"IN": ["PRELAT", "PRELS"]}},
    ]
    # bool(doc.ents) == False or # pronoun doesn t refer to entity
    # possesive pronoun, third person

    # typical noun endings referring to persons, male
    # {"er", "or", "ent", "tekt", "eur",

    # indefinite or demonstrative pronoun attributive


    nlp = spacy.load("de_core_news_lg")
    matcher = Matcher(nlp.vocab)
    matcher.add("ar_ad_nn", [ar_ad_nn], on_match=on_match_ar_ad_nn)
    #matcher.add("pp", [pp], on_match=on_match_pp)
    matcher.add("id_dp_nn", [ip_dp_nn], on_match=on_match_ip_dp_nn)
    matcher.add("ad_nn", [ad_nn], on_match=on_match_ad_nn)
    matcher.add("su_ip_dp", [su_ip_dp], on_match=on_match_su_ip_dp)
    matcher.add("pp_ad_nn", [pp_ad_nn], on_match=on_match_pp_ad_nn)
    matcher.add("isolated_nn", [nn_isolated], on_match=on_match_nn)
    matcher.add("rel_pro", [relpro], on_match=on_match_rel)
    infile = DIR / "german_annotated.txt"
    outfile = DIR / "german_annotated_inclusiv_spacy.txt"
    #clean_annotated_file(infile=(DIR / "german_annotated_inclusive.txt"), outfile=(DIR / "german_annotated_inclusive_clean.txt"))
    with open(infile, "r", encoding="utf8") as inn, open(outfile, "w", encoding="utf8") as out:
        for line in inn:
            print(line)
            doc = nlp(line)
            replace = True
            # check for entities referring to persons
            if doc.ents:
                if 'PER' in [t.ent_type_ for t in doc]:
                    replace = False
            # check for tokens inhibiting replacements
            for lemma in [t.lemma_ for t in doc]:
                if lemma in gendered_no_replacement:
                    replace = False
            if replace:

                print([t.lemma_ for t in doc ])
                #print([t.pos_ for t in doc])
                matches = matcher(doc)
                #print(matches)
            text = " ".join(t._.value or t.text for t in doc)
            #print(text)
            out.write(text)
                #breakpoint()
                # for token in doc:
                #     print(
                #         token.text,
                #         token.morph,
                        # token.ent_type_,
                        # token.ent_iob_,
                        # token.lemma_,
                        # token.pos_,
                        # token.tag_,
                        # token.dep_,
                        # token.is_punct
                #    )

    compare_files(gold_file=(DIR / "german_annotated_inclusive_clean.txt"), trial_file=outfile)
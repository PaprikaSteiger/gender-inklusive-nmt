from pathlib import Path
import typing as t

import spacy
from spacy.matcher import Matcher
from spacy.tokens import Doc, Span
from spacy.tokens import Token
from tqdm import tqdm


from load_corpus import DIR
from replace_functions_de import (
    replace_article,
    replace_adjective,
    replace_noun,
    get_declination_type,
    replace_personal_pronoun,
)
from special_cases_de import (
    gendered_no_replacement,
    noun_lemma_endings,
    pre_replacements,
)
from util import clean_annotated_file, compare_files, tokenize, DIR

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
# By default, the matcher will only return the matches and not do anything else,
# like merge entities or assign labels.
# This is all up to you and can be defined individually
# for each pattern, by passing in a callback function as the on_match argument on
# add(). This is useful, because it lets you write entirely custom and pattern-specific logic.
# For example, you might want to merge some patterns into one token,
# while adding entity labels for other pattern types.
# You shouldn’t have to create different matchers for each of those processes.

# customize spacy Token slightly to have attribute vor replaced text
Token.set_extension("value", default="")


def on_match_ar_ip_pp_ad_nn(
    matcher: spacy.matcher.Matcher,
    doc: spacy.tokens.Doc,
    i: int,
    matches: t.List[t.Tuple],
    gender_token: str = ":",
) -> None:
    # get the matched tokens
    match_id, start, end = matches[i]
    # breakpoint()
    entities = [t for t in Span(doc, start, end, label="EVENT")]
    noun = entities.pop(-1)
    # only noun
    if len(entities) == 0:
        replace_noun(noun=noun, gender_token=gender_token)
        return
    # check for articles, pronouns and adjectives
    article, pronoun, pronoun2 = False, False, False
    token = entities.pop(0)
    if token.tag_ == "ART":
        article = token
    elif token.tag_ in ["PDAT", "PIAT", "PPOSAT"]:
        pronoun = token
    try:
        if entities[0].tag_ in ["PDAT", "PIAT", "PPOSAT"]:
            if pronoun:
                pronoun2 = entities.pop(0)
            else:
                pronoun = entities.pop(0)
    except IndexError:
        pass

    if len(entities) == 0:
        if replace_noun(noun=noun, gender_token=gender_token):
            if article:
                replace_article(article=article, gender_token=gender_token)
            if pronoun:
                if pronoun.lemma_ == "kein":
                    # kein identical with indefinite article
                    replace_article(
                        article=pronoun,
                        gender_token=gender_token,
                        manual_morph="Definite=Ind",
                    )
                else:
                    replace_adjective(
                        adjective=pronoun,
                        declination_type="strong",
                        gender_token=gender_token,
                    )
            if pronoun2:
                if pronoun.lemma_ == "kein":
                    # kein identical with indefinite article
                    replace_article(
                        article=pronoun,
                        gender_token=gender_token,
                        manual_morph="Definite=Ind",
                    )
                else:
                    replace_adjective(
                        adjective=pronoun,
                        declination_type="strong",
                        gender_token=gender_token,
                    )
    else:
        if replace_noun(noun=noun, gender_token=gender_token):
            declination_type = ""
            adjectives = [t for t in entities if t.tag_ == "ADJA"]
            if article:
                declination_type = get_declination_type(determiner=article)
                replace_article(article=article, gender_token=gender_token)
            elif pronoun:
                if not declination_type:
                    declination_type = get_declination_type(determiner=pronoun)
                if pronoun.lemma_ == "kein":
                    # kein identical with indefinite article
                    replace_article(
                        article=pronoun,
                        gender_token=gender_token,
                        manual_morph="Definite=Ind",
                    )
                else:
                    replace_adjective(
                        adjective=pronoun,
                        declination_type="strong",
                        gender_token=gender_token,
                    )
            elif pronoun2:
                if not declination_type:
                    declination_type = get_declination_type(determiner=pronoun2)
                if pronoun.lemma_ == "kein":
                    # kein identical with indefinite article
                    replace_article(
                        article=pronoun,
                        gender_token=gender_token,
                        manual_morph="Definite=Ind",
                    )
                else:
                    replace_adjective(
                        adjective=pronoun,
                        declination_type="strong",
                        gender_token=gender_token,
                    )
            for adjective in adjectives:
                replace_adjective(
                    adjective=adjective,
                    declination_type=declination_type,
                    gender_token=gender_token,
                )


def on_match_pp(
    matcher: spacy.matcher.Matcher,
    doc: spacy.tokens.Doc,
    i: int,
    matches: t.List[t.Tuple],
    gender_token: str = ":",
) -> None:
    # simmple approach, if there is a named entity in the doc, don't change anything
    if bool(doc.ents):
        return None
    # get the matched tokens
    match_id, start, end = matches[i]
    entities = [t for t in Span(doc, start, end, label="EVENT")]
    assert len(entities) == 1
    pronoun = entities[0]
    replace_personal_pronoun(pronoun=pronoun, gender_token=gender_token)


def on_match_su_ip_dp(
    matcher: spacy.matcher.Matcher,
    doc: spacy.tokens.Doc,
    i: int,
    matches: t.List[t.Tuple],
    gender_token: str = ":",
):
    # get the matched tokens
    match_id, start, end = matches[i]
    entities = [t for t in Span(doc, start, end, label="EVENT")]
    # if nothing was replaced in this sentence, don't replace individual pronouns
    # if not any(gender_token in token._.value for token in doc):
    #     return None
    # first token is the not-determiner
    pronoun = entities.pop(-1)
    if pronoun.lemma_ == "kein":
        # kein identical with indefinite article
        replace_article(
            article=pronoun, gender_token=gender_token, manual_morph="Definite=Ind"
        )
    elif pronoun.lemma_ == "der":
        replace_article(article=pronoun, gender_token=gender_token)
    else:
        replace_adjective(
            adjective=pronoun, declination_type="strong", gender_token=gender_token
        )
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
        replace_article(rel, gender_token=gender_token, manual_morph="Definite=Def")


def spacy_pipeline(infile: str, outfile_target: str):
    # patterns
    # start writing rules
    # us .sent to get sentence span of matched tokens
    # or .doc if only sentences processed at once

    # noun phrases with article modified by possibly various adjectives and adverbs
    # possible separated by a conjunction or
    # das sehr grosse, besonders grüne Haus
    ar_ip_pp_ad_nn = [
        {"TAG": "ART", "OP": "?"},
        {"TAG": {"IN": ["PDAT", "PIAT", "PPOSAT"]}, "OP": "*"},
        {"POS": "ADV", "OP": "*"},
        {"TAG": "ADJA", "OP": "*"},
        {"IS_PUNCT": True, "OP": "?"},
        {"POS": "ADV", "OP": "*"},
        {"TAG": "ADJA", "OP": "*"},
        {"POS": "NOUN"},
    ]

    # substitution indefinite or demonstrative pronoun:
    su_ip_dp = [{"TAG": "ART", "OP": "?"}, {"TAG": {"IN": ["PDS", "PIS"]}}]

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
    # matcher.add("ar_ad_nn", [ar_ad_nn], on_match=on_match_ar_ad_nn)
    # # matcher.add("pp", [pp], on_match=on_match_pp)
    # matcher.add("id_dp_nn", [ip_dp_nn], on_match=on_match_ip_dp_nn)
    # matcher.add("ad_nn", [ad_nn], on_match=on_match_ad_nn)
    # matcher.add("pp_ad_nn", [pp_ad_nn], on_match=on_match_pp_ad_nn)
    # matcher.add("isolated_nn", [nn_isolated], on_match=on_match_nn)
    matcher.add("ar_ip_pp_ad_nn", [ar_ip_pp_ad_nn], on_match=on_match_ar_ip_pp_ad_nn)
    matcher.add("su_ip_dp", [su_ip_dp], on_match=on_match_su_ip_dp)
    matcher.add("rel_pro", [relpro], on_match=on_match_rel)
    with open(infile, "r", encoding="utf8") as inn, open(
        outfile_target, "w", encoding="utf8"
    ) as out:
        for line in tqdm(inn):
            # print(line)
            for ele, replacement in pre_replacements.items():
                if ele in line:
                    line = line.replace(ele, replacement)
            doc = nlp(line)
            # irregular replacements
            # for token in doc:
            #     if token.lemma_ in irregular_replacements:
            replace = True
            # check for entities referring to persons
            if doc.ents:
                if "PER" in [t.ent_type_ for t in doc]:
                    replace = False
            # check for tokens inhibiting replacements
            for lemma in [t.lemma_ for t in doc]:
                if lemma in gendered_no_replacement:
                    replace = False
            if replace:
                # print([t.lemma_ for t in doc ])
                # print([t.pos_ for t in doc])
                matches = matcher(doc)
                # print(matches)
            text = " ".join(t._.value or t.text for t in doc)
            # print(text)
            out.write(text)
            # breakpoint()
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


if __name__ == "__main__":
    # infile = r"C:\Users\steig\Desktop\Neuer Ordner\data\train_data_de.txt"
    # outfile_source = r"C:\Users\steig\Desktop\Neuer Ordner\data\train_data__tokenized_de2.txt"
    # outfile = r"C:\Users\steig\Desktop\Neuer Ordner\data\train_data_annotated_de2.txt"
    # spacy_pipeline(infile=infile, outfile_target=outfile, outfile_source=outfile_source)

    outfile = r"C:\Users\steig\Desktop\Neuer Ordner\gender-inklusive-nmt\data\german_annotated_inclusiv_spacy_test3.txt"
    spacy_pipeline(
        infile=r"C:\Users\steig\Desktop\Neuer Ordner\gender-inklusive-nmt\data\test_set_de.txt",
        outfile_target=outfile,
    )
    compare_files(
        gold_file=r"C:\Users\steig\Desktop\Neuer Ordner\gender-inklusive-nmt\data\test_set_de_annotated.txt",
        trial_file=outfile,
    )
    # clean_annotated_file(infile=(DIR / "german_annotated_inclusive.txt"), outfile=(DIR / "german_annotated_inclusive_clean.txt"))

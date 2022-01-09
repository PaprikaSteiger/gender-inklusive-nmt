from pathlib import Path
import typing as t

import spacy
from spacy.matcher import Matcher
from spacy.tokens import Doc, Span
from spacy.tokens import Token
from load_corpus import DIR

# list of all pos taggs, dependencies etc
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

# important replacements
replacements = {
    "er": "er:in",
    "er_pl": "er:innen",
}
# special words
pronouns = {
    # jeder
}
# Artikel

def replace_articel(article: spacy.tokens.Token, gender_token=":"):
    morph = article.morph
    if "Number=Plur" in morph:
        return None
    if "Definite=Ind" in morph:
        if "Case=Nom" in morph:
            if "Gender=Fem" in morph:
                article._.value = article.text[:-1] + f"{gender_token}e"
            elif "Gender=Masc" in morph:
                article._.value = article.text + f"{gender_token}e"
        elif "Case=Gen" in morph:
            if "Gender=Fem" in morph:
                article._.value = article.text + f"{gender_token}s"
            elif "Gender=Masc" in morph:
                article._.value = article.text[:-1] + f"r{gender_token}s"
        elif "Case=Dat" in morph:
            if "Gender=Fem" in morph:
                article._.value = article.text + f"{gender_token}m"
            elif "Gender=Masc" in morph:
                article._.value = article.text[:-1] + f"r{gender_token}m"
        elif "Case=Acc" in morph:
            if "Gender=Fem" in morph:
                article._.value = article.text + f"{gender_token}n"
            elif "Gender=Masc" in morph:
                article._.value = article.text[:-1] + f"r{gender_token}n"
    else:
        if "Case=Nom" in morph:
            if "Gender=Fem" in morph:
                article._.value = article.text + f"{gender_token}der"
            elif "Gender=Masc" in morph:
                article._.value = f"die{gender_token}" + article.text
        elif "Case=Gen" in morph:
            if "Gender=Fem" in morph:
                article._.value = article.text + f"{gender_token}des"
            elif "Gender=Masc" in morph:
                article._.value = f"der{gender_token}" + article.text
        elif "Case=Dat" in morph:
            if "Gender=Fem" in morph:
                article._.value = article.text + f"{gender_token}dem"
            elif "Gender=Masc" in morph:
                article._.value = f"der{gender_token}" + article.text
        elif "Case=Acc" in morph:
            if "Gender=Fem" in morph:
                article._.value = article.text + f"{gender_token}den"
            elif "Gender=Masc" in morph:
                article._.value = f"die{gender_token}" + article.text


def get_declination_type(determiner: spacy.tokens.Token):
    # TODO do for other than Art:
    tag = determiner.tag_
    morph = determiner.morph
    if tag == "ART":
        if "Definite=Ind" in morph:
            return "mixed"
        else:
            return "weak"


def replace_adjective(adjective: spacy.tokens.Token, declination_type: str, gender_token=":"):
    morph = adjective.morph
    if "Number=Plur" in morph or declination_type=="weak":
        return None
    if declination_type=="strong":
        if "Case=Nom" in morph:
            if "Gender=Fem" in morph:
                adjective._.value = adjective.text + f"{gender_token}r"
            elif "Gender=Masc" in morph:
                adjective._.value = adjective.text[:-1] + f"{gender_token}r"
        elif "Case=Gen" in morph:
            if "Gender=Fem" in morph:
                adjective._.value = adjective.text + f"{gender_token}n"
            elif "Gender=Masc" in morph:
                adjective._.value = adjective.text[:-1] + f"r{gender_token}n"
        elif "Case=Dat" in morph:
            if "Gender=Fem" in morph:
                adjective._.value = adjective.text + f"{gender_token}m"
            elif "Gender=Masc" in morph:
                adjective._.value = adjective.text[:-1] + f"r{gender_token}m"
        elif "Case=Acc" in morph:
            if "Gender=Fem" in morph:
                adjective._.value = adjective.text + f"{gender_token}n"
            elif "Gender=Masc" in morph:
                adjective._.value = adjective.text[:-1] + f"r{gender_token}n"

    elif declination_type=="mixed":
        if "Case=Nom" in morph:
            if "Gender=Fem" in morph:
                adjective._.value = adjective.text + f"{gender_token}r"
            elif "Gender=Masc" in morph:
                adjective._.value = adjective.text[:-1] + f"{gender_token}r"


def replace_noun(noun: spacy.tokens.Token, gender_token=":"):
    # check the ending
    # er
    # male nouns in er
    if noun.lemma_.endswith("er") and "Gender=Masc" in noun.morph:
        if "Number=Plur" in noun.morph:
            if "Case=Dat" in noun.morph:
                noun._.value = f"ern{gender_token}innen".join(noun.text.rsplit("er", 1))
            else:
                noun._.value = f"er{gender_token}innen".join(noun.text.rsplit("er", 1))
        else:
            if "Case=Gen" in noun.morph:
                noun._.value = f"ers{gender_token}in".join(noun.text.rsplit("er", 1))
            else:
                noun._.value = f"er{gender_token}in".join(noun.text.rsplit("er", 1))
    # female nouns in in
    if noun.lemma_.endswith("in") and "Gender=Fem" in noun.morph:
        if "Number=Plur" in noun.morph:
            if "Case=Dat" in noun.morph:
                noun._.value = f"ern{gender_token}innen".join(noun.text.rsplit("in", 1))
            else:
                noun._.value = f"er{gender_token}innen".join(noun.text.rsplit("in", 1))
        else:
            if "Case=Gen" in noun.morph:
                noun._.value = f"ers{gender_token}in".join(noun.text.rsplit("in", 1))
            else:
                noun._.value = f"er{gender_token}in".join(noun.text.rsplit("in", 1))


def on_match_ar_ad_nn(
        matcher: spacy.matcher.Matcher,
        doc: spacy.tokens.Doc,
        i: int,
        matches: t.List[t.Tuple],
        replacements: t.Dict[str, str]=replacements,
        gender_token: str=":",
) -> None:
    # get the matched tokens
    match_id, start, end = matches[i]
    entities = [t for t in Span(doc, start, end, label="EVENT")]
    # TODO decide given the noun wether to replace anything or not

    if len(entities) == 2:
        article = entities.pop(0)
        noun = entities.pop(-1)
        replace_noun(noun=noun, gender_token=gender_token)
        replace_articel(article=article, gender_token=gender_token)
    else:
        # TODO: distinguish adjectives and adverbs/partikles
        article = entities.pop(0)
        noun = entities.pop(-1)
        adjectives = entities
        declination_type = get_declination_type(determiner=article)
        replace_noun(noun=noun, gender_token=gender_token)
        replace_articel(article=article, gender_token=gender_token)
        for adjective in adjectives:
            replace_adjective(adjective=adjective, declination_type=declination_type, gender_token=gender_token)


def clean_annotated_file(infile: Path, outfile: Path):
    with open(infile, "r", encoding="utf8") as inn, open(outfile, "w", encoding="utf8") as out:
        for line in inn:
            line = line.split()
            line = " ".join(line[2:])
            out.write(line + "\n")


if __name__ == "__main__":
    nlp = spacy.load("de_core_news_lg")
    matcher = Matcher(nlp.vocab)
    ar_ad_nn = [{"TAG": "ART"}, {"POS": "ADV", "OP": "*"}, {"TAG": "ADJA", "OP": "*"}, {"POS": "NOUN"}]
    matcher.add("ar_ad_nn", [ar_ad_nn], on_match=on_match_ar_ad_nn)
    infile = DIR / "german_annotated.txt"
    outfile = DIR / "german_annotated_inclusiv_spacy.txt"
    #clean_annotated_file(infile=(DIR / "german_annotated1.txt"), outfile=infile)
    with open(infile, "r", encoding="utf8") as inn:
        for line in inn:
            print(line)
            doc = nlp(line)
            matches = matcher(doc)
            text = " ".join(t._.value or t.text for t in doc)
            print(text)
            breakpoint()
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

# start writing rules
# us .sent to get sentence span of matched tokens
# or .doc if only sentences processed at once
# TODO: we might encounter multiple adjectives with or without punctuation. Thus maybe apply it
# TODO: to tokens without punctuation, to catch all adjectives
# an article followed by an adjective followed by a noun
    article_adjective_phrase_noun = [
        {"TAG": "ART"},
        #{"POS": "ADV", "OP": "*"},
        {"TAG": "ADJA", "OP": "*"},
        {"POS": "NOUN"}
    ]
    ar_ad_nn = [{"TAG": "ART"}, {"POS": "ADV", "OP": "*"}, {"TAG": "ADJA", "OP": "*"}, {"POS": "NOUN"}]

# personal pronoun, no entity in sentence, no object, not referring to a noun not describing a person
    pp = [{"TAG": "PPR"}, {"MORPH": {"IS_SUBSET": ["Number=Sing", "Gender=Masc", "Gender=Fem", "Case=Nom"]}}]
    #bool(doc.ents) == False or # pronoun doesn t refer to entity
# possesive pronoun, third person


# tokens where gender inclusive shall not be used
# {"Mann", "Frau", "Mutter", "Vater"
# typical noun endings refering to persons, male
# {"er", "or", "ent", "tekt", "eur",


from pathlib import Path
import typing as t

import spacy
from spacy.matcher import Matcher
from spacy.tokens import Doc, Span
from spacy.tokens import Token
from load_corpus import DIR

from replace_functions import replace_article, replace_adjective, replace_noun, get_declination_type

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

# important noun endings
noun_lemma_endings = [
    "er", "in",
    "ent", "entin",
    "at", "atin",
    "te", "tin",
    "or", "orin",
    "eur", "euse", "eurin",
    "tekt", "tektin",
    "ender", "ende",
    "se", "sin" # Virtuose, are there other words with ending e - in?
    # yes, der Kriminelle, die Kriminelle, but it's invariant...
    # TODO: what to do with ein KriminelleR, but der KriminellE, it follows the strong, mixed, weak declination pattern




]
# tokens where gender inclusive shall not be used
no_replacment = [
    "Mann",
    "Frau",
    "Mutter",
    "Vater",
    "Computer",
]

special_nouns = [
    "Freund", "Freundin",
    "Arzt", "Ärztin",
    "Frisör", # "Friseurin",


]
# special words
pronouns = {
    # jeder
}

special_cases = [
    "kein", # mixed declination, not weak one


]

replacements = {
    "jedermann": "jeder", # shall be replaced bei jeder
}


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

    article = entities.pop(0)
    noun = entities.pop(-1)
    # TODO decide given the noun whether to replace anything or not
    # Check endings of lemma
    # check the noun if something has to be replaced
    if not any(noun.lemma_.endswith(ending) for ending in noun_lemma_endings):
        return None
    # no adjective or adverb
    if len(entities) == 0:
        replace_noun(noun=noun, gender_token=gender_token)
        replace_article(article=article, gender_token=gender_token)
    else:
        # TODO: distinguish adjectives and adverbs/partikel
        adjectives = [t for t in entities if t.tag_ == "ADJA"]
        # adverbs are invariant in German, so just replace the adjectives
        declination_type = get_declination_type(determiner=article)
        replace_noun(noun=noun, gender_token=gender_token)
        replace_article(article=article, gender_token=gender_token)
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
            print(matches)
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



# typical noun endings refering to persons, male
# {"er", "or", "ent", "tekt", "eur",


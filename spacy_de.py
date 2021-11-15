from pathlib import Path

import spacy
from spacy.matcher import Matcher

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
#By default, the matcher will only return the matches and not do anything else, like merge entities or assign labels. This is all up to you and can be defined individually for each pattern, by passing in a callback function as the on_match argument on add(). This is useful, because it lets you write entirely custom and pattern-specific logic. For example, you might want to merge some patterns into one token, while adding entity labels for other pattern types. You shouldn’t have to create different matchers for each of those processes.

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

    infile = DIR / "german_annotated.txt"
    outfile = DIR / "german_annotated_inclusiv_spacy.txt"
    clean_annotated_file(infile=(DIR / "german_annotated1.txt"), outfile=infile)
    with open(infile, "r", encoding="utf8") as inn:
        for line in inn:
            print(line)
            doc = nlp(line)
            print(bool(doc.ents))
            if not bool(doc.ents):
                exit()
            for token in doc:
                print(
                    token.text,
                    token.morph,
                    # token.ent_type_,
                    # token.ent_iob_,
                    # token.lemma_,
                    # token.pos_,
                    # token.tag_,
                    # token.dep_,
                    # token.is_punct
                )

# start writing rules
# us .sent to get sentence span of matched tokens
# or .doc if only sentences processed at once
# an article followed by an adjective followed by a noun


# personal pronoun, no entity in sentence, no object, not referring to a noun not describing a person
    pp = [{"TAG": "PPR"}, {"MORPH": {"IS_SUBSET": ["Number=Sing", "Gender=Masc", "Gender=Fem", "Case=Nom"]}}]
    #bool(doc.ents) == False or # pronoun doesn t refer to entity
# possesive pronoun, third person
ar_ad_nn = [{"TAG": "ART"}, {"POS": "ADV", "OP": "*"}, {"TAG": "ADJA", "OP": "*"}, {"POS": "NOUN"}]

# tokens where gender inclusive shall not be used
# {"Mann", "Frau",
# typical noun endings refering to persons, male
# {"er", "or", "ent", "tekt", "eur",


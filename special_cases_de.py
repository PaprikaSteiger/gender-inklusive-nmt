gendered_no_replacement = [
    "Mann",
    "Herr",
    "Frau",
]
# tokens where gender inclusive shall not be used
no_replacment = [
    "Mutter",
    "Vater",
    "Computer",
    "Roboter",
    "Eimer", #And komposita
    "Fühler",
    "Körper",
    "Gottesanbeterin",
    "Völker", # shouldn't happen anyway as the lemma is volk
    "Fehler",
    "Hunger",
    "20er", #TODO: in general numbers+er
    "Zweiter",
    "Dritter", # ...
    "Leiter", # only if die Leiter
    "Butter",
    "Papier",
    "Scanner",
    "Fieber",
    "Gelächter",
    "Acker",
    #"Wikinger", TODO: ask an expert? For me it's referring to a population/culture not just the male ones
    #"Bürger", TODO: ask an expert?
    #"Boomer", TODO: ask an expert?
    #"Barde", TODO: ask an expert?
    "Meter",
    "Kilometer",
    "Wasser",
    "Muster",
    "Opfer",
    "Lager",
    "Charakter",
    "September",
    "Oktober",
    "November",
    "Dezember",
    "Sommer",
    "Winter",
    "Mauer",
    "Wasser",
    "Gletscher",
    "Wunder",
    "Fenster",
    "Gelder",
    "Gelächter",
    "Becher",
    "Manier",

    # - ending in
    "Medizin",
    "Benzin",

    # - ending ent
    "Moment",

    # - ending or
    "Traktor",


]

# important noun endings
noun_lemma_endings = {
    ("er", "in"): 1, # sg ers:in, just dative: ern:innen
    ("ent", "entin"): 3, # nom sg ent:in, sonst sg alles enten:in, plural enten:innen
    ("at", "atin"): 3, # wie ent
    ("te", "tin"): 3, # wie ent
    ("or", "orin"): 2, # just genitive ors:in, plural always en:innen
    ("eur", "euse"): 4, #Coiffeur
    ("eur","eurin"): 4,
    ("tekt", "tektin"): 3, # wie ent
    #("ender", "enderin"): 1, # wie (t)or
    #"se", "sin" # Virtuose, are there other words with ending e - in?
    # TODO: what to do with ein KriminelleR, but der KriminellE, it follows the strong, mixed, weak declination pattern
    # TODO: adjectives/pronouns used as noun follow adjective declination e.g. Kriminelle / Dritte vs. ein KriminellEr
    # TODO: for all adjectives used as noun, e.g. also ein ErwachseneR der Erwachsene
}


special_nouns = [
    "Freund", "Freundin",
    "Arzt", "Ärztin",
    "Frisör", # "Friseurin",
    "Chirurg", "Chirurgin"
]

irregular_replacements = {
    "jedermann": "jeder", # shall be replaced bei jeder
    "Wunderknabe": "Wunderkind",

}
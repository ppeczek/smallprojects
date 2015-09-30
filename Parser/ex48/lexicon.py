directions = ("north", "south", "east", "west", "down", "up", "left", "right", "back")
verbs = ("go", "stop", "kill", "eat")
stops = ("the", "in", "of", "from", "at", "it")
nouns = ("door", "bear", "princess", "cabinet")
    
def scan (sentence):
    lexicon = []
    sentence = sentence.lower()
    words = sentence.split()
    for word in words:
        if direction_test(word):
            lexicon.append(direction_test(word))
            continue
        if verb_test(word):
            lexicon.append(verb_test(word))
            continue
        if stop_test(word):
            lexicon.append(stop_test(word))
            continue
        if noun_test(word):
            lexicon.append(noun_test(word))
            continue
        try:
            lexicon.append(("number", int(word)))
            continue
        except:
            lexicon.append(("error", word))
    return lexicon

def direction_test(word):
    if word in directions:
        return ("direction", word)
    return None
            
def verb_test(word):
    if word in verbs:
        return ("verb", word)
    return None

def stop_test(word):
    if word in stops:
        return ("stop", word)
    return None

def noun_test(word):
    if word in nouns:
        return ("noun", word)
    return None
import random

# Dictionnaire de N-grammes freequemment concernes par des erreurs en OCR et leurs associations
unigram_mistakes = {
    'I': 'l', 'o': 'a', 'e': 'c', 'a': 'o', 't': 'f',
    'l': 'I', 'b': 'h', 'd': 'cl', 'm': 'n', 'n': 'm'
}

bigram_mistakes = {
    'cl': 'd', 'rn': 'm', 'oi': 'oi', 'ue': 've', 're': 'ne',
    'ne': 're', 've': 'ue', 'oi': 'oi', 'll': 'tl', 'tt': 'lt'
}

# Fonction permettant d'intorduire UNE erreur de type aleatoire a une position aleatoire dans un texte
def introduce_mistake(text):

    # Choix du type d'erreur
    mistake_type = random.choice(['remove_char', 'add_char', 'mistake_char', 'remove_space',
                                  'add_space', 'newline', 'punctuation', 'capital_letter'])
    
    if mistake_type == 'remove_char':
        if len(text) > 1: #On fait attention a avoir de quoi supprimer
            pos = random.randint(0, len(text) - 1)
            text = text[:pos] + text[pos + 1:]
            
    elif mistake_type == 'add_char':
        pos = random.randint(0, len(text) - 1)
        char = random.choice(list(unigram_mistakes.keys()))
        text = text[:pos] + char + text[pos:]
    
    elif mistake_type == 'mistake_char':
        altered = False
        i = 0
        while not altered and i < 100: #Tant qu'on a pas d'association on recommence (max 100x)
            pos = random.randint(0, len(text) - 1)
            i += 1
            if text[pos] in unigram_mistakes or (pos < len(text) - 1 and text[pos:pos+2] in bigram_mistakes):
                altered = True

        if text[pos:pos+2] in bigram_mistakes: #Si on a un bigramme on choisit un bigramme un premier
            text = text[:pos] + bigram_mistakes[text[pos:pos+2]] + text[pos+2:]
        elif text[pos] in unigram_mistakes: #Sinon on prend une lettre
            text = text[:pos] + unigram_mistakes[text[pos]] + text[pos+1:]
            
    
    elif mistake_type == 'remove_space':
        spaces = [pos for pos, char in enumerate(text) if char == ' ']
        if spaces:
            pos = random.choice(spaces)
            text = text[:pos] + text[pos + 1:]
    
    elif mistake_type == 'add_space':
        pos = random.randint(0, len(text) - 1)
        text = text[:pos] + ' ' + text[pos:]
    
    elif mistake_type == 'newline':
        pos = random.randint(0, len(text) - 1)
        text = text[:pos] + '\n' + text[pos:]
    
    elif mistake_type == 'punctuation':
        punctuations = ['.', ',', ';', ':', '!', '?']
        pos = random.randint(0, len(text) - 1)
        text = text[:pos] + random.choice(punctuations) + text[pos + 1:]
    
    elif mistake_type == 'capital_letter':
        pos = random.randint(0, len(text) - 1)
        if text[pos].isalpha():
            text = text[:pos] + text[pos].swapcase() + text[pos+1:]
    
    return text

# Introduction de N erreurs dans un texte
def alter_text(golden_text, n_mistakes):
    for _ in range(n_mistakes):
        golden_text = introduce_mistake(golden_text)
    return golden_text

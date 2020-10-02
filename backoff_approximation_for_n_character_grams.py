import re, nltk
# nltk.download('brown')
from nltk.corpus import brown

print("Loading Brown Corpus...")

tokens = []
for genre in brown.categories():
    genre_words = brown.words(categories = genre)
    tokens.extend(genre_words)

print("Brown Corpus loaded successfully!!")

token = input("Enter a word to generate probabilistic counts: ")
backoff = int(input("Enter the backoff size (Must be compulsorily lesser than length of the input word): "))

def generate_chain_rule_probability_approximation(word, backoff = 0):
    tokens_string = ' '.join(tokens)
    prev_grams_count = len(tokens)
    characters = list(word)
    probability = 1
    backoff_counter = 0
    pattern = None
    for i in range(len(characters)):
        if backoff == 0:
            pattern = re.compile('{}'.format(''.join(characters[0:i + 1])))
            grams_count = len(pattern.findall(tokens_string))
        else:
            if backoff_counter <= backoff:
                grams = [x for x in tokens if x.startswith(''.join(characters[0:backoff_counter + 1]))]
                grams_count = len(grams)
            else:
                backoff_limit = min(backoff_counter, backoff)
                start = i - backoff_limit
                search_pattern = re.compile(r'\s?\w{{{0}}}{1}'.format(start, ''.join(characters[start: i + 1])))
                grams = [token for token in tokens if search_pattern.match(token) is not None]
                # print('True Grams : {}'.format(grams))
                grams_count = len(grams)
                # print(grams_count)
                prev_grams_pattern = re.compile(r'\s?\w{{{0}}}{1}'.format(start, ''.join(characters[start: i])))
                prev_grams = [token for token in tokens if prev_grams_pattern.match(token) is not None]
                # print('Previous Grams : {}'.format(prev_grams))
                prev_grams_count = len(prev_grams)
                # print(prev_grams_count)

            backoff_counter += 1
        probability *= (grams_count / prev_grams_count)

        print('Iteration {}:  {} / {}'.format(i + 1, grams_count, prev_grams_count))
        prev_grams_count = grams_count
        
    return probability

def generate_counts(word, backoff):
    non_backoff_approximation = generate_chain_rule_probability_approximation(word)
    print('Chain Rule Probability Approximation without Backoff = {}'.format(non_backoff_approximation))
    backoff_approximation = generate_chain_rule_probability_approximation(word, backoff)
    print('Chain Rule Probability Approximation (when Backoff = {}) = {}'.format(backoff, backoff_approximation))
    actual_probability = tokens.count(word) / len(tokens)
    print(tokens.count(word))
    print('Actual Probability = {}'.format(actual_probability))
    
generate_counts(token, backoff)
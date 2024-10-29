import itertools
import random
import hashlib
import base64
import json
from collections import defaultdict
import string

COMMON_PASSWORDS = ['123456', 'password', 'qwerty', 'abc123']
COMMON_PATTERNS = ['{0}123', '{0}2023', '123{0}', '{0}!', '{0}@']

def apply_phonetic_substitutions(word):
    subs = {'s': 'z', 'ph': 'f', 'a': '4', 'e': '3', 'i': '1', 'o': '0'}
    for original, substitute in subs.items():
        word = word.replace(original, substitute)
    return word

def shuffle_characters(word):
    return ''.join(random.sample(word, len(word)))

def insert_symbols(word, symbols):
    positions = range(len(word) + 1)
    position = random.choice(positions)
    symbol = random.choice(symbols)
    return word[:position] + symbol + word[position:]

def generate_markov_chain_words(base_wordlist, length=8):
    markov_chain = defaultdict(list)
    for word in base_wordlist:
        for i in range(len(word) - 1):
            markov_chain[word[i]].append(word[i + 1])

    generated_words = set()
    while len(generated_words) < 100:
        word = random.choice(list(base_wordlist))
        new_word = word[0]
        while len(new_word) < length:
            next_char = random.choice(markov_chain.get(new_word[-1], string.ascii_lowercase))
            new_word += next_char
        generated_words.add(new_word)

    return generated_words

def combine_data(data, separators=None, use_years=None, prefix=None, suffix=None, custom_patterns=None):
    base_wordlist = set()
    for entry in data:
        base_wordlist.add(entry)

        if separators:
            for sep in separators:
                base_wordlist.add(f'{prefix}{sep}{entry}{suffix}' if prefix or suffix else f'{entry}')

        if use_years:
            for year in use_years:
                base_wordlist.add(f'{entry}{year}')
                if separators:
                    for sep in separators:
                        base_wordlist.add(f'{entry}{sep}{year}')

        if custom_patterns:
            for pattern in custom_patterns:
                base_wordlist.add(pattern.replace("[name]", entry).replace("[year]", str(random.choice(use_years or []))))

    return base_wordlist

def apply_mutations(wordlist, advanced=False):
    mutated_list = set()
    for word in wordlist:
        leetspeak_word = apply_phonetic_substitutions(word)
        mutated_list.add(leetspeak_word)
        if advanced:
            mutated_list.add(word[::-1])
            mutated_list.add(shuffle_characters(word))
    return wordlist.union(mutated_list)

def generate_wordlist(data, output_file, mutations=False, advanced_mutations=False, min_length=0, max_length=0, separators=None, years=None, prefix=None, suffix=None, predefined=False, size_limit=None, number_range=None, custom_patterns=None, smart_expand=False, padding=None, markov=False, language_translations=None, exclude=None):
    base_wordlist = combine_data(data, separators=separators, use_years=years, prefix=prefix, suffix=suffix, custom_patterns=custom_patterns)

    if mutations:
        base_wordlist = apply_mutations(base_wordlist, advanced=advanced_mutations)

    if predefined:
        base_wordlist.update(COMMON_PASSWORDS)
        for word in data:
            for pattern in COMMON_PATTERNS:
                base_wordlist.add(pattern.format(word))

    if smart_expand:
        expanded_list = set()
        for word in base_wordlist:
            expanded_list.add(word + random.choice(['!', '@', '#', '$', '%']))
            expanded_list.add(word + str(random.randint(10, 99)))
        base_wordlist.update(expanded_list)

    if number_range:
        start, end = number_range
        for word in data:
            for num in range(start, end + 1):
                base_wordlist.add(word + str(num))
                base_wordlist.add(str(num) + word)

    if padding:
        for word in list(base_wordlist):
            base_wordlist.add(padding + word)
            base_wordlist.add(word + padding)

    if markov:
        base_wordlist.update(generate_markov_chain_words(base_wordlist))

    if language_translations:
        for word in list(base_wordlist):
            for translation in language_translations:
                base_wordlist.add(translation)

    if exclude:
        base_wordlist = {word for word in base_wordlist if word not in exclude}

    if min_length > 0 or max_length > 0:
        base_wordlist = {word for word in base_wordlist if (min_length <= len(word) <= max_length)}

    if size_limit and len(base_wordlist) > size_limit:
        base_wordlist = set(random.sample(base_wordlist, size_limit))

    return base_wordlist

def encode_wordlist(wordlist, encoding_type):
    encoded_list = set()
    for word in wordlist:
        if encoding_type == 'base64':
            encoded_list.add(base64.b64encode(word.encode()).decode())
        elif encoding_type == 'md5':
            encoded_list.add(hashlib.md5(word.encode()).hexdigest())
        elif encoding_type == 'sha256':
            encoded_list.add(hashlib.sha256(word.encode()).hexdigest())
    return encoded_list

def export_wordlist(wordlist, output_file, format_type):
    if format_type == 'txt':
        with open(output_file, 'w') as f:
            for word in wordlist:
                f.write(word + "\n")
    elif format_type == 'csv':
        with open(output_file, 'w') as f:
            f.write(",".join(wordlist))
    elif format_type == 'json':
        with open(output_file, 'w') as f:
            json.dump(list(wordlist), f)

def get_user_input():
    print("Welcome to the Advanced Personalized Wordlist Generator!")

    data = []
    data.append(input("Enter name(s) of the target (comma separated): ").strip().split(','))
    data.append(input("Enter birthdate of the target (yyyy-mm-dd, optional): ").strip())
    data.append(input("Enter pet's name(s) of the target (comma separated, optional): ").strip().split(','))

    separators = input("Do you want to use separators (like '-', '_')? (y/n): ").strip().lower() == 'y'
    separators = input("Enter separators (comma separated, e.g., '-', '_', optional): ").strip().split(',') if separators else None

    use_years = input("Do you want to use years in the wordlist (e.g., 1990, 2023)? (y/n): ").strip().lower() == 'y'
    years = input("Enter years to include (comma separated, e.g., 1990,2023, optional): ").strip().split(',') if use_years else None

    prefix = input("Enter a custom prefix (optional): ").strip() or None
    suffix = input("Enter a custom suffix (optional): ").strip() or None

    custom_patterns = input("Do you want to use custom patterns (e.g., '[name][year]', optional)? (y/n): ").strip().lower() == 'y'
    custom_patterns = input("Enter any custom patterns (e.g., '[name][year]', optional): ").strip().split(',') if custom_patterns else None

    use_mutations = input("Do you want to apply common mutations (leetspeak, capitalization)? (y/n): ").strip().lower() == 'y'
    advanced_mutations = input("Do you want to apply advanced mutations (reverse, case-leetspeak combos)? (y/n): ").strip().lower() == 'y' if use_mutations else False

    use_predefined = input("Do you want to include predefined common passwords and patterns? (y/n): ").strip().lower() == 'y'

    min_length = int(input("Enter the minimum word length (enter 0 for no limit): ").strip() or 0)
    max_length = int(input("Enter the maximum word length (enter 0 for no limit): ").strip() or 0)

    size_limit = int(input("Enter a size limit for the wordlist (enter 0 for no limit): ").strip() or 0)

    number_range = tuple(map(int, input("Enter a number range to append (e.g., '100 999', optional): ").strip().split())) if input("Do you want to include a number range (e.g., 100-999)? (y/n): ").strip().lower() == 'y' else None

    smart_expand = input("Do you want to use smart wordlist expansion (add symbols, random numbers)? (y/n): ").strip().lower() == 'y'

    encoding_type = input("Do you want to encode the wordlist (base64, md5, sha256)? (leave blank for no encoding): ").strip().lower() or None

    format_type = input("In what format would you like to export the wordlist (txt, csv, json)? ").strip().lower() or "txt"

    output_file = input("Enter output filename (default: wordlist.txt): ").strip() or "wordlist.txt"

    padding = input("Enter padding to add to the start or end of each entry (optional): ").strip() or None

    markov = input("Do you want to use Markov chain-based word generation? (y/n): ").strip().lower() == 'y'

    language_translations = input("Enter any additional translations for the wordlist (comma separated, optional): ").strip().split(',') if input("Do you want to use translations? (y/n): ").strip().lower() == 'y' else None

    exclude = input("Enter any words to exclude from the wordlist (comma separated, optional): ").strip().split(',') if input("Do you want to exclude certain words? (y/n): ").strip().lower() == 'y' else None

    return data, separators, years, prefix, suffix, custom_patterns, use_mutations, advanced_mutations, use_predefined, min_length, max_length, size_limit, number_range, smart_expand, encoding_type, format_type, output_file, padding, markov, language_translations, exclude

def main():
    data, separators, years, prefix, suffix, custom_patterns, use_mutations, advanced_mutations, use_predefined, min_length, max_length, size_limit, number_range, smart_expand, encoding_type, format_type, output_file, padding, markov, language_translations, exclude = get_user_input()

    data = [item for sublist in data for item in sublist if item]

    if not data:
        print("No data provided. Please provide at least one form of target information.")
        return

    wordlist = generate_wordlist(
        data=data, 
        output_file=output_file, 
        mutations=use_mutations, 
        advanced_mutations=advanced_mutations,
        min_length=min_length, 
        max_length=max_length, 
        separators=separators, 
        years=years, 
        prefix=prefix, 
        suffix=suffix, 
        predefined=use_predefined, 
        size_limit=size_limit,
        number_range=number_range,
        custom_patterns=custom_patterns,
        smart_expand=smart_expand,
        padding=padding,
        markov=markov,
        language_translations=language_translations,
        exclude=exclude
    )

    if encoding_type:
        wordlist = encode_wordlist(wordlist, encoding_type)

    export_wordlist(wordlist, output_file, format_type)

if __name__ == "__main__":
    main()

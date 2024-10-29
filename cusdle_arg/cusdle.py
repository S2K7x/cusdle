# ex: python word.py -n "john,doe" -b "1985-08-15" -p "fluffy,whiskers" --prefix "user_" --suffix "_2024" --mutations --output "wordlist.txt"
# ex : python cliword.py -n "alice,bob" --patterns "[name][year]" --encoding md5 --format json --output "wordlist.json"
# ex : python cliword.py -n "admin" --number-range "100 999" --exclude "password,123456" --size-limit 1000 --output "filtered_wordlist.txt"

import argparse
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

def parse_args():
    parser = argparse.ArgumentParser(description="Generate a personalized wordlist with various options.")
    
    parser.add_argument('-n', '--names', type=str, required=True, help="Comma-separated names of the target.")
    parser.add_argument('-b', '--birthdate', type=str, help="Birthdate of the target (yyyy-mm-dd).")
    parser.add_argument('-p', '--pets', type=str, help="Comma-separated names of pets of the target.")
    parser.add_argument('-s', '--separators', type=str, help="Comma-separated list of separators to use (e.g., '-', '_').")
    parser.add_argument('-y', '--years', type=str, help="Comma-separated list of years to include (e.g., 1990,2023).")
    parser.add_argument('--prefix', type=str, help="Custom prefix to add to each entry.")
    parser.add_argument('--suffix', type=str, help="Custom suffix to add to each entry.")
    parser.add_argument('--patterns', type=str, help="Comma-separated list of custom patterns (e.g., '[name][year]').")
    parser.add_argument('--mutations', action='store_true', help="Apply common mutations (leetspeak, capitalization).")
    parser.add_argument('--advanced-mutations', action='store_true', help="Apply advanced mutations (reverse, case-leetspeak combos).")
    parser.add_argument('--predefined', action='store_true', help="Include predefined common passwords and patterns.")
    parser.add_argument('--min-length', type=int, default=0, help="Minimum word length (default: 0 for no limit).")
    parser.add_argument('--max-length', type=int, default=0, help="Maximum word length (default: 0 for no limit).")
    parser.add_argument('--size-limit', type=int, default=0, help="Size limit for the wordlist (default: 0 for no limit).")
    parser.add_argument('--number-range', type=str, help="Number range to append (e.g., '100 999').")
    parser.add_argument('--smart-expand', action='store_true', help="Use smart wordlist expansion (add symbols, random numbers).")
    parser.add_argument('--padding', type=str, help="Padding to add to the start or end of each entry.")
    parser.add_argument('--markov', action='store_true', help="Use Markov chain-based word generation.")
    parser.add_argument('--translations', type=str, help="Comma-separated list of additional translations for the wordlist.")
    parser.add_argument('--exclude', type=str, help="Comma-separated list of words to exclude from the wordlist.")
    parser.add_argument('--encoding', type=str, choices=['base64', 'md5', 'sha256'], help="Encode the wordlist (base64, md5, sha256).")
    parser.add_argument('--format', type=str, choices=['txt', 'csv', 'json'], default='txt', help="Export format (txt, csv, json).")
    parser.add_argument('--output', type=str, default='wordlist.txt', help="Output filename (default: wordlist.txt).")
    
    return parser.parse_args()

def main():
    args = parse_args()

    data = args.names.split(',')
    if args.birthdate:
        data.append(args.birthdate)
    if args.pets:
        data.extend(args.pets.split(','))

    separators = args.separators.split(',') if args.separators else None
    years = args.years.split(',') if args.years else None
    custom_patterns = args.patterns.split(',') if args.patterns else None
    number_range = tuple(map(int, args.number_range.split())) if args.number_range else None
    language_translations = args.translations.split(',') if args.translations else None
    exclude = args.exclude.split(',') if args.exclude else None

    wordlist = generate_wordlist(
        data=data,
        output_file=args.output,
        mutations=args.mutations,
        advanced_mutations=args.advanced_mutations,
        min_length=args.min_length,
        max_length=args.max_length,
        separators=separators,
        years=years,
        prefix=args.prefix,
        suffix=args.suffix,
        predefined=args.predefined,
        size_limit=args.size_limit,
        number_range=number_range,
        custom_patterns=custom_patterns,
        smart_expand=args.smart_expand,
        padding=args.padding,
        markov=args.markov,
        language_translations=language_translations,
        exclude=exclude
    )

    if args.encoding:
        wordlist = encode_wordlist(wordlist, args.encoding)

    export_wordlist(wordlist, args.output, args.format)

if __name__ == "__main__":
    main()

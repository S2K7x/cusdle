# cusdle.py - A Powerful Wordlist Generator Tool

## Overview
`cusdle.py` is a versatile and feature-rich wordlist generator designed to help security professionals and enthusiasts create personalized wordlists for various use cases. It supports a wide range of options, including name-based generation, birthdate inclusion, pet names, separators, years, custom patterns, mutations, advanced mutations, predefined common passwords, word length limits, size limits, number ranges, smart expansion, padding, Markov chain-based word generation, language translations, exclusion of specific words, encoding (base64, md5, sha256), and multiple output formats (txt, csv, json).

## Features
- **Name-based Generation**: Generate words based on target names.
- **Birthdate Inclusion**: Include birthdate in the wordlist.
- **Pet Names**: Include pet names in the wordlist.
- **Separators**: Use custom separators between words.
- **Years**: Include specific years in the wordlist.
- **Custom Patterns**: Use custom patterns to generate words.
- **Mutations**: Apply common mutations like leetspeak and capitalization.
- **Advanced Mutations**: Apply advanced mutations like reverse and case-leetspeak combos.
- **Predefined Common Passwords**: Include predefined common passwords and patterns.
- **Word Length Limits**: Set minimum and maximum word lengths.
- **Size Limits**: Limit the size of the wordlist.
- **Number Ranges**: Append numbers within a specified range.
- **Smart Expansion**: Use smart wordlist expansion by adding symbols and random numbers.
- **Padding**: Add padding to the start or end of each entry.
- **Markov Chain-based Word Generation**: Use Markov chain-based word generation.
- **Language Translations**: Include additional translations for the wordlist.
- **Exclusion**: Exclude specific words from the wordlist.
- **Encoding**: Encode the wordlist using base64, md5, or sha256.
- **Output Formats**: Export the wordlist in txt, csv, or json format.

## Usage
```bash
python cusdle.py -n "john,doe" -b "1985-08-15" -p "fluffy,whiskers" --prefix "user_" --suffix "_2024" --mutations --output "wordlist.txt"
```

```bash
python cusdle.py -n "alice,bob" --patterns "[name][year]" --encoding md5 --format json --output "wordlist.json"
```

```bash
python cusdle.py -n "admin" --number-range "100 999" --exclude "password,123456" --size-limit 1000 --output "filtered_wordlist.txt"
```

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/S2K7/cusdle.git
    cd cusdle
    ```

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Running the Tool
1. Open a terminal and navigate to the project directory.
2. Run the tool with the desired options:
    ```bash
    python cusdle.py -n "john,doe" -b "1985-08-15" -p "fluffy,whiskers" --prefix "user_" --suffix "_2024" --mutations --output "wordlist.txt"
    ```

## Contributing
Contributions are welcome! Please open an issue or submit a pull request.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
```

This README file provides a comprehensive overview of the `cusdle.py` tool, including its features, usage examples, installation instructions, and contribution guidelines. It is designed to be informative and user-friendly, making it easy for users to understand and utilize the tool effectively.

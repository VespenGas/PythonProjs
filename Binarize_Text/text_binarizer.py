#!/usr/bin/env python3
import pathlib
import re
import itertools


def preprocess(input_text):
    if isinstance(input_text, str):
        input_text = list(input_text.split(' '))
    elif isinstance(input_text, list):
        pass
    else:
        raise SystemExit(1)
    all_words = str(' '.join(input_text)).replace("\n", '').casefold()
    clean = re.sub(r"""
                   [,.;@#?!&$—'"] + \ *""",
                   " ",          
                   all_words,
                   flags=re.VERBOSE)
    all_words = sorted(list(set(list(clean.split(' ')))))
    out_text = list(itertools.filterfalse(lambda x: x == '', all_words))
    return out_text
def save_report(*, binary, words):
    with open('result.csv', 'w') as file:
        file.write(str(words)[1:-1] +'\n' + str(binary)[1:-1])
    return 0
def main():

    textfiles = list(pathlib.Path(".").glob("*.txt"))
    all_words = []
    for textfile in textfiles:
        with open(textfile, 'r') as f:
            all_words.extend(f)
    vocab = preprocess(all_words)
    
    check_text = "text1.txt"
    
    with open(check_text, 'r') as text:
        check_text = text.read()
    check_text = preprocess(check_text)
    binary_repr = [1 if word in check_text else 0 for word in vocab]
    save_report(binary = binary_repr, words = vocab)
    raise SystemExit(0)
if __name__ == '__main__':
    main()

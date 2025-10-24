# Imports
import hashlib
import sys
import pyfiglet
import os
from prompt_toolkit import prompt
from prompt_toolkit.completion import PathCompleter, Completion
from prompt_toolkit.shortcuts import CompleteStyle
from prompt_toolkit.formatted_text import HTML

# Banner
ascii_banner = pyfiglet.figlet_format("crackatoa")
print(ascii_banner)
print("Available Algorithms: MD5 | SHA1 | SHA224 | SHA256\n")

# Bash Completer with colors

class BashPathCompleter(PathCompleter):
    #Path Completer that colors directories blue, files white.
    def get_completions(self, document, complete_event):
        word = document.get_word_before_cursor()
        for completion in super().get_completions(document, complete_event):
            display_text = completion.text
            if os.path.isdir(completion.text):
                display_text = f"<ansiblue>{completion.text}</ansiblue>"
            yield Completion(
                completion.text,
                start_position=completion.start_position,
                display=HTML(display_text)
            )

path_completer = BashPathCompleter(expanduser=True)

# User inputs
hash_type = input("Select Hash Type: ").strip().upper()
wordlist_location = prompt(
    "Enter path to wordlist: ",
    completer=path_completer,
    complete_while_typing=False,
    complete_style=CompleteStyle.MULTI_COLUMN
)
hash_to_crack = input("Enter Hash: ").strip()

# Validate inputs
if hash_type not in ("MD5", "SHA1", "SHA224", "SHA256"):
    print("Please choose a valid algorithm: MD5 | SHA1 | SHA224 | SHA256")
    sys.exit(1)

if not os.path.isfile(wordlist_location):
    print(f"Error: File '{wordlist_location}' not found.")
    sys.exit(1)

# Hash functions
hash_funcs = {
    "MD5": hashlib.md5,
    "SHA1": hashlib.sha1,
    "SHA224": hashlib.sha224,
    "SHA256": hashlib.sha256
}

hash_func = hash_funcs[hash_type]

# Wordlist processing with progress
found = False

with open(wordlist_location, "r", encoding="utf-8", errors="ignore") as f:
    total_lines = sum(1 for _ in f)

with open(wordlist_location, "r", encoding="utf-8", errors="ignore") as f:
    for i, word in enumerate(f, 1):
        word = word.strip()
        hashed_word = hash_func(word.encode("utf-8")).hexdigest()
        if hashed_word == hash_to_crack:
            print(f"\033[1;32m[+] HASH FOUND: {word}\033[0m\n")
            found = True
            break

        # Progress every 1000 lines
        if i % 1000 == 0 or i == total_lines:
            print(f"Progress: {i}/{total_lines} words ({(i/total_lines)*100:.2f}%)", end="\r")

if not found:
    print("\n\033[1;31m[-] No match found in the wordlist.\033[0m")
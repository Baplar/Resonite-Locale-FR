#!/usr/bin/env python3

import json

LANGUAGE_NAMES = {
    "cs": "Czech",
    "de": "German",
    "en-gb": "English (United Kingdom)",
    "eo": "Esperanto",
    "es": "Spanish",
    "et": "Estonian",
    "fi": "Finnish",
    "fr": "French",
    "hu": "Hungarian",
    "is": "Icelandic",
    "ja": "Japanese",
    "ko": "Korean",
    "mn": "Mongolian",
    "nl": "Dutch",
    "no": "Norwegian",
    "pl": "Polish",
    "pt-br": "Portuguese (Brazil)",
    "ru": "Russian",
    "sv": "Swedish",
    "th": "Thai",
    "tr": "Turkish",
    "ua": "ua",
    "uk": "Ukrainian",
    "zh-cn": "Chinese (Simplified, Mainland China)",
    "zh-tw": "Chinese (Traditional, Taiwan)",
}

class MissingChecker:
    def __init__(self, en, lang, out):
        self.out = out
        with open(en, 'r', encoding="utf8") as en_file:
            self.en = json.load(en_file)
        with open(lang, 'r', encoding="utf8") as lang_file:
            self.lang = json.load(lang_file)
        self.output = []
        
    def run(self):
        self.make_header()
        self.parse()
        self.save()
    
    def make_header(self):
        self.output.append('# Missing Keys')
        self.output.append('Note that this file updates only during build processes and doesn\'t necessarily reflect the current state.')
        self.output.append('')
        localeCode = self.lang['localeCode']
        self.output.append(f"# {LANGUAGE_NAMES[localeCode]} [{localeCode}]")
        
    def parse(self):
        for key in self.en["messages"].keys():
            if (key not in self.lang["messages"]):
                self.output.append(key)            
    
    def save(self):
        with open(self.out, 'w', encoding="utf8") as out:
            out.write('\n'.join(self.output))
            out.write('\n')
        
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='This script will list the missing locale keys in a given locale.')
    parser.add_argument('--en', metavar='en_path', type=str, 
                        help='The path to the en.json locale.')
    parser.add_argument('--lang', metavar='lang_path', type=str, 
                        help='The path to the LANG.json locale to clean.')
    parser.add_argument('--out', metavar='out_path', type=str, 
                        help='The path to save the formatted list of missing translations.')

    args = parser.parse_args()
    N = MissingChecker(args.en, args.lang, args.out)
    N.run()
    print("Check complete!")

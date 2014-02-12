#!/usr/bin/python
from passphrase import password
import argparse

parser = argparse.ArgumentParser(description='Phrase => Password')
parser.add_argument("wordlist", help="text file to use as a source of patterns")
parser.add_argument("phrase", help="phrase to convert to a password")

parser.add_argument('--website', type=str, default="", help="website for which to create password")
parser.add_argument('--id', type=str, default="", help="login id on the website")
parser.add_argument('--length', type=int, default=16, help="length of password required")
parser.add_argument('--ease', type=int, default=2, help="how easy should it be", choices=[0, 1, 2, 3, 4, 5])
parser.add_argument('--case', type=int, default=2, help="1: uppercase, 2: lowercase, 3: mixed case", choices=[1,2,3])
parser.add_argument('--numeric', action='store_true', help="whether to include numbers")
parser.add_argument('--special', action='store_true', help="whether to include special characters")

args = parser.parse_args()

print(password(args.id, args.website, args.wordlist, args.phrase, args.length, args.ease+2, args.case, args.numeric, args.special))

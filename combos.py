import os
import sys
import json
import ntpath
import getpass
import itertools
import subprocess

# TODO:
# Count possible permutations
# Track tries
# Hide error text

################################################################################
# Usage                                                                        #
################################################################################

if len(sys.argv) != 2 and len(sys.argv) != 3:
	sys.stderr.write("Usage: python %s <archive> [separator]\n" % sys.argv[0])
	sys.stderr.write("   Ex: python %s test.7z '|'\n" % sys.argv[0])
	sys.exit(1)

################################################################################
# Global definitions                                                           #
################################################################################

archive = sys.argv[1]
#separator = sys.argv[2]
separator = " "

################################################################################
# Function definitions                                                         #
################################################################################

def prompt_words():
	words = []

	word = True
	while word:
		word = getpass.getpass("Enter word (empty line to stop): ")
		if word:
			words.append(word)
	
	print "Read %d words.\n" % len(words)
	
	return words

def enumerate_combos():
	combos = [ ]

	words = prompt_words()
	for x in range(0, len(words)):
		for combo in itertools.combinations(words, x + 1):
			for perm in itertools.permutations(list(combo)):
				combos.append(separator.join(perm))

	print "Enumerated %d combinations.\n" % len(combos)
	
	return combos

def attempt_combos(combos):
	attempt = 0
	FNULL = open(os.devnull, 'w')
	for combo in combos:
		attempt += 1
		if attempt % 25 == 0:
			print "Attempt %d" % attempt
		command = [ "7z", "t", "-p%s" % combo, archive ]
		rc = subprocess.call(command, stdout=FNULL, stderr=FNULL)
		if not rc:
			print "Success with combo '%s'." % combo
			return

	print "No luck. Tried %d combinations." % len(combos)

def dump_combos(combos):
    print "Dumping combos...\n"
    fout = open("combos.txt", "w")
    for combo in combos:
        fout.write(combo + "\n")

################################################################################
# Main                                                                         #
################################################################################

combos = enumerate_combos()
dump_combos(combos)
attempt_combos(combos)

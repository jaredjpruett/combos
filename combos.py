import os
import sys
import json
import ntpath
import getpass
import itertools
import subprocess

################################################################################
# Usage                                                                        #
################################################################################

if len(sys.argv) != 3:
	sys.stderr.write("Usage: python %s <archive> <separator>\n" % sys.argv[0])
	sys.stderr.write("   Ex: python %s test.7z '|'\n")
	sys.exit(1)

################################################################################
# Global definitions                                                           #
################################################################################

archive = sys.argv[1]
separator = sys.argv[2]

################################################################################
# Function definitions                                                         #
################################################################################

def prompt_words():
	words = []

	word = True
	while word:
		word = getpass.getpass("Enter word (empty line to stop): ")
		if word:
			if word == getpass.getpass("Confirm word: "):
				words.append(word)
			else:
				sys.stderr.write("Words did not match.\n")
			print
	
	print "\nRead %d words.\n" % len(words)
	
	return words

def enumerate_combos():
	words = prompt_words()
	combos = []

	for x in range(0, len(words)):
		for combo in itertools.combinations(words, x + 1):
			for perm in itertools.permutations(list(combo)):
				combos.append(separator.join(perm))
	
	return combos

def attempt_combos(combos):
	FNULL = open(os.devnull, 'w')

	for combo in combos:
		command = [ "7z", "t", "-p%s" % combo, archive ]

		rc = subprocess.call(command, stdout=FNULL)

		if not rc:
			print "Success with combo '%s'." % combo
			return

	print "No luck. Tried %d combinations." % len(combos)

################################################################################
# Main                                                                         #
################################################################################

attempt_combos(enumerate_combos())

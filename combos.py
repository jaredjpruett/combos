import json
import itertools

################################################################################
# Global definitions                                                           #
################################################################################

input_file = "words"
output_file = "combos"

separator = " "

################################################################################
# Function definitions                                                         #
################################################################################

def read_words():
	return [ word.strip('\n') for word in open(input_file).readlines() ]

def enumerate_combos(words):
	combos = []

	for x in range(0, len(words)):
		for combo in itertools.combinations(words, x + 1):
			for perm in itertools.permutations(list(combo)):
				combos.append(separator.join(perm))
	
	return combos

def write_combos(combos):
	fp = open(output_file, "w")

	for combo in combos:
		fp.write("%s\n" % combo)

################################################################################
# Main                                                                         #
################################################################################

write_combos(enumerate_combos(read_words()))

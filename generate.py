import random

import numpy as np
from scipy import stats

import probconst

episodes = 2
nanogenmoseed = 727272
np.random.seed(nanogenmoseed)
random.seed(nanogenmoseed)

line_length_prob = None
sentence_length_prob = None
sentence_type_prob = None

def main():
	setup_probs()
	generate_season()


def setup_probs():
	global sentence_length_prob
	global line_length_prob
	global sentence_type_prob
	sentence_length_prob = create_probability(probconst.sentence_lengths)
	line_length_prob = create_probability(probconst.line_lengths)
	sentence_type_prob = create_probability(probconst.sentence_types)

def create_probability(d):
	return stats.rv_discrete(a=1, values = (list(d.keys()), list(d.values())))

def generate_season():
	with open('missing_season.txt', 'w') as f:
		for episode in range(1,episodes+1):
			f.write("SEASON UNKNOWN: EPISODE {ep} -- {title}\n".format(ep=episode, title=get_title()))
			f.write('=============================\n\n')
			script = generate_episode()
			f.write(script)
			f.write("\n\n=============================\n\n")


def get_title():
	return "THE PLACEHOLDER"

def generate_episode():
	word_count_goal = random.randint(3500, 3800)
	word_count = 0

	episode = ""

	last_character = 'GEORGE'

	while word_count < word_count_goal:
		character = get_next_character(last_character)
		last_character = character
		line = generate_line(character)
		episode += line + '\n'
		word_count += len(line.split(' '))

	return episode


def generate_line(character):
	goal_length = get_rand_from_prob(line_length_prob)
	line = ' '.join([generate_sentence() for i in range(goal_length)])
	return '{}: {}'.format(character, line)

def get_next_character(last_character):
	characters = ['JERRY', 'ELAINE', 'GEORGE', 'KRAMER']
	characters.remove(last_character)
	return characters[random.randint(0,len(characters)-1)]

def generate_sentence():
	possible = "The goats are going to live under the bridge forever.".split(' ')
	goal_length = get_rand_from_prob(sentence_length_prob)
	return ' '.join(possible[:goal_length]) + get_sentence_terminator()

def get_sentence_terminator():
	stype = get_rand_from_prob(sentence_type_prob)
	if stype == 1:
		return '.'
	elif stype == 2:
		return '!'
	elif stype == 3:
		return '?'
	else:
		raise Exception("Unknown sentence type: {}.".format(stype))

def get_rand_from_prob(prob):
	#
	return prob.rvs(size=1)[0]

if __name__ == "__main__":
	main()
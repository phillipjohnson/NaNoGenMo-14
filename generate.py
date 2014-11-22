import random

import numpy as np

import probconst
import sentencegenerator

episodes = 22
nanogenmoseed = 727272
np.random.seed(nanogenmoseed)
random.seed(nanogenmoseed)


def main():
    generate_season()


def generate_season():
    titles = get_titles(episodes)
    with open('missing_season.txt', 'w') as f:
        for episode in range(1, episodes + 1):
            f.write("SEASON UNKNOWN: EPISODE {ep} -- {title}\n".format(ep=episode, title=titles[episode - 1]))
            f.write('=============================\n\n')
            script = generate_episode()
            f.write(script)
            f.write("\n\n=============================\n\n")


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
    goal_length = probconst.get_line_length()
    line = ' '.join([sentencegenerator.generate() for i in range(goal_length)])
    return '{}: {}'.format(character, line)


def get_next_character(last_character):
    characters = ['JERRY', 'ELAINE', 'GEORGE', 'KRAMER']
    characters.remove(last_character)
    return characters[random.randint(0, len(characters) - 1)]


def get_titles(n):
    query = """
    match (w:Word {word:"THE"})-[:CONCORDANCE]->(w2:Word)
    where rand() < (0.01)
    return w2.word limit n;
    """

    query = query.replace("limit n", "limit " + str(n))

    title_results = sentencegenerator.execute(query)
    title_nouns = [result.values[0] for result in title_results]

    return ["THE " + noun for noun in title_nouns]


if __name__ == "__main__":
    main()
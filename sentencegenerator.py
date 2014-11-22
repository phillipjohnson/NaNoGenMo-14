from py2neo.neo4j import GraphDatabaseService, CypherQuery

import probconst

graph = GraphDatabaseService()


def execute(query):
    # print(query)
    return CypherQuery(graph, query).execute()


def cache_result(query, cache_key):
    results = execute(query)
    if results:
        total = sum(record.values[1] for record in results)
        frequencies = {}

        for record in results:
            word = record.values[0]
            count = record.values[1]
            frequencies[word] = count / total

        probconst.put_word_in_cache(cache_key, frequencies)
    else:
        #Directly cache this as having nothing
        probconst.concordance_cache[cache_key] = None


def cache_interrogatives():
    query = 'match (s:Start {type:"question"})-[:BEGINS]->(w) return w.word, count(*);'
    cache_result(query, '*QUESTION')


def cache_declaratives():
    query = 'match (s:Start {type:"statement"})-[:BEGINS]->(w) return w.word, count(*);'
    cache_result(query, '*STATEMENT')


def cache_terminal_words():
    query = 'match (w:Word)-[:TERMINATES]->(e:End) return w.word, count(*);'
    cache_result(query, '*END')


def cache_one_word_sentences():
    query = 'match (s:Start)-[:BEGINS]->(w:Word)-[:TERMINATES]->(e:End) return w.word, count(*);'
    cache_result(query, '*END')

cache_interrogatives()
cache_declaratives()
cache_terminal_words()


def try_generate():
    goal_length = probconst.get_sentence_length()
    terminator = get_sentence_terminator()

    words = []

    for i in range(goal_length):
        if i == 0:
            if terminator == '?':
                next_word = get_interrogative()
            else:
                next_word = get_declarative()
        else:
            next_word = get_or_put_concordance(words[i - 1])
            if not next_word:
                return words, terminator

        words.append(next_word)

    return words, terminator


def is_valid(words):
    last_word = words[len(words) - 1]
    if last_word not in probconst.concordance_cache['*END'].word_list:
        return False


    return True


def generate():
    valid_sentence = False
    while not valid_sentence:
        words, terminator = try_generate()
        valid_sentence = is_valid(words)

    return words_to_sentence(words, terminator)


def words_to_sentence(words, terminator):
    return ' '.join(words) + terminator


def get_sentence_terminator():
    stype = probconst.get_sentence_type()
    if stype == 1:
        return '.'
    elif stype == 2:
        return '!'
    elif stype == 3:
        return '?'
    else:
        raise Exception("Unknown sentence type: {}.".format(stype))


def get_interrogative():
    return probconst.get_concordance_from_cache('*QUESTION')


def get_declarative():
    return probconst.get_concordance_from_cache('*STATEMENT')


def get_or_put_concordance(word):
    next_word = probconst.get_concordance_from_cache(word)
    if not next_word:
        query = 'match (w1:Word {word:"' + word + '"})-[:CONCORDANCE]->(w2) return w2.word, count(*);'
        cache_result(query, word)
        return probconst.get_concordance_from_cache(word)

    return next_word
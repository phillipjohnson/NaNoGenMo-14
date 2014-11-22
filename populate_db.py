from py2neo.neo4j import GraphDatabaseService, CypherQuery
import re
import sentencegenerator

graph = GraphDatabaseService()
punctuation = list('!,\'.:"?;()[]\\/-')
splitter = re.compile('([!?\.])')

corpus_cache = []


def main():
    clear_db()

    execute("create (e:End);")
    execute("create (s:Start {type:'statement'});")
    execute("create (s:Start {type:'question'});")

    lines = []
    with open('sf_lines.txt', 'r') as f:
        lines = f.readlines()

    for line in lines:
        line = line.replace('\n', '')
        sentences = split_sentences(line)
        for sentence in sentences:
            load_sentence(sentence)

    sentencegenerator.execute("match (n)-[r]->(w:Word {word:''}) delete r;")
    sentencegenerator.execute("match (w:Word {word:''})-[r]-() delete r;")
    sentencegenerator.execute("match (w:Word {word:''}) delete w;")
    sentencegenerator.execute("match (w:Word {word:'THE'})-[r]->(e:End) delete r;")
    sentencegenerator.execute("match (w:Word {word:'I'})-[r]->(e:End) delete r;")
    sentencegenerator.execute("match (w:Word {word:'AND'})-[r]->(e:End) delete r;")


def split_sentences(line):
    split_line = re.split(splitter, line)
    sentences = [''.join([split_line[i], split_line[i + 1]]) for i in range(len(split_line) - 1) if i % 2 == 0]

    return sentences


def load_sentence(sentence):
    words = [w for w in sentence.split(' ') if w != '']
    get_or_create_word(words[0])
    if sentence[-1:] in list('.!'):
        edge = match_statement_to_word(words[0])
    elif sentence[-1:] == '?':
        edge = match_question_to_word(words[0])
    execute(edge)

    for i in range(len(words)):
        if i == len(words) - 1:
            edge = match_word_to_end(words[i])
        else:
            get_or_create_word(words[i + 1])
            edge = match_word_to_word(words[i], words[i + 1])

        execute(edge)


def match_word_to_end(word):
    word = clean_word(word)
    return "match (word:Word {word:'" + word + "'}) match (e:End) create (word)-[:TERMINATES]->(e);"


def match_word_to_word(a, b):
    a = clean_word(a)
    b = clean_word(b)
    return "match (a:Word {word: '" + a + "'}) match (b:Word {word: '" + b + "'}) create (a)-[:CONCORDANCE]->(b);"


def match_statement_to_word(word):
    word = clean_word(word)
    return "match (s:Start {type:'statement'}) match (word:Word {word: '" + word + "'}) create (s)-[:BEGINS]->(word);"


def match_question_to_word(word):
    word = clean_word(word)
    return "match (s:Start {type:'question'}) match (word:Word {word: '" + word + "'}) create (s)-[:BEGINS]->(word);"


def get_or_create_word(word):
    if word not in corpus_cache:
        word = clean_word(word)
        query = "merge (w:Word {word:'" + word + "'}) return w;"
        execute(query)
        corpus_cache.append(word)


def clear_db():
    execute("MATCH (n) OPTIONAL MATCH (n)-[r]-() DELETE n, r")


def execute(query):
    # print(query)
    return CypherQuery(graph, query).execute()


def clean_word(word):
    word = word.upper()
    for mark in punctuation:
        word = word.replace(mark, '')

    return word


if __name__ == "__main__":
    main()

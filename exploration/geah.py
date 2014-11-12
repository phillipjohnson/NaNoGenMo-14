from py2neo.neo4j import GraphDatabaseService, CypherQuery

graph = GraphDatabaseService()
punctuation = list('!,\'.:"?;()[]\\/')

def main():
	clear_db()

	execute("create (e:End);")
	execute("create (s:Start {type:'statement'});")
	execute("create (s:Start {type:'question'});")

	lines = []
	with open('geah.txt', 'r') as f:
		lines = f.readlines()

	for line in lines:
		line = line.replace('\n','')
		words = line.split(' ')

		get_or_create_word(words[0])
		if line[-1:] in list('.!'):
			edge = match_statement_to_word(words[0])
		elif line[-1:] == '?':
			edge = match_question_to_word(words[0])
		execute(edge)

		for i in range (len(words)):
			if i==len(words) - 1:
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
	word = clean_word(word)
	query = "merge (w:Word {word:'" + word + "'}) return w;"
	execute(query)

def clear_db():
	execute("MATCH (n) OPTIONAL MATCH (n)-[r]-() DELETE n, r")

def execute(query):
	#print(query)
	return CypherQuery(graph, query).execute()

def clean_word(word):
	word = word.upper()
	for mark in punctuation:
		word = word.replace(mark,'')

	return word

if __name__=="__main__":
	main()

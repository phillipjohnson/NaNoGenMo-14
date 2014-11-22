import re

with open('../sf_lines.txt', 'r') as f:
	lines = f.readlines()
	full_text = f.read()

line_lengths = {}
sentence_lengths = {}
sentence_types = {}

splitter = re.compile('[!?\.]')
for line in lines:
	line = line.replace('\n','')
	sentences = [s.strip() for s in re.split(splitter, line) if s]
	sentence_count = len(sentences)
	if line != '' and sentence_count != 0:
		line_lengths[sentence_count] = line_lengths.get(sentence_count, 0) + 1 
		for sentence in sentences:
			if sentence != '':
				word_count = len(sentence.split(' '))
				sentence_lengths[word_count] = sentence_lengths.get(word_count, 0) + 1


total = sum(sentence_lengths.values())
line_probs = {k:(v/total) for k,v in line_lengths.items()}
total = sum(line_lengths.values())
sentence_probs = {k:(v/total) for k,v in sentence_lengths.items()}

with open('../sf_lines.txt', 'r') as f:
	full_text = f.read()

sentence_types['1'] = len(re.findall('\.', full_text))
sentence_types['2'] = len(re.findall('\!', full_text))
sentence_types['3'] = len(re.findall('\?', full_text))

total = sum(sentence_types.values())
sentence_type_probs = {k:(v/total) for k,v in sentence_types.items()}

with open('../probconst_out.py','w') as f:
	f.write('line_lengths = {}\n'.format(str(line_probs)))
	f.write('sentence_lengths = {}\n'.format(str(sentence_probs)))
	f.write('sentence_types = {}\n'.format(str(sentence_type_probs)))

import re

with open('seinfeld.txt', 'r') as f:
	scripts = f.read()

pattern = re.compile('[A-Z]+:[\w ,\'"\?;:!-\.]+')
lines = re.findall(pattern, scripts)

parens = re.compile('\([\w ,\'"\?;:!-\.]+\)')
speaker = re.compile('[A-Z]+:')
spaces = re.compile(' {2,}')

with open ('sf_lines.txt', 'w') as f:
	for line in lines:
		line = line.replace('...','. ')
		line = re.sub(parens,' ', line)
		line = re.sub(speaker, '', line)
		line = re.sub(spaces,' ', line)
		line = line.strip()
		f.write(line + '\n')
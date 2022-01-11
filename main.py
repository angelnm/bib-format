from pybtex.database.input import bibtex # https://docs.pybtex.org/api/parsing.html
from collections import Counter # https://docs.python.org/3/library/collections.html
import sys

data = {
	'A': {},
	'B': {},
	'C': {},
	'D': {},
	'E': {},
	'F': {},
	'G': {},
	'H': {},
	'I': {},
	'J': {},
	'K': {},
	'L': {},
	'M': {},
	'N': {},
	'O': {},
	'P': {},
	'Q': {},
	'R': {},
	'S': {},
	'T': {},
	'U': {},
	'V': {},
	'W': {},
	'X': {},
	'Y': {},
	'Z': {},
}
separator = ''
for i in range(70):
	separator += '='

def parse_entry(k_entry, c_entry):
	c_fields = c_entry.fields
	c_person = c_entry.persons
	c_tabs = '\t\t'

	output = ""
	def check_field(field):
		nonlocal output
		if field in c_fields:
			output += c_tabs+'\t{}="{}",\n'.format(field,c_fields[field])
	def add_authors():
		nonlocal output
		output += c_tabs+'\tauthor="'
		for p in c_person['author'][:-1]:
			output += '{} and\n'.format(str(p))+c_tabs+'\t\t'
		output += '{}",\n'.format(str(c_person['author'][-1]))

	output += c_tabs+'@{0}{{{1},\n'.format(c_entry.type, k_entry)

	fields = [
		'title',
		'author',
		'month',
		'year',
		'booktitle',
		'address',
		'publisher',
		'url',
		'pages',
		'journal',
		'volume',
		'number',
		'bibsource',
		'biburl',
		'timestamp',
		'eprint',
		'archivePrefix',
		'primaryClass',
		'organization',
		'note',
		'issn',
		'keywords',
	]

	for f in fields:
		if f != 'author':
			check_field(f)
		else:
			add_authors()

	output += c_tabs+'}\n'
	return output

if __name__ == "__main__":
	in_file  = 'anthology.bib'
	out_file = 'out_anthology.bib' 
	if len(sys.argv) >= 2:
		in_file  = sys.argv[1]
	if len(sys.argv) >= 3:
		out_file = sys.argv[2]

	# Read the File
	parser = bibtex.Parser()
	bib_data = parser.parse_file(in_file)

	# Read the File
	# Letter -> Author -> Entries
	for key in bib_data.entries:
		c_entry = bib_data.entries[key]

		first_author = str(c_entry.persons['author'][0])
		first_letter = first_author[0].upper()
		first_dict   = data[first_letter]

		if first_author not in first_dict:
			first_dict[first_author] = {}

		first_dict[first_author][key] = c_entry

	# Write the File
	file = open(out_file, 'w')
	for key in data:
		file.write('%|{}\n'.format(separator))
		file.write('%| {}\n'.format(key))
		file.write('%|{}\n'.format(separator))

		for author in data[key]:
			file.write('\t%|{}\n'.format(author))
			for k_entry in data[key][author]:
				entry = data[key][author][k_entry]
				file.write(parse_entry(k_entry, entry))
		file.write('\n')
	file.close()

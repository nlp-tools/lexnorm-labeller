import nltk
import json

input_file = "data/raw_data.txt"
word_file = "data/words_en.txt"
domain_specific_words_file = "data/domain_specific_words.txt"
acronym_replacements_file = "data/acronyms.txt"
error_words_file = "output/error_words.txt"
output_file = "output/output.js"

valid_words 			= set([line.replace("\n", "") for line in open(word_file, "r")])
domain_specific_words 	= set([line.replace("\n", "") for line in open(domain_specific_words_file, "r")])

alphabet = set("abcdefghijklmnopqrstuvwxyz1234567890.'\"~!@#$%^&*(),:;|\\/ <>")
# Only words with these characters will be added.
# If the word does not contain one of these characters, it will be removed.



acronym_replacements = {}
for line in open(acronym_replacements_file, "r"):
	line = line.replace("\n", "").lower()
	if line.find("\t") > 0:
		split = line.split("\t")		
		acronym_replacements[split[0]] = split[1]
	else:
		acronym_replacements[line] = line 

#dictionary_replacements = {k: v for k, v in [line.replace("\n", "").split("\t") for line in open(acronym_replacements_file, "r")]}
#print acronym_replacements

json_data = []
error_lines = []
tid = 0

with open(input_file, "r") as data:
	for line in data:
		tid += 1
		line = ''.join([char.lower() if char.lower() in alphabet else ' ' for char in line]) # Remove chars not in alphabet (question marks, quotation marks, etc)

		tl = nltk.word_tokenize(line.lower())
		
		line_has_error = False
		error_words = []
		output = []

		# Pre-output is the code that gets rendered to the html page so you can modify it from a form
		# makes it way easier that way		
		pre_output = []
		word_index = 0
		for word in tl:
			word = word.lower()
			word_error = False
			if word not in valid_words and word.isalpha() and word not in domain_specific_words and word not in acronym_replacements:
				error_words.append(word)
				line_has_error = True
				word_error = True

			if word in acronym_replacements:
				output.append(acronym_replacements[word])
			else:
				output.append(word)
			
			if word_error:
				pre_output.append("<input data-wordindex=\"" + str(word_index) + "\" placeholder=\"" + word + "\"></input>")
			else:
				pre_output.append(word)
			word_index += 1



		obj = {"tid": tid, "index": tid, "input": tl, "pre-output": " ".join(pre_output), "output": output, "original": line}

		if line_has_error:
			error_lines.append(obj)	
			error_lines[-1]["errors"] = error_words	


		json_data.append(obj)


with open(error_words_file, "w") as output:
	for line in error_lines:
		output.write(str(line["tid"]) + ": " + "Errors: " + str(line["errors"]) + "\n")
		#print str(line["tid"]) + ": " + line["original"]
with open(output_file, "w") as output:
	output.write("data = ")
	json.dump(json_data, output)

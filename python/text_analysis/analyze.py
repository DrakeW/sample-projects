import json
load_file = open('tom_sawyer.txt')
giant_string = load_file.read()
load_file.close()
word_list = giant_string.split()
word_counts = {}
for word in word_list:
  if word not in word_counts:
    word_counts[word] = 0
  word_counts[word] += 1
max_count = 0
max_word = ''
for word, count in word_counts.items():
  if count > max_count:
    max_count = count
    max_word = word
print 100. * word_counts['happy'] / len(word_list)
store_file = open('word_counts.json', 'w')
store_file.write(json.dumps(word_counts))
store_file.close()
word_counts_file = open('word_counts.json')
more_counts = json.loads(word_counts_file.read())
word_counts_file.close()
print more_counts

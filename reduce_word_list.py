import json 

# https://gist.github.com/slushman/34e60d6bc479ac8fc698df8c226e4264
file_name = 'minimal_wordle_list.json'

with open(file_name, 'r') as file:
    word_list = json.load(file)

with open('minimal_wordle_list.txt', 'w') as file:
    for word in word_list:
        file.write(word + '\n')

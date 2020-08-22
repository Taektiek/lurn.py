import json

class Word():
    
    def __init__(self, original, translation):
        self.original = original
        self.translation = translation

        self.state = 'Unseen'
        self.in_sprint = False

def load_file(file_loc):
    word_input = open(file_loc)
    return word_input.read()

def create_words(words_dict):
    out = []

    for i in words_dict["words"]:
        out.append(Word(i["original"], i["translation"]))

    return out

def generate_state_dict(words):
    states = {}
    for i in words:
        if i.state in states:
            states[i.state].append(i)
        else:
            states[i.state] = [i]

    return states

def generate_sprint_list(words):
    sprint = []
    for i in words:
        if i.in_sprint:
            sprint.append(i)

    return sprint

def main():
    words_dict = json.loads(load_file('./wordsets/spanish-dutch_test.json'))
    words = create_words(words_dict)
    words[1].state = 'Seen'
    words[3].in_sprint = True
    print(generate_state_dict(words))
    print(generate_sprint_list(words))

if __name__ == "__main__":
    main()
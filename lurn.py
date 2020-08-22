import json

class Word():
    
    def __init__(self, original, translation):
        self.original = original
        self.translation = translation

def load_file(file_loc):
    word_input = open(file_loc)
    return word_input.read()

def create_words(words_dict):
    out = []

    for i in words_dict["words"]:
        out.append(Word(i["original"], i["translation"]))

    return out

def main():
    words = json.loads(load_file('./wordsets/spanish-dutch_test.json'))
    print(create_words(words))

if __name__ == "__main__":
    main()
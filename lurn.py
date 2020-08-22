import json

class Word():
    
    def __init__(self, original, translation):
        self.original = original
        self.translation = translation

def load_file(file_loc):
    word_input = open(file_loc)
    return word_input.read()

def main():
    print(json.loads(load_file('./input_structure.json')))

if __name__ == "__main__":
    main()
import json

def load_file(file_loc):
    word_input = open(file_loc)
    return word_input.read()

def main():
    print(json.loads(load_file('./input_structure.json')))

if __name__ == "__main__":
    main()
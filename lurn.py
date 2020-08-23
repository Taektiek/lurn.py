import json

class Word():
    
    def __init__(self, original, translation):
        self.original = original
        self.translation = translation

        self.state = 'Unseen'
        self.in_sprint = False

class Vocabulary():

    def __init__(self):
        self.file_loc = './wordsets/lasalud.json'

        self.sprint_length = 10
        self.words = self.create_words(json.loads(load_file(self.file_loc)))

        self.sprint = []
        self.active = []

    @staticmethod
    def create_words(words_dict):
        out = []

        for i in words_dict["words"]:
            out.append(Word(i["original"], i["translation"]))

        return out

    def generate_state_dict(self):
        states = {}
        for i in self.words:
            if i.state in states:
                states[i.state].append(i)
            else:
                states[i.state] = [i]

        return states

    def generate_sprint_list(self):
        sprint = []
        for i in self.words:
            if i.in_sprint:
                sprint.append(i)

        return sprint

    def update_sprint(self):
        for i in range(self.sprint_length - len(self.sprint)):
            self.generate_state_dict()["Unseen"][i].in_sprint = True
            self.sprint.append(self.generate_state_dict()["Unseen"][i])
            


def load_file(file_loc):
    word_input = open(file_loc)
    return word_input.read()



def main():
    voc = Vocabulary()
    voc.update_sprint()
    for i in voc.sprint:
        print(i.__dict__)

if __name__ == "__main__":
    main()
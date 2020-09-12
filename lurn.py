#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import random
import string
from os import system, name

class Word():
    
    def __init__(self, original, translation):
        self.original = original
        self.translation = translation

        self.state = 'Unseen'
        self.in_sprint = False

class Question():

    def __init__(self, question, answer, word):
        self.question = question
        self.answer = answer
        self.word = word

class Vocabulary():

    def __init__(self, file_loc, sprint_length=10):
        self.file_loc = file_loc

        self.sprint_length = sprint_length
        self.words = self.create_words(json.loads(load_file(self.file_loc)))

        self.sprint = []
        self.active = []

    @staticmethod
    def create_words(words_dict):
        """Creates a list with objects for every word

        Args:
            words_dict (dictionary): A dictionary with a key words which is a list of dictionaries with an original key and a translation key. 

        Returns:
            list: A list which consists of word objects
        """        
        out = []

        for i in words_dict["words"]:
            out.append(Word(i["original"], i["translation"]))

        return out

    def generate_state_dict(self):
        """Creates a dictionary with lists for each state

        Returns:
            dictionary: A dictionary with list for each state with the state name as key.
        """        
        states = {}
        for i in self.words:
            if i.state in states:
                states[i.state].append(i)
            else:
                states[i.state] = [i]

        return states

    def update_sprint(self):
        """Fills the sprint up to it's intended size
        """        
        self.sprint += random.sample(self.generate_state_dict()["Unseen"], self.sprint_length - len(self.sprint))
        for i in self.sprint:
            i.in_sprint = True

    def generate_round(self):
        """Generates a round based on the sprint
        """        
        self.active = random.sample(self.sprint, self.sprint_length)

    def generate_multiple_choice(self, word):
        """Generates a multiple choice question

        Args:
            word (Word object): The word that needs to be learned

        Returns:
            Question object: A question object with a question and an answer
        """        
        l = [i.translation for i in random.sample(self.words, 3)]
        l.append(word.translation)
        random.shuffle(l)
        s = f'{word.original}\n'
        for i, j in enumerate(l):
            s += f'{str(i+1)}: {j} '
        answer = str(l.index(word.translation) + 1)
        return Question(s, answer, word)
        
        

    def generate_question(self, number):
        """Generates a question based on the state

        Args:
            number (integer): Location in the current round

        Returns:
            Question object: Question object with a question and answer
        """        
        if self.active[number].state == "Unseen":
            return self.generate_multiple_choice(self.active[number])
        elif self.active[number].state == "Seen":
            return Question(f'{self.active[number].translation}: ', self.active[number].original, self.active[number])
        elif self.active[number].state == "Learned":
            return Question(f'{self.active[number].original}: ', self.active[number].translation, self.active[number])

    def check_answer(self, question, given, word):
        """Checks if the given answer is correct

        Args:
            question (Question object): Object with question and answer
            given (string): The answer that was given
            word (Word object): The word the question was based on

        Returns:
            string: Returns feedback string which is shown to the user
        """        
        if word.state == 'Unseen':
            if question.answer.lower() == given.lower():
                word.state = 'Seen'
                return f'Correct the word is now {word.state.lower()}'
            else:
                return f'Wrong the correct answer was: {question.answer}'
        if word.state == 'Seen' or word.state == 'Known':
            if question.answer.lower() == given.lower():
                if word.state == 'Seen':
                    word.state = 'Known'
                else:
                    word.state = 'Learned'
                    self.sprint.remove(word)
                return f'Correct the word is now {word.state.lower()}'
            else:
                return f'Wrong the correct answer was: {word.original}'


def load_file(file_loc):
    """Loads text file from location

    Args:
        file_loc (string): File location

    Returns:
        string: Contents of text file
    """    
    word_input = open(file_loc)
    return word_input.read()

def clear(): 
    """Clears the terminal screen
    """    
    # for windows 
    if name == 'nt': 
        _ = system('cls') 
  
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = system('clear') 

def main():
    clear()
    
    config = json.loads(load_file("./config.json"))

    voc = Vocabulary(config["word_set_loc"], config["sprint_size"])
    for i in range(100):
        print(f'Round {i+1}')
        voc.update_sprint()
        voc.generate_round()
        for i in range(voc.sprint_length):
            voc.update_sprint()
            q = voc.generate_question(i)
            input(voc.check_answer(q, input(q.question), voc.active[i]))
            clear()


if __name__ == "__main__":
    main()
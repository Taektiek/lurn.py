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
        """Creates word objects from dictionary

        Args:
            words_dict (dictionary): A dictionary with a list words with seperate dictionaries 
            with an original and translation key

        Returns:
            list: A list of Word objects
        """
        out = []

        for i in words_dict["words"]:
            out.append(Word(i["original"], i["translation"]))

        return out

    def generate_state_dict(self):
        """Generates a dictionary with lists of objects and each state as a key

        Returns:
            dictionary: a dictionary with lists per state
        """
        states = {}
        for i in self.words:
            if i.state in states:
                states[i.state].append(i)
            else:
                states[i.state] = [i]

        return states

    def update_sprint(self):
        """Updates the sprint to be have sprint_length as its length. Randomly picks Unseen word objects.
        """
        self.sprint += random.sample(self.generate_state_dict()["Unseen"], self.sprint_length - len(self.sprint))
        for i in self.sprint:
            i.in_sprint = True

    def generate_round(self):
        """Generates the round from the current sprint
        """
        self.active = random.sample(self.sprint, self.sprint_length)

    def generate_multiple_choice(self, word):
        l = [i.translation for i in random.sample(self.words, 3)]
        l.append(word.translation)
        random.shuffle(l)
        s = f'{word.original}\n'
        for i, j in enumerate(l):
            s += f'{str(i+1)}: {j} '
        answer = str(l.index(word.translation) + 1)
        return Question(s, answer, word)
        
        

    def generate_question(self, number):
        if self.active[number].state == "Unseen":
            return self.generate_multiple_choice(self.active[number])
        elif self.active[number].state == "Seen":
            return Question(f'{self.active[number].translation}: ', self.active[number].original, self.active[number])
        elif self.active[number].state == "Learned":
            return Question(f'{self.active[number].original}: ', self.active[number].translation, self.active[number])

    def ask_question(self, question):
        """Asks the question using input()

        Args:
            number (int): the position in the array of the question

        Returns:
            str: returns the given answer
        """
        return input(question.question)

    def check_answer(self, question, given, word):
        """Checks if the given answer is correct

        Args:
            answer (Object): The word object the question is based on
            given (str): The string given by the user

        Returns:
            str: String for the user to let them know what happened
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
    """Loads a file and returns the string

    Args:
        file_loc (string): Location of the file

    Returns:
        string: contents of the file
    """
    word_input = open(file_loc)
    return word_input.read()

def clear(): 
  
    # for windows 
    if name == 'nt': 
        _ = system('cls') 
  
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = system('clear') 

def main():
    clear()
    voc = Vocabulary('./wordsets/english-dutch.json', 5)
    for i in range(100):
        print(f'Round {i+1}')
        voc.update_sprint()
        voc.generate_round()
        for i in range(voc.sprint_length):
            voc.update_sprint()
            q = voc.generate_question(i)
            input(voc.check_answer(q, voc.ask_question(q), voc.active[i]))
            clear()


if __name__ == "__main__":
    main()
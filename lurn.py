#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import random
import string

class Word():
    
    def __init__(self, original, translation):
        self.original = original
        self.translation = translation

        self.state = 'Unseen'
        self.in_sprint = False

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


    def ask_question(self, number):
        """Asks the question using input()

        Args:
            number (int): the position in the array of the question

        Returns:
            str: returns the given answer
        """
        return input(self.active[number].original + ': ')
         
    def check_answer(self, answer, given):
        """Checks if the given answer is correct

        Args:
            answer (Object): The word object the question is based on
            given (str): The string given by the user

        Returns:
            str: String for the user to let them know what happened
        """
        if answer.translation.lower() == given.lower():
            answer.state = 'Seen'
            self.sprint.remove(answer)
            return 'Correct'
        else:
            return f'Wrong the correct answer was: {answer.translation}'


def load_file(file_loc):
    """Loads a file and returns the string

    Args:
        file_loc (string): Location of the file

    Returns:
        string: contents of the file
    """
    word_input = open(file_loc)
    return word_input.read()



def main():
    voc = Vocabulary('./wordsets/lasalud.json', 3)
    for i in range(100):
        print(f'Round {i+1}')
        voc.update_sprint()
        voc.generate_round()
        for i in range(voc.sprint_length):
            voc.update_sprint()
            print(voc.check_answer(voc.active[i], voc.ask_question(i)))

if __name__ == "__main__":
    main()
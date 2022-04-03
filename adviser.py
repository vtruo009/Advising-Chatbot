
from nltk import parse, stem
from nltk.stem import PorterStemmer
from nltk.stem import LancasterStemmer
import nltk
import re
import os
import json
import GoogleDF
import parse_prereqs

# replace with appropriate json file obtianed from DialogFlow
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = '.json'

stemmer = LancasterStemmer()

course_list = {}
stemmed_query = []
dictionary = []
english_dict = []

def PopulateLists():
    global course_list
    course_list = parse_prereqs.ParsePrerequsites()

def GenerateResponse(intent, params, processed_tokens):
    global course_list
    if len(params) == 0:
        return
    # Need to fix this for checking sufficiency because params is gonna be a list
    if type(params) == str:
        c = re.sub("[A-Za-z]+", lambda ele: " " + ele[0] + " ", params).strip()
        temp = int(re.search(r'\d+', c).group())
        if temp < 100:
            c = c[:2] + '0' + c[3:]
        else:
            c = c.replace(' ', '')
    else:
        c = re.sub("[A-Za-z]+", lambda ele: " " + ele[0] + " ", params[1]).strip()
        temp = int(re.search(r'\d+', c).group())
        if temp < 100:
            c = c[:2] + '0' + c[3:]
        else:
            c = c.replace(' ', '')

    if not bool(params):
        return
    elif intent == "Check Prerequisites":
        print(course_list[c])
    elif intent == "Check Available Classes":
        courses = ''
        mod_c = re.sub("[A-Za-z]+", lambda ele: " " + ele[0] + " ", c).strip()
        for course in course_list:
            if mod_c.upper() in course_list[course]:
                if courses == '':
                    courses = course.upper()
                else:
                    courses +=  ', ' + course.upper()
        print(courses)
    elif intent == "Check Sufficiency":
        print('User\'s intention is to:', intent)


#====================== Query Processing ======================#
def find_edit1_words(input):
    letters = 'abcdefghijklmnopqrstuvwxyz0123456789'
    splits = [(input[:i], input[i:])          for i in range(len(input) + 1)]
    deletes = [L + R[1:]                     for L, R in splits if R]
    replaces = [L + c + R[1:]               for L, R in splits if R for c in letters]
    inserts = [L + c + R                    for L, R in splits for c in letters]
    return list(deletes + replaces + inserts)

def spelled_correctly(tokens):
    global dictionary
    global english_dict
    one_edit_words = {}
    suggestions = {}
    if len(dictionary) == 0:
        with open("dictionaries/courses.txt", "r") as f:
            dictionary = f.read().lower().replace(' ', '').splitlines()

    if len(english_dict) == 0:
        with open("dictionaries/dictionary.txt", "r") as f:
            english_dict = f.read().lower().splitlines()
    
    for token in tokens:
        if token not in dictionary and token not in english_dict:
            one_edit_words[token] = find_edit1_words(token)

    for key in one_edit_words:
        for word in one_edit_words[key]:
            if word in dictionary or word in english_dict:
                if key not in suggestions:
                    suggestions[key] = [word]
                else:
                    suggestions[key].append(word)
        
    return suggestions
    
def ProcessQuery(user_query):
    tokens = re.findall(r'[a-zA-Z]+\s?[0-9]+[a-zA-Z]*|\b[a-zA-Z]+\b', user_query.lower())
    
    processed_tokens = []
    for token in tokens:
        processed_tokens.append(token.replace(' ', ''))

    corrected_words = spelled_correctly(processed_tokens)
    if len(corrected_words) > 2:
        for s in corrected_words:
            print(s, ':', corrected_words[s])
        return
    (intent, params) = GoogleDF.CheckIntent(' '.join(processed_tokens))
    PopulateLists()
    GenerateResponse(intent, params, processed_tokens)

def main():
    GoogleDF.implicit()
    
    while (True):
        user_query = input("Student: ")
        ProcessQuery(user_query)

main()
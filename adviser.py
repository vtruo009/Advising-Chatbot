
from nltk import parse, stem
from nltk.stem import PorterStemmer
from nltk.stem import LancasterStemmer
import nltk
import re
import os
import json
import GoogleDF
import parse_pdf
import envir

stemmer = LancasterStemmer()

course_list = {}
stemmed_query = []
dictionary = []

# def ProcessData():
#     # Read in courses
#     with open("course_prereqs.json") as file:
#         data = json.load(file)

#     for course in data["courses"]:
#         if course['number'] not in course_list:
#             course_list[course['number'].lower()] = course["prerequisites"]
def PopulateLists():
    global course_list
    course_list = parse_pdf.ParsePrerequsitesPDF()

def GenerateResponse(intent, params, processed_tokens):
    global course_list
    if intent == "Check Prerequisites":
        print(course_list[params])
    elif intent == "Check Available Classes":
        c = re.sub("[A-Za-z]+", lambda ele: " " + ele[0] + " ", params[0]).upper()
        courses = ''
        for course in course_list:
            if c in course_list[course]:
                if courses == '':
                    courses = course.upper()
                else:
                    courses +=  ', ' + course.upper()
        print(courses)

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
    one_edit_words = {}
    suggestions = {}
    if len(dictionary) == 0:
        with open("courses.txt", "r") as f:
            dictionary = f.read().lower().replace(' ', '').splitlines()
        # with open("englishwords.txt", "r") as f: #do we need this
        #     dictionary = f.read().lower().splitlines()

    for token in tokens:
        if token not in dictionary:
            # one call to find_edit1_words will find all the words
            # but there are more then one tokens so i need to append
            #do i need a misspelled words list?
            one_edit_words[token] = find_edit1_words(token)
    # print(one_edit_words)
    for key in one_edit_words:
        suggestions[key] = []
        for word in one_edit_words[key]:
            if word in dictionary:
                # suggestions.append(word)
                suggestions[key].append(word)
    return suggestions
    
def ProcessQuery(user_query):
    # tokenizing
    # tokens = re.findall(r'\b[a-zA-Z]+[0-9]*[a-zA-Z]*\b', user_query.lower())
    # tokens = re.split("\s+",user_query.lower())
    # tokens = re.findall(r'(?:[cC][sS]|(?:ENGR|engr)|[eE]{2})\s?[0-9]+[a-zA-Z]*|\b[a-zA-Z]+\b', user_query.lower())
    tokens = re.findall(r'[a-zA-Z]+\s?[0-9]+[a-zA-Z]*|\b[a-zA-Z]+\b', user_query.lower())
    # tokens = sorted(list(set(tokens)))
    # print(tokens)

    processed_tokens = []
    for token in tokens:
        processed_tokens.append(token.replace(' ', ''))
    # stemming
    # for token in tokens:
    #     if token == "prereq" or token == "prereqs":
    #         token = "prerequisites"
    #     stemmed_query.append(stemmer.stem(token))
    # print(tokens)
    # print(processed_tokens)
    # corrected_words = spelled_correctly(processed_tokens)
    (intent, params) = GoogleDF.CheckIntent(' '.join(processed_tokens))
    PopulateLists()
    GenerateResponse(intent, params, processed_tokens)
    
    # print(corrected_words)


def main():
    GoogleDF.implicit()
    
    # ParsePDF()
    # ProcessData()
    # # while (True):
    # print("Adviser: What can I help you with?")
    user_query = input("Student: ")
    ProcessQuery(user_query)
    # parse_pdf.ParseCoursesPDF()
    parse_pdf.ParsePrerequsitesPDF()
    # FindPrereq()



main()


# def FindPrereq():
#     course_num = ''.join(re.findall("[cC][sS][0-9]{1,3}[a-zA-Z]*", ' '.join(stemmed_query)))
#     if course_num in course_list:
#         retrieved = course_list[course_num]
#         print("Adviser: The prerequisites for", course_num + ":")
#         for prereq in retrieved:
#             print(prereq)

from nltk import stem
from nltk.stem import PorterStemmer
from nltk.stem import LancasterStemmer
import nltk
import PyPDF2 as p
import re
import json

stemmer = LancasterStemmer()

course_list = {}
stemmed_query = []

def ParsePDF():
    # file = open("CSE_Courses.pdf", "rb")
    # pdf = p.PdfFileReader(file)
    # page = pdf.getPage(0)
    # pdf_text = page.extractText()
    with open("courses.pdf", "rb") as file:
        pdf = p.PdfFileReader(file)
        num_pages = pdf.getNumPages()
        content = ''
        for i in range(num_pages):
            page = pdf.getPage(i)
            content += page.extractText() + '\n'
    # tokens = re.findall("[cC][sS]\s?[0-9]+[a-zA-Z]*", content)
    tokens = re.findall("(?:[cC][sS]|ENGR|EE)\s?[0-9]+[a-zA-Z]*", content)
    for token in tokens:
        print(token)


def ProcessData():
    # Read in courses
    with open("course_prereqs.json") as file:
        data = json.load(file)

    for course in data["courses"]:
        if course['number'] not in course_list:
            course_list[course['number'].lower()] = course["prerequisites"]

def ProcessQuery(user_query):
    # tokenizing
    tokens = re.findall(r'\b[a-zA-Z]+[0-9]*[a-zA-Z]*\b', user_query.lower())
    # tokens = re.split("\s+",s.lower())
    tokens = sorted(list(set(tokens)))

    # stemming
    for token in tokens:
        if token == "prereq" or token == "prereqs":
            token = "prerequisites"
        stemmed_query.append(stemmer.stem(token))

def FindPrereq():
    course_num = ''.join(re.findall("[cC][sS][0-9]{1,3}[a-zA-Z]*", ' '.join(stemmed_query)))
    if course_num in course_list:
        retrieved = course_list[course_num]
        print("Adviser: The prerequisites for", course_num + ":")
        for prereq in retrieved:
            print(prereq)

def main():
    # ProcessData()
    # # while (True):
    # print("Adviser: What can I help you with?")
    # user_query = input("Student: ")
    # ProcessQuery(user_query)
    # FindPrereq()
    ParsePDF()


main()
import re
import nltk
import PyPDF2 as p
import requests
from bs4 import BeautifulSoup
from nltk.tokenize import sent_tokenize

def ParseCoursesPDF():
    '''Need to keep in mind that new courses may be added to this websit. Need to do some dynamic processing'''
    # file = open("CSE_Courses.pdf", "rb")
    # pdf = p.PdfFileReader(file)
    # page = pdf.getPage(0)
    # pdf_text = page.extractText()
    with open("pdfs/courses.pdf", "rb") as file:
        pdf = p.PdfFileReader(file)
        num_pages = pdf.getNumPages()
        content = ''
        for i in range(num_pages):
            page = pdf.getPage(i)
            content += page.extractText() + '\n'
    # tokens = re.findall("[cC][sS]\s?[0-9]+[a-zA-Z]*", content)
    tokens = re.findall("(?:[cC][sS]|ENGR|EE)\s?[0-9]+[a-zA-Z]*", content)
    with open("courses.txt", "r+") as file:
        for token in tokens:
            file.write(token + '\n')


def ParsePrerequsitesPDF():
    '''Need to keep in mind that new courses may be added to this websit. Need to do some dynamic processing'''
    URL = 'https://www1.cs.ucr.edu/undergraduate/course-descriptions/'
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    courses = {}
    course = ''
    for text in soup.find_all('tr')[1:]:
        courses[text.td.text] = text.contents[2].text

    for number in courses:
        sentences = nltk.sent_tokenize(courses[number])
        for sent in sentences:
            prereq = re.findall("^Prerequisite\(s\)\:.*", sent)
            if len(prereq) > 0:
                courses[number] = prereq[0]
                break
            else:
                courses[number] = 'Prerequisite(s): none.'
    # prereqs = []
    # for item in desc:
    #     sentences = nltk.sent_tokenize(item)
    #     for sent in sentences:
    #         if bool(re.findall("^Prerequisite\(s\)\:.*", sent)):
    #             prereqs.append(re.findall("^Prerequisite\(s\)\:.*", sent))
















    # print(soup.body.text)
    # results = soup.find_all('tr')
    # print(results[1])
    # with open("pdfs/prerequisites.pdf", "rb") as file:
    #     pdf = p.PdfFileReader(file)
    #     num_pages = pdf.getNumPages()
    #     content = ''
    #     for i in range(num_pages):
    #         page = pdf.getPage(i)
    #         content += page.extractText() + '\n'
    # print(content)
    # tokens = re.findall("[cC][sS]\s?[0-9]+[a-zA-Z]*", content)
    prereqs = []
    # tokens = re.split("(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\ .|\?)\s", content)
    # tokens = sent_tokenize(content)
    # print(tokens)
    # for token in tokens:
    #     print(token)
        # the_one = re.findall("^Prerequisite\(s\):\s.*", token)
        # print(the_one)
        # prereqs.extend(the_one)
        # if len(the_one) > 0:
        #     break
    # print(prereqs)
    # # for token in tokens:
    # #     print(token)
    # print("the one", the_one[0].replace('Ò', '\"').replace('Ó', '\"'))
import re
import nltk
import PyPDF2 as p
import requests
from bs4 import BeautifulSoup
from nltk.tokenize import sent_tokenize

#This is for downloading the course list PDF and parse the PDF instead of webpage
'''def ParseCoursesPDF():
    #Need to keep in mind that new courses may be added to this website. Need to do some dynamic processing
    with open("pdfs/courses.pdf", "rb") as file:
        pdf = p.PdfFileReader(file)
        num_pages = pdf.getNumPages()
        content = ''
        for i in range(num_pages):
            page = pdf.getPage(i)
            content += page.extractText() + '\n'
    tokens = re.findall("(?:[cC][sS]|ENGR|EE)\s?[0-9]+[a-zA-Z]*", content)
    with open("courses.txt", "r+") as file:
        for token in tokens:
            file.write(token + '\n')'''


def ParsePrerequsites():
    '''Need to keep in mind that new courses may be added to this websit. Need to do some dynamic processing'''
    URL = 'https://www1.cs.ucr.edu/undergraduate/course-descriptions/'
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    courses = {}
    course = ''
    for text in soup.find_all('tr')[1:]:
        courses[text.td.text.lower().replace(" ", '')] = text.contents[2].text

    for number in courses:
        sentences = nltk.sent_tokenize(courses[number])
        for sent in sentences:
            prereq = re.findall("^Prerequisite\(s\)\:.*", sent)
            if len(prereq) > 0:
                courses[number] = prereq[0][17:]
                break
            else:
                courses[number] = 'Prerequisite(s): none.'
    return courses
# Virtual Chatbot

Virtual Advisor is designed to specifically help UC Riverside's Bournes College of Engineering academic advisors answer Engineering & Computer Science (ENCS) students' course related questions. In 2021, there are 1000+ undergraduates but only 3 academic advisors for ENCS majors.

## Overview

[Application Demo](https://youtu.be/ienj8SfMV8k)

First, the program prompts for user input.

![Prompting user input](/assets/Prompt.png)

Once user hits enter, the input then gets send to ```ProcessQuery()``` for tokenization and for DialogFlow to check the user's intent. Since future courses may be added to the curriculum, parsing the webpage to extract information makes the program more dynamic and maintainable than downloading the webpage as a PDF then parse the PDF. The program pases the webpage in ```ParsePrerequisites()``` and stores the extracted courses in a list for later use.

When the user intent is determined and the ```course_list``` is ready, the program generates the response in ```GenerateResponse()```, printing out the prerequisites needed for a course or the courses that user can take after taking a course.

![Interaction with chatbot](/assets/Interaction.png)

## Tools Used

* Python
    * nltk - library used for tokenization
* DiaglogFlow - create intents and entities to generate the appropriate response based on user input
* BeautifulSoup - used to parse the web page that lists all the available undergraduate courses for Computer Science majors

## Future Enhancements

There are a few areas where this project could improve.

### Third Intent

As of now, the program can only determine two types of intents:

* Check prerequisites - "What do I need for CS100?
* Check for available classes - "What classes can I take after taking CS10?"

For future enhancements, a third intent should be added to allow students to check if they have the prerequsites done for a certain calss they want to take. FOr example:

* Check sufficiency - "Is CS10 and CS12 enough for CS100?"

### Response Structure

Currently, the program simply tokenizes the prerequisite paragraph from the webpage and present that as is to the user. For better readability, the response should be structured into bullet points. Another nice-to-have feature is to link the corresponding course description page to each bullet point, allowing students to learn more about the courses.
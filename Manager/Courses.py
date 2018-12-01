
from Manager.Constants import SESSION_REQUESTS, COURSES_GETTER_URL
from lxml import html
from Scrappers.Tasks import scrapeTasks
from Scrappers.Contents import scrapeContents
from Scrappers.Polls import scrapePolls
from Scrappers.Quests import scrapeQuests
#from Scrappers.Grades import scrapeGrades

def inspectCourses():
    # Get courses
    myCourses = html.fromstring(SESSION_REQUESTS.get(COURSES_GETTER_URL, headers = dict(referer = COURSES_GETTER_URL)).content).xpath("//p[@class='coursename']")
    if(len(myCourses) == 0):
        print "Incorrect login";

    for course in myCourses:
        name = course.xpath("./a/text()")[0];
        print "Scrapping content of: " + name;
        link = course.xpath("./a/@href")[0];
        print "Opening link: " + link;
        courseContent = html.fromstring(SESSION_REQUESTS.get(link, headers = dict(referer = COURSES_GETTER_URL)).content).xpath("//a[text()='Este curso']/../div[@class='dropdown-menu']/ul/li/a");
        for courseStuff in courseContent:
            sublink = courseStuff.xpath("./@href")[0]
            if (courseStuff.xpath("./text()")[0].upper() == "TAREAS"):
                scrapeTasks(sublink, name);
            elif (courseStuff.xpath("./text()")[0].upper() == "RECURSOS"):
                scrapeContents(sublink, name);
            elif (courseStuff.xpath("./text()")[0].upper() == "ENCUESTAS"):
                scrapePolls(sublink, name);
            elif (courseStuff.xpath("./text()")[0].upper() == "CUESTIONARIOS"):
                scrapeQuests(sublink, name);
            #if (courseStuff.xpath("./text()")[0].upper() == "CALIFICACIONES"):
                #scrapeGrades(sublink, name);
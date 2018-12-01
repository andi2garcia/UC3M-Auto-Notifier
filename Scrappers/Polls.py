
from Manager.Constants import SESSION_REQUESTS, COURSES_GETTER_URL
from tinydb import Query
from lxml import html
from Manager.Database import db
from Manager.Mailer import sendEmailnotify
import unicodedata

def scrapePolls(url, courseName):
    course = html.fromstring(SESSION_REQUESTS.get(url, headers=dict(referer=COURSES_GETTER_URL)).content);
    tableCols = course.xpath("//div[@role='main']/table/thead/tr/th/text()");
    coursePolls = course.xpath(
        "//div[@role='main']/table/tbody/tr[not(contains(@class, 'tabledivider'))]");
    pollNumber = 0;
    for coursePoll in coursePolls:
        colNumber = 0
        coursePollInfo = coursePoll.xpath("./td[not(a)] | ./td/a")

        pollObj = {};
        for val in coursePollInfo:
            val = val.xpath("./text()")
            if len(val) == 0:
                val = ""
            else:
                val = val[0];

            pollObj.update({tableCols[colNumber]: val});
            colNumber += 1;
        PollQuery = Query()
        pollOnDb = db.table('Polls').search(PollQuery.Nombre == pollObj.get("Nombre"));
        if (len(pollOnDb) == 0):
            msg = courseName + ": Tienes una nueva encuesta disponible -> " + pollObj.get("Nombre");
            sendEmailnotify(msg);
            print msg;
        db.table('Polls').upsert(pollObj, PollQuery.Nombre == pollObj.get("Nombre"));
        pollNumber += 1;
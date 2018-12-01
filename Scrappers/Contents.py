
from Manager.Constants import SESSION_REQUESTS, COURSES_GETTER_URL
from tinydb import Query
from lxml import html
from Manager.Database import db
from Manager.Mailer import sendEmailnotify
import unicodedata

def scrapeContents(url, courseName):
    course = html.fromstring(SESSION_REQUESTS.get(url, headers=dict(referer=COURSES_GETTER_URL)).content);
    tableCols = course.xpath("//div[@role='main']/table/thead/tr/th/text()");
    courseResources = course.xpath(
        "//div[@role='main']/table/tbody/tr[not(contains(@class, 'tabledivider'))]");
    resourceNumber = 0;
    for courseResource in courseResources:
        colNumber = 0
        courseResourceInfo = courseResource.xpath("./td[not(a)] | ./td/a")

        resourceObj = {};
        for val in courseResourceInfo:
            val = val.xpath("./text()")
            if len(val) == 0:
                val = ""
            else:
                val = val[0];

            resourceObj.update({tableCols[colNumber]: val});
            colNumber += 1;
        ResourceQuery = Query()
        resourceOnDb = db.table('Resources').search(ResourceQuery.Nombre == resourceObj.get("Nombre"));
        if (len(resourceOnDb) == 0):
            msg = courseName + ": Tienes un nuevo recurso disponible -> " + resourceObj.get("Nombre");
            sendEmailnotify(msg);
            print msg;
        db.table('Resources').upsert(resourceObj, ResourceQuery.Nombre == resourceObj.get("Nombre"));
        resourceNumber += 1;
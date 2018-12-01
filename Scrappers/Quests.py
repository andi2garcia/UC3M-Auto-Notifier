
from Manager.Constants import SESSION_REQUESTS, COURSES_GETTER_URL
from tinydb import Query
from lxml import html
from Manager.Database import db
from Manager.Mailer import sendEmailnotify
import unicodedata

def scrapeQuests(url, courseName):
    course = html.fromstring(SESSION_REQUESTS.get(url, headers=dict(referer=COURSES_GETTER_URL)).content);
    tableCols = course.xpath("//div[@role='main']/table/thead/tr/th/text()");
    courseQuests = course.xpath(
        "//div[@role='main']/table/tbody/tr[not(contains(@class, 'tabledivider'))]");
    questNumber = 0;
    for courseQuest in courseQuests:
        colNumber = 0
        courseQuestInfo = courseQuest.xpath("./td[not(a)] | ./td/a")

        questObj = {};
        for val in courseQuestInfo:
            val = val.xpath("./text()")
            if len(val) == 0:
                val = ""
            else:
                val = val[0];

            questObj.update({tableCols[colNumber]: val});
            colNumber += 1;
        QuestQuery = Query()
        questOnDb = db.table('Quests').search(QuestQuery.Nombre == questObj.get("Nombre"));
        prevDate = db.table('Quests').get(QuestQuery.Tareas == questObj.get("Nombre"));
        if (len(questOnDb) == 0):
            msg = courseName + ": Tienes un nuevo cuestionario disponible -> " + questObj.get("Nombre");
            sendEmailnotify(msg);
            print msg;
        elif (db.table('Quests') is not None and questObj is not None and prevDate is not None
              and questObj.get("Fecha de entrega") != prevDate["Fecha de entrega"]):
            msg = courseName + ": Se ha modificado la fecha de entrega del cuestionario a " + questObj.get(
                    "Fecha de entrega") + " -> " + questObj.get("Nombre");
            print msg;
            sendEmailnotify(msg);
        db.table('Quests').upsert(questObj, QuestQuery.Nombre == questObj.get("Nombre"));
        questNumber += 1;
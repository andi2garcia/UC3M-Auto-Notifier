# -*- coding: iso-8859-1 -*-
from Manager.Constants import SESSION_REQUESTS, COURSES_GETTER_URL
from tinydb import Query
from lxml import html
from Manager.Database import db
from Manager.Mailer import sendEmailnotify
import unicodedata
#TODO: fix a encoding
def scrapeGrades(url, courseName):
    course = html.fromstring(SESSION_REQUESTS.get(url, headers=dict(referer=COURSES_GETTER_URL)).content);
    tableCols = course.xpath("//div[@role='main']/table/thead/tr/th/text()");
    courseGrades = course.xpath(
        "//div[@role='main']/table/tbody/tr[not(contains(@class, 'tabledivider'))]");
    gradeNumber = 0;
    for courseGrade in courseGrades:
        colNumber = 0
        courseGradeInfo = courseGrade.xpath("./td | ./th/a")

        gradeObj = {};
        for val in courseGradeInfo:
            val = val.xpath("./text()")
            if len(val) == 0:
                val = ""
            else:
                val = val[0];

            gradeObj.update({tableCols[colNumber]: val});
            colNumber += 1;
        if len(gradeObj) > 0:
            print gradeObj;
            GradeQuery = Query()
            gradeOnDb = db.table('Grades').search(GradeQuery.Nombre == gradeObj.get("Ítem de calificación"));
            if (len(gradeOnDb) == 0):
                msg = courseName + ": Tienes una nueva nota asignada (has sacado un " + gradeObj.get("Calificación") + ") -> " + gradeObj.get("Ítem de calificación");
                sendEmailnotify(msg);
                print msg;
            db.table('Grades').upsert(gradeObj, GradeQuery.Nombre == gradeObj.get("Ítem de calificación"));
            gradeNumber += 1;

from Manager.Constants import SESSION_REQUESTS, COURSES_GETTER_URL
from tinydb import Query
from lxml import html
from Manager.Database import db
from Manager.Mailer import sendEmailnotify

def scrapeTasks(url, courseName):
    course = html.fromstring(SESSION_REQUESTS.get(url, headers=dict(referer=COURSES_GETTER_URL)).content);
    tableCols = course.xpath("//table[@class='generaltable']/thead/tr/th/text()");
    courseTasks = course.xpath(
        "//table[@class='generaltable']/tbody/tr[not(contains(@class, 'tabledivider'))]");

    taskNumber = 0;
    for courseTask in courseTasks:
        colNumber = 0
        courseTaskInfo = courseTask.xpath("./td[not(a)]| ./td/a")
        taskObj = {};
        for val in courseTaskInfo:
            val = val.xpath("./text()")
            if len(val) == 0:
                val = ""
            else:
                val = val[0];

            taskObj.update({tableCols[colNumber]: val});
            colNumber += 1;
        TaskQuery = Query()
        taskOnDb = db.table('Tasks').search(TaskQuery.Tareas == taskObj.get("Tareas"));
        if len(taskOnDb) == 0:
            msg = courseName + ": Tienes una tarea nueva para realizar antes del " + taskObj.get("Fecha de entrega") + " -> " + taskObj.get("Tareas");
            sendEmailnotify(msg);
            print msg;
        elif (type(db.table('Tasks')) != "NoneType" and taskObj.get("Fecha de entrega") != db.table('Tasks').get(TaskQuery.Tareas == taskObj.get("Tareas"))["Fecha de entrega"]):
            msg = courseName + ": Se ha modificado la fecha de entrega del trabajo a " + taskObj.get(
                    "Fecha de entrega") + " -> " + taskObj.get("Tareas");
            sendEmailnotify(msg);
            print msg;
        db.table('Tasks').upsert(taskObj, TaskQuery.Tareas == taskObj.get("Tareas"));
        taskNumber += 1;
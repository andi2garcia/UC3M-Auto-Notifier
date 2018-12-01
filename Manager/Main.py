from Manager.MoodleLogin import doLogin
from Manager.Database import closeDb, initDb
from Manager.Courses import inspectCourses
import sys

def main():
    reload(sys)
    sys.setdefaultencoding('utf8')
    # Init db
    initDb();

    # Login on Moodle
    doLogin();

    # Get Courses
    inspectCourses();

    # Close database
    closeDb();

if __name__ == '__main__':
    main()
import sqlite3


def get_learning_obj_en(db_file):
    """
    :param db_file: database file location
    :return: list with learning objectives
    """
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    statement = 'SELECT learning_obj FROM acs_modules'
    cursor.execute(statement)
    records = cursor.fetchall()
    learning_obj = []
    for row in records:
        learning_obj.append([row[0]])
    conn.close()

    return learning_obj

def get_course_by_title(db_file, title):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM acs_modules WHERE title LIKE ?", ("%" + title +  "%",))
    records = cursor.fetchall()
    courses = []
    for row in records:
        courses.append(row)
    conn.close()
    return courses

def get_course_by_instructor(db_file, name):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM acs_modules WHERE instructor LIKE ?", ("%" + name + "%",))
    records = cursor.fetchall()
    instructor = []
    for row in records:
        instructor.append(row[1])
    conn.close()
    return instructor

def get_course_by_area(db_file, elective):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    if elective:
        cursor.execute("SELECT * FROM acs_modules WHERE course_type LIKE \'%elective%\'")
    else:
        cursor.execute("SELECT * FROM acs_modules WHERE course_type LIKE \'%obligatory%\'")

    records = cursor.fetchall()
    courses = []
    for row in records:
        courses.append(row[1])
    conn.close()
    return courses
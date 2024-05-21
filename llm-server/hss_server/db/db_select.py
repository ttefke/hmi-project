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
        instructor.append(row)
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
        courses.append(row)
    conn.close()
    return courses

def get_course_by_term(db_file, term):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    if "1" in term:
        cursor.execute("SELECT * FROM acs_modules WHERE time LIKE \'%1%\'")
    elif "2" in term or "summer" in term:
        cursor.execute("SELECT * FROM acs_modules WHERE time LIKE \'%2%\'")
    elif "3" in term:
        cursor.execute("SELECT * FROM acs_modules WHERE time LIKE \'%3%\'")
    else: # winter
        cursor.execute("SELECT * FROM acs_modules WHERE time LIKE \'%1%\' OR time LIKE \'%3%\'")

    records = cursor.fetchall()
    courses = []
    for row in records:
        courses.append(row)
    conn.close()
    return courses

def get_course_by_index(db_file, index):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM acs_modules WHERE ROWID = ?", (index,))
    records = cursor.fetchall()
    courses = []
    for row in records:
        courses.append(row)
    conn.close()
    return courses
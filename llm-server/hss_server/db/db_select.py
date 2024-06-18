import sqlite3

import Levenshtein

## SBERT matching
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

def get_course_contents(db_file):
    """
    :param db_file: database file location
    :return: list with course contents
    """
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    statement = 'SELECT course_contents FROM acs_modules'
    cursor.execute(statement)
    records = cursor.fetchall()
    contents = []
    for row in records:
        contents.append([row[0]])
    conn.close()

    return contents

## SQL matching
# Levenshtein
def levenshtein_string_matches(s1, s2, ratio=0.66):
    return Levenshtein.ratio(s1, s2) > ratio

def levenshtein_course_matches(row, s, index, ratio=0.66):
    stringFromDB = row[index]
    stringsFromDB = stringFromDB.split(" ")
    for string in stringsFromDB:
        if len(string) > 3 and levenshtein_string_matches(string, s, ratio):
            return True
    
    return False

# SQL helper
def row_to_course_information(row):
    # Selects the following columns: page number, title, instructor, learning objectives
    return [1.0, [row[0:4]]]

# Select by row
def get_course_by_title(db_file, title, isAnyMatch, isExactMatch):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    if isExactMatch:
        cursor.execute('SELECT * FROM acs_modules WHERE UPPER(title) LIKE UPPER(?);', ("%" + title[1:-1] +  "%",))
    else:
        cursor.execute('SELECT * FROM acs_modules')
    
    records = cursor.fetchall()
    courses = []
    for row in records:
        # Filter results if neither any nor exact match
        # Use elif to avoid unnecessary calls to the matching function
        if isAnyMatch or isExactMatch:
            courses.append(row_to_course_information(row))
        elif levenshtein_course_matches(row, title, 1, 0.5):
            courses.append(row_to_course_information(row))
            
    conn.close()    
    return courses

def get_course_by_instructor(db_file, name, isAnyMatch, isExactMatch):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    if isExactMatch:
        cursor.execute('SELECT * FROM acs_modules WHERE UPPER(instructor) LIKE UPPER(?);', ("%" + name[1:-1] + "%",))
    else:
        cursor.execute('SELECT * FROM acs_modules;')
        
    records = cursor.fetchall()
    courses = []
    for row in records:
        # Filter results if neither any nor exact match
        # Use elif to avoid unnecessary calls to the matching function
        if isAnyMatch or isExactMatch:
            courses.append(row_to_course_information(row))
        elif levenshtein_course_matches(row, name, 2):
            courses.append(row_to_course_information(row))
    
    conn.close()
    return courses

def get_course_by_area(db_file, elective, isAnyMatch, isExactMatch):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Exact match: throw away quotes
    if isExactMatch:
        elective = elective[1:-1]

    if levenshtein_string_matches("true", elective):
        cursor.execute('SELECT * FROM acs_modules WHERE course_type LIKE \'%elective%\';')
    elif levenshtein_string_matches("false", elective):
        cursor.execute('SELECT * FROM acs_modules WHERE course_type LIKE \'%obligatory%\';')
    elif isAnyMatch:
        cursor.execute('SELECT * FROM acs_modules')
    else:
        return []

    records = cursor.fetchall()
    courses = []
    for row in records:
        courses.append(row_to_course_information(row))
    conn.close()
    return courses

def get_course_by_term(db_file, term, isAnyMatch, isExactMatch):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Exact match: throw away quotes
    if isExactMatch:
        term = term[1:-1]

    if "1" in term:
        cursor.execute('SELECT * FROM acs_modules WHERE time LIKE \'%1%\';')
    elif "2" in term or levenshtein_string_matches("summer", term.lower()):
        cursor.execute('SELECT * FROM acs_modules WHERE time LIKE \'%2%\';')
    elif "3" in term:
        cursor.execute('SELECT * FROM acs_modules WHERE time LIKE \'%3%\';')
    elif levenshtein_string_matches("winter", term.lower()):
        cursor.execute('SELECT * FROM acs_modules WHERE time LIKE \'%1%\' OR time LIKE \'%3%\';')
    elif isAnyMatch:
        cursor.execute('SELECT * FROM acs_modules')
    else:
        return []

    records = cursor.fetchall()
    courses = []
    for row in records:
        courses.append(row_to_course_information(row))
    conn.close()
    return courses

def get_course_by_learning(db_file, learning, isAnyMatch, isExactMatch):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    if isAnyMatch:
        cursor.execute('SELECT * FROM acs_modules;')
    elif isExactMatch:
        # In these query type the contents array contains exactly one element
        cursor.execute('SELECT * FROM acs_modules WHERE UPPER(learning_obj) LIKE UPPER(?);', ("%" + learning[0][1:-1] + "%",))
    else:
        return []
        
    records = cursor.fetchall()
    courses = []
    for row in records:
        courses.append(row_to_course_information(row))
    conn.close()
    return courses

def get_course_by_content(db_file, contents, isAnyMatch, isExactMatch):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    if isAnyMatch:
        cursor.execute('SELECT * FROM acs_modules;')
    elif isExactMatch:
        # In these query type the contents array contains exactly one element
        cursor.execute('SELECT * FROM acs_modules WHERE UPPER(course_contents) LIKE UPPER(?);', ("%" + contents[0][1:-1] + "%",))
    else:
        return []

    records = cursor.fetchall()
    courses = []
    for row in records:
        courses.append(row_to_course_information(row))
    conn.close()
    return courses

def get_course_by_index(db_file, index):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM acs_modules WHERE ROWID = ?;', (index,))
    records = cursor.fetchall()
    courses = []
    for row in records:
        courses.append(row[0:4])
    conn.close()
    return courses
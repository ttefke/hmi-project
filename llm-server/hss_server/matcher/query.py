from db.db_select import get_course_by_title, get_course_by_instructor, get_course_by_area, get_course_by_term
from quart import jsonify

def list_course_by_title(ctx, json_payload):
    logger = ctx["logger"]
    db_courses = ctx["db_courses"]
    match = {}

    if not "intitle" in json_payload:
        return jsonify('{No title specified}')
    
    query = json_payload['intitle']

    if not isinstance(query, str):
        return jsonify('{Course title must be string}')
    
    logger.debug('query: {0}'.format(query))
    match = get_course_by_title(db_courses, query)
    logger.debug('{0}'.format(match))
    return match

def list_course_by_instructor(ctx, json_payload):
    logger = ctx["logger"]
    db_courses = ctx["db_courses"]
    match = {}

    if not "instructor" in json_payload:
        return jsonify('{No instructor specified}')

    query = json_payload['instructor']

    if not isinstance(query, str):
        return jsonify('{Instructor name must be string}')
    
    logger.debug('query: {0}'.format(query))
    match = get_course_by_instructor(db_courses, query)
    logger.debug('{0}'.format(match))
    return match

def list_course_by_area(ctx, json_payload):
    logger = ctx["logger"]
    db_courses = ctx["db_courses"]
    match = {}

    if not "elective" in json_payload:
        return jsonify('{Not specified whether module should be elective}')
    
    query = json_payload['elective']

    if not isinstance(query, bool):
        return jsonify('{Course type must be boolean}')

    logger.debug('query: {0}'.format(query))
    match = get_course_by_area(db_courses, query)
    logger.debug('{0}'.format(match))
    return match

def list_course_by_term(ctx, json_payload):
    logger = ctx["logger"]
    db_courses = ctx["db_courses"]
    match = {}

    if not "term" in json_payload:
        return jsonify('{No term specified}')
    
    query = json_payload['term']
    
    if not isinstance(query, str):
        return jsonify('{Course term must be string}')
    
    logger.debug('query: {0}'.format(query))
    match = get_course_by_term(db_courses, query)
    logger.debug('{0}'.format(match))
    return match
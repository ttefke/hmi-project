def toDict(courses):
    # Map course result to dictionary -> can easily be parsed as JSON
    result = {}
    courseList = []
    
    for i in courses:
        course = {}
        course["matchRate"] = float(i[0])
        course["pageNumber"] = int(i[1][0][0])
        course["title"] = i[1][0][1]
        course["instructor"] = i[1][0][2]
        course["learningObjectives"] = i[1][0][3]
        courseList.append(course)

    result["courses"] = courseList
    return result
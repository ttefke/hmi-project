
def toDict(newCourses, existingCourses={}):
    # Map course result to dictionary -> can easily be parsed as JSON
    result = {}
    courseList = []
    
    if not isinstance(existingCourses, dict):
        return {}

    if not existingCourses:
        # No existing courses yet
        pass
    elif not "courses" in existingCourses:
        return {}
    else:
        courseList = existingCourses["courses"]
 
    for i in newCourses:
        course = {}
        course["matchRate"] = float(i[0])
        course["pageNumber"] = int(i[1][0][0])
        course["title"] = i[1][0][1]
        course["instructor"] = i[1][0][2]
        course["learningObjectives"] = i[1][0][3]

        courseIsAlreadyListed = False
        for j in courseList:
            # Check if course is in dict of existing courses
            if j["title"] == course["title"]:
                courseIsAlreadyListed = True
                # Match rate of new course is higher -> remove existing course, add new
                # Else keep existing course
                if j["matchRate"] < course["matchRate"]:
                    courseList.remove(j)
                    courseList.append(course)

        if not courseIsAlreadyListed:
            # Course is not in list -> add
            courseList.append(course)

    result["courses"] = sorted(courseList, key=lambda x: x["matchRate"], reverse=True)
    return result
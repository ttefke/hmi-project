package main

type CourseOverview struct {
	Courses []CourseData `json:"courses"`
}

type CourseData struct {
	MatchRate          float64 `json:"matchRate"`
	Manual             string  `json:"manual"`
	Title              string  `json:"title"`
	Instructor         string  `json:"instructor"`
	LearningObjectives string  `json:"learningObjectives"`
}

func (a CourseData) equals(b CourseData) bool {
	if a.Manual != b.Manual {
		return false
	}
	if a.Title != b.Title {
		return false
	}
	if a.Instructor != b.Instructor {
		return false
	}
	if a.LearningObjectives != b.LearningObjectives {
		return false
	}
	return true
}

func contains(needle CourseData, haystack []CourseData) bool {
	for _, course := range haystack {
		if course.equals(needle) {
			return true
		}
	}
	return false
}

type Facet int

const (
	AND Facet = iota
	OR
	NOT
	INTITLE
	INSTRUCTOR
	LEARNING
	CONTENT
	ELECTIVE
	TERM
	UNKNOWN
	ERROR
)

type QueryExpression struct {
	facet   Facet
	operand string
}

type TitleRequest struct {
	Intitle    string `json:"intitle"`
	AnyMatch   bool   `json:"any"`
	ExactMatch bool   `json:"exact"`
}

type InstructorRequest struct {
	Instructor string `json:"instructor"`
	AnyMatch   bool   `json:"any"`
	ExactMatch bool   `json:"exact"`
}

type ElectiveRequest struct {
	Elective bool `json:"elective"`
}

type TermRequest struct {
	Term string `json:"term"`
}

// Learning, Content
type VectoriseRequest struct {
	Language   string   `json:"language"`
	Vectorise  []string `json:"vectorise"`
	AnyMatch   bool     `json:"any"`
	ExactMatch bool     `json:"exact"`
}

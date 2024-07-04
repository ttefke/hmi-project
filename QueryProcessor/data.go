package main

type CourseOverview struct {
	Courses []CourseData `json:"courses"`
}

type CourseData struct {
	MatchRate          float64 `json:"matchRate"`
	PageNumber         int     `json:"pageNumber"`
	Title              string  `json:"title"`
	Instructor         string  `json:"instructor"`
	LearningObjectives string  `json:"learningObjectives"`
}

func (a CourseData) equals(b CourseData) bool {
	if a.PageNumber != b.PageNumber {
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
	Elective   string `json:"elective"`
	AnyMatch   bool   `json:"any"`
	ExactMatch bool   `json:"exact"`
}

type TermRequest struct {
	Term       string `json:"term"`
	AnyMatch   bool   `json:"any"`
	ExactMatch bool   `json:"exact"`
}

// Learning, Content
type VectoriseRequest struct {
	Language   string   `json:"language"`
	Vectorise  []string `json:"vectorise"`
	AnyMatch   bool     `json:"any"`
	ExactMatch bool     `json:"exact"`
}

type FreeFormRequest struct {
	Query string `json:"query"`
}

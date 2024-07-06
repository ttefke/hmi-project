package main

import (
	"errors"
	"log"
	"slices"
)

func extractNotStatements(query []QueryExpression) ([]QueryExpression, error) {
	notStatements := make([]QueryExpression, 0)
	for index, facet := range query {
		// handle error facet
		if facet.facet == UNKNOWN || facet.facet == ERROR ||
			(facet.facet == NOT && index == len(query)) {
			return []QueryExpression{}, errors.New("invalid search")
		}

		// add next facet if current facet is 'not'
		if facet.facet == NOT && index < len(query)-1 {
			notStatements = append(notStatements, query[index+1])
		}
	}
	return notStatements, nil
}

func extractOrStatements(query []QueryExpression) ([]QueryExpression, error) {
	orStatements := make([]QueryExpression, 0)

	for index, facet := range query {
		if facet.facet == UNKNOWN || facet.facet == ERROR ||
			(facet.facet == NOT && index == len(query)) ||
			(facet.facet == OR && index == len(query)) ||
			(facet.facet == OR && index == 0) {
			return []QueryExpression{}, errors.New("invalid search")
		}

		// prevent queries like not ... or ... (can not use facet twice)
		if index > 1 && facet.facet == OR && query[index-2].facet == NOT {
			return []QueryExpression{}, errors.New("invalid search")
		}

		if facet.facet == OR {
			// in nested or queries like ... or ... or..., prevent facets
			// from being added twice
			if !slices.Contains(orStatements, query[index-1]) {
				orStatements = append(orStatements, query[index-1])
			}
			orStatements = append(orStatements, query[index+1])
		}
	}

	return orStatements, nil
}

func extractAndStatements(query []QueryExpression) ([]QueryExpression, error) {
	andStatements := make([]QueryExpression, 0)

	// only one facet
	if len(query) == 1 {
		return query, nil
	}

	// otherwise, iterate over facets
	for index, facet := range query {
		if facet.facet == UNKNOWN || facet.facet == ERROR {
			return []QueryExpression{}, errors.New("invalid search")
		}

		// do not add not/or facets
		if facet.facet == NOT || facet.facet == OR {
			continue
		}

		if index == 0 {
			// append first facet unless second one is an or statement
			if query[1].facet != OR {
				andStatements = append(andStatements, facet)
			}
		} else if index == len(query)-1 {
			// append last facet unless the facet before is either or or not
			if query[index-1].facet != NOT && query[index-1].facet != OR {
				andStatements = append(andStatements, facet)
			}
		} else {
			// append facet unless facet before or after it is 'or' or the previous facet is 'not'
			if query[index-1].facet != OR && query[index+1].facet != OR && query[index-1].facet != NOT {
				andStatements = append(andStatements, facet)
			}
		}
	}

	return andStatements, nil
}

func handleStatements(query []QueryExpression) ([]CourseData, error) {
	notStatements, err := extractNotStatements(query)
	if err != nil {
		log.Println("Error while extracting not statements:", err)
	}

	orStatements, err := extractOrStatements(query)
	if err != nil {
		log.Println("Error while extracting or statements:", err)
	}

	andStatements, err := extractAndStatements(query)
	if err != nil {
		log.Println("Error while extracting and statements:", err)
	}

	log.Println("Processing query:", query)
	log.Println("Not statements:", notStatements)
	log.Println("Or statements:", orStatements)
	log.Println("And statements:", andStatements)

	// result container
	courses := []CourseData{}

	// only one statement
	if len(notStatements) == 0 && len(orStatements) == 0 &&
		len(andStatements) == 1 {
		data, err := handleFacet(andStatements[0])
		if err != nil {
			log.Println("Could not handle first and facet:", err)
			return []CourseData{}, err
		}
		return data, nil
	}

	// run or statements
	for _, facet := range orStatements {
		data, err := handleFacet(facet)
		if err != nil {
			log.Println("Could not handle or facet:", err)
			return []CourseData{}, err
		}
		courses = or(courses, data)
	}

	// run not statements
	for index, facet := range notStatements {
		if len(orStatements) == 0 && index == 0 {
			// no previous statements -> get all data and run the NOT operation afterwards
			data, err := handleFacet(QueryExpression{facet: INSTRUCTOR, operand: ""})
			if err != nil {
				log.Println("Could not handle not facet:", err)
				return []CourseData{}, err
			}
			courses = append(courses, data...)
		}
		data, err := handleFacet(facet)
		if err != nil {
			log.Println("Could not handle not facet:", err)
			return []CourseData{}, err
		}
		courses = not(courses, data)
	}

	// run and statements
	for index, facet := range andStatements {
		if len(orStatements) == 0 && len(notStatements) == 0 && index == 0 {
			// no previous statements -> get all data and run the AND operation afterwards
			data, err := handleFacet(QueryExpression{facet: INSTRUCTOR, operand: ""})
			if err != nil {
				log.Println("Could not run fist and facet:", err)
				return []CourseData{}, err
			}
			courses = append(courses, data...)
		}
		data, err := handleFacet(facet)
		if err != nil {
			log.Println("Could not run and facet:", err)
			return []CourseData{}, err
		}
		courses = and(courses, data)
	}

	return courses, nil
}

func and(a, b []CourseData) []CourseData {
	result := make([]CourseData, 0)
	for _, course := range a {
		if contains(course, b) {
			result = append(result, course)
		}
	}
	return result
}

func or(a, b []CourseData) []CourseData {
	return append(a, b...)
}

func not(courses, coursesToRemove []CourseData) []CourseData {
	//remove all courses from list matching the facet
	result := make([]CourseData, 0)
	for _, course := range courses {
		if !contains(course, coursesToRemove) {
			result = append(result, course)
		}
	}
	return result
}

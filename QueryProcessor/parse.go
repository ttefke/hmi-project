package main

import (
	"strings"
)

func parse(query string) []QueryExpression {
	var parsedQuery []QueryExpression = make([]QueryExpression, 0)
	var currentExpression QueryExpression = QueryExpression{facet: UNKNOWN, operand: ""}
	var facetString = ""

	for i := 0; i < len(query); i++ {
		character := string(query[i])
		switch character {
		case "+":
			// ignored, this is the case unless or/not operation specified
		case "|":
			// store last facet
			if currentExpression.facet == UNKNOWN && len(facetString) > 0 {
				currentExpression.facet = ERROR
			}
			if currentExpression.facet != UNKNOWN {
				parsedQuery = append(parsedQuery, currentExpression)
			}

			// add or facet
			parsedQuery = append(parsedQuery, QueryExpression{facet: OR, operand: "|"})

			// clean data
			currentExpression = QueryExpression{facet: UNKNOWN, operand: ""}
			facetString = ""
		case "-":
			// store last facet
			if currentExpression.facet == UNKNOWN && len(facetString) > 0 {
				currentExpression.facet = ERROR
			}
			if currentExpression.facet != UNKNOWN {
				parsedQuery = append(parsedQuery, currentExpression)
			}

			// add or facet
			parsedQuery = append(parsedQuery, QueryExpression{facet: NOT, operand: "-"})

			// clean data
			currentExpression = QueryExpression{facet: UNKNOWN, operand: ""}
			facetString = ""
		case " ":
			// Facet is known and operand is present -> store facet
			if currentExpression.facet != UNKNOWN && len(currentExpression.operand) > 0 {
				parsedQuery = append(parsedQuery, currentExpression)
				currentExpression = QueryExpression{facet: UNKNOWN, operand: ""}
				facetString = ""
			}
			// Facet is unknown but operand is present -> assume the operand of the last facet contains space
			if currentExpression.facet == UNKNOWN && len(facetString) > 0 {
				if len(parsedQuery) > 0 {
					parsedQuery[len(parsedQuery)-1].operand += " " + facetString
					facetString = ""
				} else {
					currentExpression.facet = ERROR
				}
			}
		case ":":
			switch strings.ToLower(facetString) {
			case "and":
				// ignored
			case "or":
				currentExpression.facet = OR
				currentExpression.operand = "|"
			case "not":
				currentExpression.facet = NOT
				currentExpression.operand = "-"
			case "intitle":
				currentExpression.facet = INTITLE
			case "instructor":
				currentExpression.facet = INSTRUCTOR
			case "learning":
				currentExpression.facet = LEARNING
			case "content":
				currentExpression.facet = CONTENT
			case "elective":
				currentExpression.facet = ELECTIVE
			case "term":
				currentExpression.facet = TERM
			default:
				currentExpression.facet = ERROR
			}
		default:
			if currentExpression.facet == UNKNOWN {
				facetString += character
			} else {
				currentExpression.operand += character
			}
		}
	}
	// Facet is unknown but facet string is present -> assume the operand of the last facet contains space
	if currentExpression.facet == UNKNOWN && len(facetString) > 0 {
		if len(parsedQuery) > 0 {
			parsedQuery[len(parsedQuery)-1].operand += " " + facetString
			facetString = ""
		} else {
			currentExpression.facet = ERROR
		}
	}
	if currentExpression.facet != UNKNOWN {
		parsedQuery = append(parsedQuery, currentExpression)
	}

	return parsedQuery
}

func isValid(parsedQuery []QueryExpression) bool {
	for _, facet := range parsedQuery {
		if facet.facet == ERROR {
			return false
		}
	}
	return true
}

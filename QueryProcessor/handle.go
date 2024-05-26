package main

import (
	"bytes"
	"encoding/json"
	"errors"
	"io"
	"log"
	"net/http"
	"strings"
)

func handleFacet(expression QueryExpression) ([]CourseData, error) {
	switch expression.facet {
	case INTITLE:
		return handleTitle(expression.operand)
	case INSTRUCTOR:
		return handleInstructor(expression.operand)
	case LEARNING:
		return handleLearning(expression.operand)
	case CONTENT:
		return handleContent(expression.operand)
	case ELECTIVE:
		return handleElective(expression.operand)
	case TERM:
		return handleTerm(expression.operand)
	default:
		return []CourseData{}, errors.New("unknown facet")
	}
}
func handleTitle(title string) ([]CourseData, error) {
	requestedTitle := TitleRequest{Intitle: title}
	requestedTitleJson, err := json.Marshal(requestedTitle)
	if err != nil {
		log.Println("Could not encode title in JSON:", err)
		return []CourseData{}, err
	}

	return handleRequest("/course_by_title/", requestedTitleJson)
}

func handleInstructor(instructor string) ([]CourseData, error) {
	requestedInstructor := InstructorRequest{Instructor: instructor}
	requestedInstructorJson, err := json.Marshal(requestedInstructor)
	if err != nil {
		log.Println("Could not encode instructor in JSON:", err)
		return []CourseData{}, err
	}

	return handleRequest("/course_by_instructor/", requestedInstructorJson)
}

func handleLearning(learningObjective string) ([]CourseData, error) {
	learningObjectiveSlice := []string{learningObjective}
	requestedLearningObjective := VectoriseRequest{Language: "en", Vectorise: learningObjectiveSlice}
	requestedLearningObjectiveJson, err := json.Marshal(requestedLearningObjective)
	if err != nil {
		log.Println("Could not encode learning objective in JSON:", err)
		return []CourseData{}, err
	}

	return handleRequest("/course_by_learning/", requestedLearningObjectiveJson)
}

func handleContent(content string) ([]CourseData, error) {
	contentSlice := []string{content}
	requestedContentObjective := VectoriseRequest{Language: "en", Vectorise: contentSlice}
	requestedContentObjectiveJson, err := json.Marshal(requestedContentObjective)
	if err != nil {
		log.Println("Could not encode course contents in JSON:", err)
		return []CourseData{}, err
	}

	return handleRequest("/course_by_contents/", requestedContentObjectiveJson)
}

func handleElective(elective string) ([]CourseData, error) {
	elective = strings.ToLower(elective)
	requestedElective := ElectiveRequest{Elective: elective == "true"}
	requestedElectiveJson, err := json.Marshal(requestedElective)
	if err != nil {
		log.Println("Could not encode elective in JSON:", err)
		return []CourseData{}, err
	}

	return handleRequest("/course_by_area/", requestedElectiveJson)
}

func handleTerm(term string) ([]CourseData, error) {
	requestedTerm := TermRequest{Term: term}
	requestedTermJson, err := json.Marshal(requestedTerm)
	if err != nil {
		log.Println("Could not encode term in JSON:", err)
		return []CourseData{}, err
	}

	return handleRequest("/course_by_term/", requestedTermJson)
}

func handleRequest(route string, jsonData []byte) ([]CourseData, error) {
	request, err := http.NewRequest(http.MethodPost, backendUrl+route, bytes.NewBuffer(jsonData))
	if err != nil {
		log.Println("Could not create backend request: ", err)
		return []CourseData{}, err
	}

	request.Header.Set("Content-Type", "application/json")

	response, err := http.DefaultClient.Do(request)
	if err != nil {
		log.Println("Could not send backend request: ", err)
		return []CourseData{}, err
	}

	body, err := io.ReadAll(response.Body)
	if err != nil {
		log.Println("Could not read response to backend request: ", err)
		return []CourseData{}, err
	}
	defer response.Body.Close()

	var overview CourseOverview
	err = json.Unmarshal(body, &overview)
	if err != nil {
		return []CourseData{}, errors.New("could not decode backend response")
	}

	return overview.Courses, nil
}

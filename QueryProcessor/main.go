package main

import (
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
	"os"

	"github.com/gorilla/mux"
)

var backendUrl string

func QueryHandler(w http.ResponseWriter, r *http.Request) {
	query := r.URL.Query().Get("query")

	// Empty object returned if query is empty or invalid
	var coursesOverview CourseOverview
	coursesOverview.Courses = []CourseData{}

	// Parse query if present
	if len(query) > 0 {
		statements := parse(query)

		// Interpret and handle facets if present
		if containsFacets(statements) {
			courses, err := handleStatements(statements)
			if err != nil {
				log.Println("Error while processing query:", err)
			}
			coursesOverview = CourseOverview{Courses: courses}
		} else {
			// Interpret query as free-form query
			courses, err := handleFreeFormQuery(query)
			if err != nil {
				log.Println("Error while processing query:", err)
			}
			coursesOverview = CourseOverview{Courses: courses}
		}
	}

	decodedCourses, err := json.Marshal(coursesOverview)
	if err != nil {
		log.Println("Error while marshalling json:", err)
	}

	// Output matching courses
	w.Header().Add("Content-Type", "application/json")
	fmt.Fprint(w, string(decodedCourses))
}

func TitlesHandler(w http.ResponseWriter, r *http.Request) {
	PassthroughHandler(w, "/get_course_titles")
}
func InstructorsHandler(w http.ResponseWriter, r *http.Request) {
	PassthroughHandler(w, "/get_instructors")
}

func PassthroughHandler(w http.ResponseWriter, route string) {
	request, err := http.NewRequest(http.MethodGet, backendUrl+route, nil)
	if err != nil {
		log.Println("Could not create backend request: ", err)
	}

	request.Header.Set("Content-Type", "application/json")

	response, err := http.DefaultClient.Do(request)
	if err != nil {
		log.Println("Could not send backend request: ", err)
	}

	body, err := io.ReadAll(response.Body)
	if err != nil {
		log.Println("Could not read response to backend request: ", err)
	}
	defer response.Body.Close()
	fmt.Fprint(w, string(body))
}

func main() {
	envSet := false
	backendUrl, envSet = os.LookupEnv("BACKEND_URL")
	if !envSet {
		log.Fatalln("Environment variable for BACKEND_URL is not set")
		os.Exit(1)
	}

	r := mux.NewRouter()
	r.HandleFunc("/query", QueryHandler)
	r.HandleFunc("/titles", TitlesHandler)
	r.HandleFunc("/instructors", InstructorsHandler)

	log.Println("Started Query Processor")

	err := http.ListenAndServe(":8080", r)
	if err != nil {
		log.Fatalln("Query Processor failed:", err)
	}
}

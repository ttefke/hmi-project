package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"

	"github.com/gorilla/mux"
)

var backendUrl string

func QueryHandler(w http.ResponseWriter, r *http.Request) {
	query := r.URL.Query().Get("query")
	fmt.Println(query)
	if len(query) == 0 {
		fmt.Fprintf(w, "No query provided")
		return
	}
	statements := parse(query)
	if isValid(statements) {
		courses, err := handleStatements(statements)
		if err != nil {
			log.Println("Error while processing query:", err)
		}
		coursesOverview := CourseOverview{Courses: courses}
		decodedCourses, err := json.Marshal(coursesOverview)
		if err != nil {
			log.Println("Error while marshalling json:", err)
		}
		fmt.Fprint(w, string(decodedCourses))
	} else {
		fmt.Fprintf(w, "Invalid query!")
	}
}

func main() {
	envSet := false
	backendUrl, envSet = os.LookupEnv("BACKEND_URL")
	if !envSet {
		log.Fatalln("Environment variable for BACKEND_URL is not set")
		os.Exit(1)
	}

	r := mux.NewRouter()
	r.HandleFunc("/", QueryHandler)

	log.Println("Started Query Processor")

	err := http.ListenAndServe(":8080", r)
	if err != nil {
		log.Fatalln("Query Processor failed:", err)
	}
}

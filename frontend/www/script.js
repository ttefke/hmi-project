const API_BASE_URL = "/query"; // Replace with your actual API base URL

let titleSuggestions = []
let instructorSuggestions = []
const electiveSuggestions = [
  "true",
  "false"
]
const termSuggestions = [
  "summer",
  "winter"
]
const facets = ["intitle", "instructor", "learning", "content", "elective", "term"];
let suggestions = [];

async function fetchData() {
  try {
    // fetch lecture titles
    const titleSuggestionUrl = `${API_BASE_URL}/titles`;  
    const titleResponse = await fetch(titleSuggestionUrl);
    if (!titleResponse.ok) {
      throw new Error(`HTTP error! status: ${titleResponse.status}`);
    }
    const titleData = await titleResponse.json();
    titleSuggestions = titleData.data;

    // fetch instructors
    const instructorSuggestionsUrl = `${API_BASE_URL}/instructors`;  
    const instructorResponse = await fetch(instructorSuggestionsUrl);
    if (!instructorResponse.ok) {
      throw new Error(`HTTP error! status: ${instructorResponse.status}`);
    }
    const instructorData = await instructorResponse.json();
    instructorSuggestions = instructorData.data;

    suggestions = suggestions.concat(titleSuggestions);
    suggestions = suggestions.concat(instructorSuggestions);
    suggestions = suggestions.concat(electiveSuggestions);
    suggestions = suggestions.concat(termSuggestions);
    suggestions = suggestions.concat(facets);
  } catch (error) {
    console.error("Error fetching data: ", error);
  }  
}
fetchData();

const searchForm = document.getElementById("search-form");
const searchBox = document.getElementById("search-box");
const suggestionsContainer = document.getElementById("suggestions");

function showSuggestions() {
  var input = searchBox.value.toLowerCase().trim();
  suggestionsContainer.innerHTML = "";
  
  const splitInput = input.split(/ |:|-|\*|\|/)
  const lastInput = splitInput[splitInput.length -1];

  if (lastInput.length > 2) {
    let currentSuggestions = suggestions.filter((word) => word.toLowerCase().startsWith(lastInput.toLowerCase()));
      if (currentSuggestions.length > 0) {
        suggestionsContainer.style.display = "block";
        
        currentSuggestions.forEach((suggestion) => {
          const suggestionItem = document.createElement("li");
          suggestionItem.textContent = suggestion;
          suggestionItem.addEventListener("click", () => {
            let remainingInput = input.slice(0, - lastInput.length);
            searchBox.value = remainingInput + suggestion;
            suggestionsContainer.style.display = "none";
          });
          suggestionsContainer.appendChild(suggestionItem);
        });
      } else {
        suggestionsContainer.style.display = "none";
      }
    }
  }

searchBox.addEventListener("input", showSuggestions);

const searchResult = document.getElementById("search-result");
const resultTableBody = document.querySelector("#result-table tbody");
const searchButton = document.getElementById("search-button");

let keyword = "";
let pageNumber = 1

async function searchCourse() {
  keyword = searchBox.value.trim();
  if (!keyword) {
    alert("Please enter a query to search.");
    return;
  }
  const url = `${API_BASE_URL}/query?query=${keyword}`;

  try {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    console.log(data);

    if (pageNumber === 1) resultTableBody.innerHTML = ""; // Clear previous results

    if (data.courses && data.courses.length > 0) {
      data.courses.forEach((course) => {
        const row = document.createElement("tr");

        const titleCell = document.createElement("td");
        titleCell.textContent = course.title || "No Title";

        const instructorCell = document.createElement("td");
        instructorCell.textContent = course.instructor || "Unknown";

        const objectivesCell = document.createElement("td");
        objectivesCell.textContent =
          course.learningObjectives || "Not specified";

        const matchRateCell = document.createElement("td");
        matchRateCell.textContent = `${Math.round(course.matchRate * 100)}%`;

        if (course.matchRate >= 0.8) {
          row.classList.add("green");
        } else if (course.matchRate >= 0.5) {
          row.classList.add("yellow");
        } else {
          row.classList.add("red");
        }

        row.appendChild(titleCell);
        row.appendChild(instructorCell);
        row.appendChild(objectivesCell);
        row.appendChild(matchRateCell);

        // Add event listener to row for redirection
        row.addEventListener("click", () => {
          const pdfUrl = course.pdfUrl;
          const pageNumber = course.pageNumber;
          if (pdfUrl && pageNumber) {
            window.location.href = `${pdfUrl}#page=${pageNumber}`;
          } else if (pdfUrl) {
            window.location.href = pdfUrl;
          }
        });

        resultTableBody.appendChild(row);
      });

      // Show the result table and "Show More" button
      searchResult.style.display = "block";
    } else {
      // Hide the result table and "Show More" button if no results
      searchResult.style.display = "none";
    }
  } catch (error) {
    console.error("Error fetching data: ", error);
    alert("An error occurred while fetching data. Please try again later.");
  }
}

searchButton.addEventListener("click", () => {
  pageNumber = 1; // Reset page number when performing new search
  searchCourse();
});

// Event listener for the search button click
searchButton.addEventListener("mousedown", () => {
  searchButton.style.backgroundColor = "#000"; // Change to black on click
});

searchButton.addEventListener("mouseup", () => {
  searchButton.style.backgroundColor = "#ff3929"; // Change back to original color
});

const API_BASE_URL = "/query"; // Replace with your actual API base URL

let titleSuggestions = []
let instructorSuggestions = []
const electiveSuggestions = [
  "true",
  "false"
]
const termSuggestions = [
  "summer",
  "winter",
  "1",
  "2",
  "3"
]

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

  const facets = ["intitle", "instructor", "elective", "term"];
  
  if (input) {
    const splitInput = input.split(/ |:/);
    const lastInput = splitInput[splitInput.length -1];

    let suggestions = [];

    // last input is a facet handled here
    if (splitInput.length >= 1) {
      let isFacet = false;
      let isSuffixed = false;
      let facet = "";

      // input is facet handled here, facet is suffexed with a colon
      if ((splitInput.length > 1) && (lastInput.length == 0) && (facets.indexOf(splitInput[splitInput.length -2]) > -1)) {
        isFacet = true;
        isSuffixed = true;
        facet = splitInput[splitInput.length -2];
      // input is a facet handled here, facet is not suffixed with a colon
      } else if ((lastInput.length > 0) && (facets.indexOf(lastInput) > -1)) {
        isFacet = true;
        facet = lastInput;
      }

      if (isFacet) {
          switch (facet) {
          case "intitle":
            suggestions = titleSuggestions;
            break;
          case "instructor":
            suggestions = instructorSuggestions;
            break;
          case "elective":
            suggestions = electiveSuggestions;
            break;
          case "term":
            suggestions = termSuggestions;
            break;
        }

        if (suggestions.length > 0) {
          suggestionsContainer.style.display = "block";
          
          suggestions.forEach((suggestion) => {
            const suggestionItem = document.createElement("li");
            suggestionItem.textContent = suggestion;
            suggestionItem.addEventListener("click", () => {
              if (isSuffixed) {
                searchBox.value = input + suggestion;
              } else {
                searchBox.value = input + ":" + suggestion;
              }
              suggestionsContainer.style.display = "none";
            });
            suggestionsContainer.appendChild(suggestionItem);
          });
        } else {
          suggestionsContainer.style.display = "none";
        }
      }
    }
  }
}

searchBox.addEventListener("input", showSuggestions);

const searchResult = document.getElementById("search-result");
const resultTableBody = document.querySelector("#result-table tbody");
const showMoreBtn = document.getElementById("show-more-btn");
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
      showMoreBtn.style.display = "block";
    } else {
      // No courses found
      const noResultRow = resultTableBody.insertRow();
      const noResultCell = noResultRow.insertCell();
      noResultCell.textContent = "No results found";
      noResultCell.colSpan = "4";

      searchResult.style.display = "block";
      showMoreBtn.style.display = "none";
    }

    // Check if there are more results to show
    if (data.hasMore) {
      pageNumber++;
      showMoreBtn.style.display = "block";
    } else {
      showMoreBtn.style.display = "none";
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

function showMore() {
  searchCourse();
}

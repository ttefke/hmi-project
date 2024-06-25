const searchForm = document.getElementById("search-form");
const searchBox = document.getElementById("search-box");
const searchResult = document.getElementById("search-result");
const resultTableBody = document.querySelector("#result-table tbody");
const showMoreBtn = document.getElementById("show-more-btn");
const searchButton = document.getElementById("search-button");

let keyword = "";
let pageNumber = 1;

// Replace with your actual API base URL
const API_BASE_URL = ""; 

async function searchCourse() {
  keyword = searchBox.value.trim();
  if (!keyword) {
    alert("Please enter a keyword to search.");
    return;
  }
const url = `${API_BASE_URL}/query/?query=${encodeURIComponent(
    keyword
  
  )};

  try {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    console.log(data); // Log the data for debugging

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

        resultTableBody.appendChild(row);
      });

      // Show the result table and "Show More" button
      searchResult.style.display = "block";
      showMoreBtn.style.display = "block";
    } else {
      // Hide the result table and "Show More" button if no results
      searchResult.style.display = "none";
      showMoreBtn.style.display = "none";
    }
  } catch (error) {
    console.error("Error fetching data: ", error);
  }
}

// Event listener for the search form submission
searchForm.addEventListener("submit", (event) => {
  event.preventDefault();
  pageNumber = 1; // Reset page number for new search
  searchCourse();
});

// Event listener for the "Show More" button
showMoreBtn.addEventListener("click", () => {
  pageNumber++;
  searchCourse();
});

// Event listener for the search button click
searchButton.addEventListener("mousedown", () => {
  searchButton.style.backgroundColor = "#000"; // Change to black on click
});

searchButton.addEventListener("mouseup", () => {
  searchButton.style.backgroundColor = "#ff3929"; // Change back to original color
});

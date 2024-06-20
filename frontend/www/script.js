const searchForm = document.getElementById("search-form");
const searchBox = document.getElementById("search-box");
const searchResult = document.getElementById("search-result");
const showMoreBtn = document.getElementById("show-more-btn");
const searchButton = document.getElementById("search-button");

let keyword = "";
let pageNumber = 1;

async function searchCourse() {
  keyword = searchBox.value.trim();
  if (!keyword) {
    alert("Please enter a keyword to search.");
    return;
  }

  const url = `/query/?query=${encodeURIComponent(
    keyword
  )}`;

  try {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    console.log(data); // Log the data for debugging

    if (pageNumber === 1) searchResult.innerHTML = ""; // Clear previous results

    if (data.courses && data.courses.length > 0) {
      data.courses.forEach((course) => {
        const courseDiv = document.createElement("div");
        courseDiv.classList.add("course-result");

        const title = document.createElement("h2");
        title.textContent = course.title || "No Title";

        const instructor = document.createElement("p");
        instructor.textContent = `Instructor: ${
          course.instructor || "Unknown"
        }`;

        const learningObjectives = document.createElement("p");
        learningObjectives.textContent = `Learning Objectives: ${
          course.learningObjectives || "Not specified"
        }`;

        const matchRate = document.createElement("p");
        matchRate.textContent = `Match Rate: ${course.matchRate}`;

        courseDiv.appendChild(title);
        courseDiv.appendChild(instructor);
        courseDiv.appendChild(learningObjectives);
        courseDiv.appendChild(matchRate);

        searchResult.appendChild(courseDiv);
      });

      // Show the "Show More" button if more results are available
      showMoreBtn.style.display = "block";
    } else {
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

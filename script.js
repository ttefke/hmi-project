const searchForm = document.getElementById("search-form");
const searchBox = document.getElementById("search-box");
const searchResult = document.getElementById("search-result");
const showMoreBtn = document.getElementById("show-more-btn");

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
  )}&pageNumber=${pageNumber}`;

  try {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    console.log(data); // Log the data for debugging

    if (pageNumber === 1) searchResult.innerHTML = ""; // Clear previous results

    data.courses.forEach((course) => {
      const courseDiv = document.createElement("div");
      courseDiv.classList.add("course-result");

      const title = document.createElement("h2");
      title.textContent = course.title;

      const instructor = document.createElement("p");
      instructor.textContent = `Instructor: ${course.instructor}`;

      const learningObjectives = document.createElement("p");
      learningObjectives.textContent = `Learning Objectives: ${course.learningObjectives}`;

      const matchRate = document.createElement("p");
      matchRate.textContent = `Match Rate: ${course.matchRate}`;

      courseDiv.appendChild(title);
      courseDiv.appendChild(instructor);
      courseDiv.appendChild(learningObjectives);
      courseDiv.appendChild(matchRate);

      searchResult.appendChild(courseDiv);
    });

    // Show the "Show More" button if more results are available
    if (data.courses.length > 0) {
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

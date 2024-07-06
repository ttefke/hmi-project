const suggestions = [
  "Agile Software Development",
  "Prof. Dr. Englmeier",
  "Computer Graphics 1 (Computergraphik 1)",
  "Prof. Hartmut Seichter, PhD",
  "Computational Intelligence",
  "Prof. Dr. Martin Golz",
  "Distributed Systems (Verteilte Systeme)",
  "Prof. Dr. Erwin Neuhardt",
  "Prof. Ralf C. Staudemeyer, Ph.D.",
  "IT Security",
  "Mobile Systems (Mobile Systeme)",
  "Prof. Dr. Michael Cebulla",
  "Service-Oriented Networks",
  "Prof. Dr.-Ing. Heinz-Peter Höller",
  "Signals and Systems",
  "Prof. Dr. Martin Golz",
  "Web Applications",
  "Prof. Dr. Erwin Neuhardt",
  "IT-Security (adv. chapters)",
  "Distributed Systems Advanced Chapters (Vertiefung Verteilte Systeme)",
  "Semantic Technologies in Distributed Systems (Semantische Technologien in verteilten Systemen)",
  "Software Quality (Softwarequalität)",
  "Prof. Dr. Erwin Neuhardt",
  "Text Mining and Search",
  "Prof. Dr. Englmeier",
  "eBusiness",
  "Prof. Dr. Thomas Urban",
  "Human-Computer Interaction",
  "Prof. Dr. Englmeier",
  "Image Processing 1",
  "Prof. Dr. Klaus Chantelau",
  "Image Processing 2",
  "Media Production 1",
];

const specificSuggestions = {
  "instructor:englmeier intitle:": [
    "Agile Software Development",
    "Text Mining and Search",
    "Human-Computer Interaction",
  ],
  "instructor:seichter intitle:": ["Computer Graphics 1 (Computergraphik 1)"],
  "instructor:golz intitle:": [
    "Computational Intelligence",
    "Signals and Systems",
  ],
  "instructor:neuhardt intitle:": [
    "Web Applications",
    "Distributed Systems (Verteilte Systeme)",
    "Software Quality (Softwarequalität)",
  ],
  "instructor:staudemeyer intitle:": [
    "IT Security",
    "IT-Security (adv. chapters)",
  ],
  "instructor:urban intitle:": ["eBusiness"],
  "instructor:chantelau intitle:": [
    "Image Processing 1",
    "Image Processing 2",
    "Media Production 1",
  ],
  "instructor:cebulla intitle:": [
    "Semantic Technologies in Distributed Systems (Semantische Technologien in verteilten Systemen)",
    "Distributed Systems Advanced Chapters (Vertiefung Verteilte Systeme)",
    "Mobile Systems (Mobile Systeme)",
  ],
  "instructor:höller intitle:": [
    "Prof. Dr.-Ing. Heinz-Peter Höller",
    "Service-Oriented Networks",
  ],
  instructor: [
    "Prof. Dr. Englmeier",
    "Prof. Hartmut Seichter, PhD",
    "Prof. Dr. Martin Golz",
    "Prof. Dr. Erwin Neuhardt",
    "Prof. Ralf C. Staudemeyer, Ph.D.",
    "Prof. Dr. Thomas Urban",
    "Prof. Dr. Klaus Chantelau",
    "Prof. Dr. Michael Cebulla",
    "Prof. Dr.-Ing. Heinz-Peter Höller",
  ],
  "intitle:": [
    "Agile Software Development",
    "Computer Graphics 1 (Computergraphik 1)",
    "Computational Intelligence",
    "Distributed Systems (Verteilte Systeme)",
    "IT Security",
    "Mobile Systems (Mobile Systeme)",
    "Service-Oriented Networks",
    "Signals and Systems",
    "Web Applications",
    "IT-Security (adv. chapters)",
    "Distributed Systems Advanced Chapters (Vertiefung Verteilte Systeme)",
    "Semantic Technologies in Distributed Systems (Semantische Technologien in verteilten Systemen)",
    "Software Quality (Softwarequalität)",
    "Text Mining and Search",
    "eBusiness",
    "Human-Computer Interaction",
    "Image Processing 1",
    "Image Processing 2",
    "Media Production 1",
  ],
  "term:summer": [
    "Media Production 1",
    "eBusiness",
    "Human-Computer Interaction",
    "Computational Intelligence",
    "Service-Oriented Networks",
    "Mobile Systems (Mobile Systeme)",
  ],
  "term:winter": [
    "Agile Software Development",
    "Computer Graphics 1 (Computergraphik 1)",
    "Distributed Systems (Verteilte Systeme)",
    "IT Security",
    "Signals and Systems",
    "Web Applications",
    "IT-Security (adv. chapters)",
    "Distributed Systems Advanced Chapters (Vertiefung Verteilte Systeme)",
    "Semantic Technologies in Distributed Systems (Semantische Technologien in verteilten Systemen)",
    "Software Quality (Softwarequalität)",
    "Text Mining and Search",
    "Image Processing 1",
    "Image Processing 2",
  ],
  elective: [
    "Image Processing 1",
    "Image Processing 2",
    "Media Production 1",
    "IT-Security (adv. chapters)",
    "Semantic Technologies in Distributed Systems (Semantische Technologien in verteilten Systemen)",
    "Software Quality (Softwarequalität)",
    "Text Mining and Search",
    "eBusiness",
    "Human-Computer Interaction",
  ],
};

const searchForm = document.getElementById("search-form");
const searchBox = document.getElementById("search-box");
const suggestionsContainer = document.getElementById("suggestions");

function showSuggestions() {
  const input = searchBox.value.toLowerCase().trim();
  suggestionsContainer.innerHTML = "";

  if (input) {
    let filteredSuggestions;

    if (input in specificSuggestions) {
      filteredSuggestions = specificSuggestions[input];
    } else {
      filteredSuggestions = suggestions.filter((suggestion) =>
        suggestion.toLowerCase().includes(input)
      );
    }

    if (filteredSuggestions.length > 0) {
      suggestionsContainer.style.display = "block";
    } else {
      suggestionsContainer.style.display = "none";
    }

    filteredSuggestions.forEach((suggestion) => {
      const suggestionItem = document.createElement("li");
      suggestionItem.textContent = suggestion;
      suggestionItem.addEventListener("click", () => {
        searchBox.value = suggestion;
        suggestionsContainer.style.display = "none";
      });
      suggestionsContainer.appendChild(suggestionItem);
    });
  } else {
    suggestionsContainer.style.display = "none";
  }
}

searchBox.addEventListener("input", showSuggestions);

const searchResult = document.getElementById("search-result");
const resultTableBody = document.querySelector("#result-table tbody");
const showMoreBtn = document.getElementById("show-more-btn");
const searchButton = document.getElementById("search-button");

let keyword = "";
let pageNumber = 1;

const API_BASE_URL = ""; // Replace with your actual API base URL

async function searchCourse() {
  keyword = searchBox.value.trim();
  if (!keyword) {
    alert("Please enter a keyword to search.");
    return;
  }
  const url = `${API_BASE_URL}/query/?query=${encodeURIComponent(keyword)}`;

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

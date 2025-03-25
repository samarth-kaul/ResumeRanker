// Function to fetch job descriptions from the API
async function fetchJobDescriptions() {
    try {
        const response = await fetch('http://127.0.0.1:8000/api/jobs/');  // Adjust with actual API URL
        const data = await response.json();
        const jobDescriptionSelect = document.getElementById('job-description');
        
        if (data.status) {
            data.data.forEach(job => {
                const option = document.createElement('option');
                option.value = job.id;
                option.textContent = job.job_title;  // Assuming 'job_description' field is returned
                jobDescriptionSelect.appendChild(option);
            });
        } else {
            alert('Failed to load job descriptions');
        }
    } catch (error) {
        console.error('Error fetching job descriptions:', error);
    }
}

// Function to handle resume upload and analyze it
async function analyzeResume() {
    const jobDescription = document.getElementById('job-description').value;
    const resumeFile = document.getElementById('resume-upload').files[0];
    const resultDiv = document.getElementById('result');
    
    if (!jobDescription) {
        resultDiv.innerHTML = 'Please select a job description.';
        resultDiv.style.display = 'block';
        return;
    }

    if (!resumeFile) {
        resultDiv.innerHTML = 'Please upload a resume.';
        resultDiv.style.display = 'block';
        return;
    }

    // Prepare FormData to send to the backend
    const formData = new FormData();
    formData.append('job_description', jobDescription);
    formData.append('resume', resumeFile);

    try {
        const response = await fetch('http://127.0.0.1:8000/api/resume/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken, // CSRF token header
            },
            body: formData
        });
        const result = await response.json();
        
        if (result.status) {
            resultDiv.innerHTML = 'Resume successfully analyzed!';
            resultDiv.style.display = 'block';
        } else {
            resultDiv.innerHTML = 'Error analyzing the resume. Please try again.';
            resultDiv.style.display = 'block';
        }
    } catch (error) {
        console.error('Error analyzing resume:', error);
        resultDiv.innerHTML = 'An error occurred. Please try again.';
        resultDiv.style.display = 'block';
    }
}

// Initialize the page
document.addEventListener('DOMContentLoaded', () => {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    fetchJobDescriptions();

    const submitBtn = document.getElementById('submit-btn');
    submitBtn.addEventListener('click', analyzeResume);
});




// document.addEventListener("DOMContentLoaded", function () {
//     const jobDescriptionDropdown = document.getElementById("jobDescription");
//     const resumeForm = document.getElementById("resumeForm");
//     const resumeInput = document.getElementById("resumeInput");
//     const loadingIndicator = document.getElementById("loading");
//     const resultsDiv = document.getElementById("results");

//     // Fetch Job Descriptions
//     fetch("http://127.0.0.1:8000/api/jobs/")
//         .then(response => response.json())
//         .then(data => {
//             jobDescriptionDropdown.innerHTML = '<option value="">Select a Job Description</option>';
//             if (data.status) {
//                 data.data.forEach(job => {
//                     jobDescriptionDropdown.innerHTML += `<option value="${job.id}">${job.title}</option>`;
//                 });
//             } else {
//                 jobDescriptionDropdown.innerHTML = "<option value=''>No jobs available</option>";
//             }
//         })
//         .catch(error => {
//             console.error("Error fetching job descriptions:", error);
//         });

//     // Handle Resume Submission
//     resumeForm.addEventListener("submit", function (e) {
//         e.preventDefault();

//         const jobDescriptionId = jobDescriptionDropdown.value;
//         if (!jobDescriptionId) {
//             alert("Please select a job description.");
//             return;
//         }

//         const file = resumeInput.files[0];
//         if (!file) {
//             alert("Please upload a resume.");
//             return;
//         }

//         loadingIndicator.style.display = "block";
//         resultsDiv.innerHTML = "";

//         const formData = new FormData();
//         formData.append("resume", file);
//         formData.append("job_description", jobDescriptionId);

//         fetch("http://127.0.0.1:8000/api/resume/", {
//             method: "POST",
//             body: formData
//         })
//         .then(response => response.json())
//         .then(data => {
//             loadingIndicator.style.display = "none";
//             if (data.status) {
//                 resultsDiv.innerHTML = "<p><strong>Analysis Complete:</strong> Resume has been analyzed successfully.</p>";
//             } else {
//                 resultsDiv.innerHTML = "<p>Error analyzing resume. Please try again.</p>";
//             }
//         })
//         .catch(error => {
//             console.error("Error analyzing resume:", error);
//             loadingIndicator.style.display = "none";
//             resultsDiv.innerHTML = "<p>Something went wrong. Try again later.</p>";
//         });
//     });
// });

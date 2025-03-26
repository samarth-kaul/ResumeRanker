let csrfToken;

document.addEventListener('DOMContentLoaded', () => {
    // Get CSRF token
    csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value || '';

    // Fetch job descriptions and populate dropdown
    fetchJobDescriptions();

    // Get submit button and attach event listener
    const submitBtn = document.getElementById('submit-btn');
    if (submitBtn) {
        submitBtn.addEventListener('click', analyzeResume);
    } else {
        console.error('Submit button not found.');
    }
});

// Function to fetch job descriptions
async function fetchJobDescriptions() {
    try {
        const response = await fetch('http://127.0.0.1:8000/api/jobs/', {
            headers: { 'X-CSRFToken': csrfToken },
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        const jobDescriptionSelect = document.getElementById('job-description');

        if (data?.data?.length > 0) {
            data.data.forEach(job => {
                const option = document.createElement('option');
                option.value = job.id;
                option.textContent = job.job_title; // Adjust key as per API response
                jobDescriptionSelect.appendChild(option);
            });
        } else {
            alert('No job descriptions available.');
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
    const loader = document.getElementById('loader');

    // Clear previous results
    resultDiv.innerHTML = '';
    resultDiv.style.display = 'none';

    // Validate user input
    if (!jobDescription) {
        resultDiv.innerHTML = '<span class="error">Please select a job description.</span>';
        resultDiv.style.display = 'block';
        return;
    }

    if (!resumeFile) {
        resultDiv.innerHTML = '<span class="error">Please upload a resume.</span>';
        resultDiv.style.display = 'block';
        return;
    }

    // Show loading spinner
    loader.style.display = 'block';

    // Prepare FormData to send to the backend
    const formData = new FormData();
    formData.append('job_description', jobDescription);
    formData.append('resume', resumeFile);

    console.log('Submitting form with:', { jobDescription, resumeFile });

    try {
        const response = await fetch('http://127.0.0.1:8000/api/resume/', {
            method: 'POST',
            headers: { 'X-CSRFToken': csrfToken }, // Include CSRF token
            body: formData
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const result = await response.json();
        console.log('Server response:', result);

        // Hide loader
        loader.style.display = 'none';

        // Check if result.status is true
        if (result.status) {
            const { rank, skill_match, experience_relevance, project_alignment, education_match,
                core_skills, additional_skills, total_experience, relevant_experience, project_classification,
                education, certifications, missing_skills, experience_gaps } = result.data;

            // Display the analysis result
            resultDiv.innerHTML = `
                <strong>Resume successfully analyzed!</strong>
                <p><strong>Rank:</strong> ${rank}</p>
                <p><strong>Skill Match:</strong> ${skill_match}%</p>
                <p><strong>Experience Relevance:</strong> ${experience_relevance}%</p>
                <p><strong>Project Alignment:</strong> ${project_alignment}%</p>
                <p><strong>Education Match:</strong> ${education_match}%</p>

                <div>
                    <strong>Core Skills:</strong>
                    <ul>
                        ${core_skills.map(skill => `<li>${skill}</li>`).join('')}
                    </ul>
                </div>

                <div>
                    <strong>Additional Skills:</strong>
                    <ul>
                        ${additional_skills.map(skill => `<li>${skill}</li>`).join('')}
                    </ul>
                </div>

                <p><strong>Total Experience:</strong> ${total_experience} years</p>

                <div>
                    <strong>Relevant Experience:</strong>
                    <ul>
                        ${relevant_experience.map(exp => `<li><strong>${exp.job_title}</strong> at ${exp.company} (${exp.duration})</li>`).join('')}
                    </ul>
                </div>

                <div>
                    <strong>Projects:</strong>
                    ${project_classification.map(project => `
                        <div>
                            <p><strong>Project Title:</strong> ${project.title}</p>
                            <p><strong>Domain:</strong> ${project.domain}</p>
                            <p><strong>Role:</strong> ${project.role}</p>
                            <p><strong>Technologies:</strong> ${project.technologies.join(', ')}</p>
                            <p><strong>Achievements:</strong></p>
                            <ul>
                                ${project.achievements.map(ach => `<li>${ach}</li>`).join('')}
                            </ul>
                        </div>
                    `).join('')}
                </div>

                <div>
                    <strong>Education:</strong>
                    <ul>
                        ${education.map(edu => `<li><strong>${edu.degree}</strong> from ${edu.institution} (${edu.year})</li>`).join('')}
                    </ul>
                </div>

                <div>
                    <strong>Missing Skills:</strong>
                    <ul>
                        ${missing_skills.map(skill => `<li>${skill}</li>`).join('')}
                    </ul>
                </div>

                <div>
                    <strong>Experience Gaps:</strong>
                    <ul>
                        ${experience_gaps.map(gap => `<li>${gap}</li>`).join('')}
                    </ul>
                </div>
            `;
        } else {
            resultDiv.innerHTML = '<span class="error">Error analyzing the resume. Please try again.</span>';
        }
    } catch (error) {
        console.error('Error analyzing resume:', error);
        resultDiv.innerHTML = '<span class="error">An error occurred. Please try again.</span>';
    } finally {
        resultDiv.style.display = 'block';
        loader.style.display = 'none'; // Ensure loader is hidden in case of failure
    }
}

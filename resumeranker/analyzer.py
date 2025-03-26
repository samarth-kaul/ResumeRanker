import pdfplumber 
import spacy
from groq import Groq
import json

def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"

    return text.strip()


# API_KEY = "enter your api key here (you can get from groq cloud console)"
API_KEY = "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"

def analyze_resume_with_llm(resume_text: str, job_description: str) -> dict:
    prompt = f"""
    You are an AI assistant specializing in resume analysis for job applications.
    Your task is to evaluate the given resume against a specific job description and extract relevant details.

    **Instructions:**  
    - Identify and extract only the most relevant information.
    - Match skills and experience based on the job description.
    - Provide a structured output in **valid JSON format**.

    **Analysis Tasks:**  
    1️⃣ **Skills Matching:**  
       - Identify all **technical**, **soft**, and **domain-specific** skills in the resume.  
       - Categorize them as **Core Skills** (highly relevant to the job) and **Additional Skills** (useful but not critical).  
       
    2️⃣ **Experience Analysis:**  
       - Calculate the **total years of experience** from work history.  
       - Identify the **most relevant job positions** that align with the job description.  
       - Extract **job titles, company names, and duration** for each relevant role.  

    3️⃣ **Project Classification:**  
       - Categorize **projects** based on their domain (e.g., AI, Web Development, Finance, Healthcare, etc.).  
       - For each project, extract:  
         - **Title**
         - **Technologies Used**
         - **Role in Project**
         - **Key Achievements**  
       
    4️⃣ **Education & Certifications:**  
       - Extract **degrees earned**, including university names and graduation years.  
       - Identify **relevant certifications** related to the job (e.g., AWS Certified, PMP, etc.).  

    5️⃣ **Resume-Job Relevance Ranking:**  
       - Assign a **Relevance Score (0-100%)** based on how well the resume matches the job description.  
       - Use the following factors:
         - **Skill Match (%)**
         - **Experience Relevance (%)**
         - **Project Alignment (%)**
         - **Education Match (%)**  

    6️⃣ **Recommendations for Improvement:**  
       - Suggest **missing skills** that could enhance the applicant’s chances.  
       - Identify **gaps in experience** or areas for improvement.  

    ---  
    **Input Data:**  
    - **Resume:**  
      ```
      {resume_text}
      ```
    - **Job Description:**  
      ```
      {job_description}
      ```

    ---  
    **Output JSON Format:**  
    ```json
    {{
        "rank": <percentage>,
        "skill_match": <percentage>,
        "experience_relevance": <percentage>,
        "project_alignment": <percentage>,
        "education_match": <percentage>,
        "core_skills": ["skill1", "skill2", "skill3", ...],
        "additional_skills": ["skill1", "skill2", ...],
        "total_experience": <number_of_years>,
        "relevant_experience": [
            {{
                "job_title": "Title",
                "company": "Company Name",
                "duration": "X years/months"
            }},
            ...
        ],
        "project_classification": [
            {{
                "title": "Project Name",
                "domain": "Project Category",
                "technologies": ["Tech1", "Tech2", ...],
                "role": "Role in Project",
                "achievements": ["Achievement1", "Achievement2"]
            }},
            ...
        ],
        "education": [
            {{
                "degree": "Degree Name",
                "institution": "University Name",
                "year": "Year of Completion"
            }},
            ...
        ],
        "certifications": ["Certification1", "Certification2", ...],
        "missing_skills": ["Suggested Skill1", "Suggested Skill2"],
        "experience_gaps": ["Gap1", "Gap2"]
    }}
    ```
    Ensure that the JSON output is structured correctly and contains **relevant, accurate** insights.
    """

    try:
        client = Groq(api_key=API_KEY)
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            response_format={"type": "json_object"}
        )
        result = response.choices[0].message.content
        return json.loads(result)

    except Exception as e:
        print(e)


def process_resume(pdf_path, job_description):
    try:
        resume_text = extract_text_from_pdf(pdf_path)
        data = analyze_resume_with_llm(resume_text, job_description)
        return data
    except Exception as e:
        print(e)
        return None
    












# SAMPLE PROMPT (this is the original older prompt)

# def analyze_resume_with_llm(resume_text:str, job_description:str)->dict:
#     prompt = f"""
#     You are an AI assistance that analyzes resumes for a software engineering job application.
#     Given a resume and a job description, extract the following details:

#     1) Identify all skills mentioned in the resume.
#     2) Calculate the total years of experience.
#     3) Categorize the projects based on the domain (e.g, AI, Web Development, Cloud etc).
#     4) Rank the resume relevance to the job description on a scale of 0 to 100.

#     Resume:
#     {resume_text}

#     Job Description
#     {job_description}

#     Provide the output in valid JSON format JSON format with this structure:
#     {{
#         "rank" : "<percentage>",
#         "skills" : ["skill1", "skill2", "skill3", "skill4",......],
#         "total_experience" : "<number of years>",
#         "project_category" : ["category1", "category2", "category3",.....>]
#     }}
#     """

#     try:
#         client = Groq(api_key=API_KEY)
#         response = client.chat.completions.create(
#             model = "llama3-8b-8192",
#             # model = "llama-3.3-70b-versatile",
#             messages = [{"role" : "user", "content" : prompt}],
#             temperature = 0.7,
#             response_format = {"type" : "json_object"}
#         )
#         result = response.choices[0].message.content
#         return json.loads(result)
    
#     except Exception as e:
#         print(e)











    
# print(extract_text_from_pdf("sample.pdf"))
# print(process_resume("sample.pdf", """Job Description:
# We are looking for a skilled React Developer to join our dynamic team. The ideal candidate will have experience in building high-performance, scalable web applications using React.js and related technologies. You will work closely with backend engineers, designers, and product managers to deliver seamless user experiences.

# Key Responsibilities:
# Develop and maintain high-quality React.js applications with reusable components and optimized performance.
# Integrate with GraphQL and RESTful APIs to fetch and manipulate data efficiently.
# Work with Redux/Context API/Zustand for state management to ensure a smooth user experience.
# Implement secure and seamless payment gateway integrations such as Stripe, Adyen, PayPal, etc.
# Optimize application performance using Redis caching, WebSockets, and lazy loading techniques.
# Ensure responsive and cross-browser compatible UI/UX.
# Containerize applications using Docker and deploy on cloud platforms (AWS, GCP, or Azure).
# Implement authentication and authorization using JWT, OAuth, or Firebase Auth.
# Work with CI/CD pipelines to automate testing and deployment.
# Collaborate with designers, backend engineers, and stakeholders to build scalable solutions.
# Maintain proper documentation, clean code, and best development practices.
# Required Skills:
# Strong proficiency in React.js and related libraries such as React Router, React Query, etc.
# GraphQL experience with Apollo Client or Relay for efficient API consumption.
# State management expertise using Redux, Redux Toolkit, or Context API.
# Experience with payment gateway integrations (Stripe, Adyen, PayPal, etc.).
# Proficiency in JavaScript (ES6+) & TypeScript.
# Backend interaction skills, including working with REST APIs, WebSockets, and GraphQL APIs.
# Knowledge of Redis for caching and optimizing API responses.
# Docker & containerization experience for efficient development and deployment.
# Familiarity with microservices architecture and API Gateway configurations.
# Database knowledge (SQL & NoSQL - PostgreSQL, MongoDB, Firebase).
# Experience in testing frameworks such as Jest, React Testing Library, or Cypress.
# Version control proficiency using Git & GitHub/GitLab.
# Experience with Agile/Scrum development workflows.
# Nice-to-Have Skills:
# Experience with Next.js for server-side rendering and static site generation.
# Knowledge of Node.js and Express for full-stack development.
# Cloud deployment experience with AWS (S3, Lambda, ECS) or Firebase.
# Experience with serverless functions (AWS Lambda, Vercel, or Netlify Functions).
# Experience with Web3.js and blockchain integrations.
# Why Join Us?
# Work on cutting-edge projects in a fast-paced environment.
# Competitive salary with performance-based bonuses.
# Flexible work schedule and remote-friendly environment.
# Opportunities for learning and career growth.
# Work with a passionate and skilled development team."""))
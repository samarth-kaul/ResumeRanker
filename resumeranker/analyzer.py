import pdfplumber 
import spacy
from groq import Groq
import json

def extract_text_ftom_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"

    return text.strip()


API_KEY = "enter your api key here (you can get from groq cloud console)"

def analyze_resume_with_llm(resume_text:str, job_description:str) -> dict:
    prompt = f"""
    You are an AI assistance that analyzes resumes for a software engineering job application.
    Given a resume and a job description, extract the following details:

    1) Identify all skills mentioned in the resume.
    2) Calculate the total years of experience.
    3) Categorize the projects based on the domain (e.g, AI, Web Development, Cloud etc).
    4) Rank the resume relevance to the job description on a scale of 0 to 100.

    Resume:
    {resume_text}

    Job Description
    {job_description}

    Provide the output in valid JSON format JSON format with this structure:
    {{
        "rank" : "<percentage>",
        "skills" : ["skill1", "skill2", "skill3", "skill4",......],
        "total_experience" : "<number of years>",
        "project_category" : ["category1", "category2", "category3",.....>]
    }}
    """

    try:
        client = Groq(api_key=API_KEY)
        response = client.chat.completions.create(
            model = "llama3-8b-8192",
            message = [{"role" : "user", "content" : prompt}],
            temperature = 0.7,
            response_format = {"type" : "json_object"}
        )
        result = response.choices[0].message.content
        return json.loads(result)
    
    except Exception as e:
        print(e)


def process_resume(pdf_path, job_description):
    try:
        resume_text = extract_text_ftom_pdf(pdf_path)
        data = analyze_resume_with_llm(resume_text, job_description)
        return data
    except Exception as e:
        print(e)
        return None
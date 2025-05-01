from fastapi import FastAPI
from pydantic import BaseModel
import requests

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.responses import JSONResponse

from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()  # This loads the environment variables from .env

# FastAPI app initialization
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow only your frontend
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods like GET, POST, OPTIONS
    allow_headers=["*"],  # Allow all headers
)
# Pydantic model for input validation
class CompanyInfoRequest(BaseModel):
    company_name: str
    industry: str

# Function to get company info from Wikipedia
def get_company_info(company_name):
    search_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{company_name.replace(' ', '_')}"
    response = requests.get(search_url)

    if response.status_code == 200:
        data = response.json()
        return data.get("extract", "No extract found.")
    else:
        return "Company not found on Wikipedia."

# Function to generate AI use cases
# def generate_ai_usecases(company_info, industry, model="gemma3"):
#     system_prompt = """
#     You are an expert AI strategist specializing in Artificial Intelligence and Generative AI (GenAI) applications.

#     Your job is to:
#     - Read the company overview and identify its key business activities.
#     - Understand its industry segment.
#     - Suggest 5 tailored AI/GenAI/ML use cases that improve the company's internal operations or customer experience.
#     - Each use case should have a short explanation.
#     - At least one use case should use Generative AI (like AI chat, report generation, or intelligent search).
#     """

#     user_prompt = f"""
#     Company Overview:
#     {company_info}

#     Industry:
#     {industry}

#     Please generate the use cases now.
#     """

#     response = ollama.chat(model=model, messages=[
#         {"role": "system", "content": system_prompt},
#         {"role": "user", "content": user_prompt}
#     ])

#     return response['message']['content']
from groq import Groq

def groq_api_call(company_info, industry):
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))


    # Construct your prompt using input parameters
    prompt = """
You are an expert AI strategist specializing in Artificial Intelligence and Generative AI (GenAI) applications.

Your job is to:
- Read the company overview and identify its key business activities.
- Understand its industry segment.
- Suggest 5 tailored AI/GenAI/ML use cases that improve the company's internal operations or customer experience.
- Each use case should have:
  - A clear title
  - A short explanation
  - (Optional but recommended) Real-world applicability
  - A reference link or source URL (e.g., Google product pages, research, documentation, case studies) where more information can be found about the technology, concept, or inspiration.

Ensure the use cases are specific, aligned to the company's core functions, and at least one uses Generative AI (like chatbots, content generation, or intelligent search). Present the response in Markdown format with readable structure and clickable hyperlinks.
"""


    user_prompt = f"""
    Company Overview:
    {company_info}

    Industry:
    {industry}

    Please generate the use cases now.
    """

    completion = client.chat.completions.create(
        model="qwen-qwq-32b",
        messages=[
            {
                
                "role": "system","content": prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        temperature=0.6,
        max_completion_tokens=4096,
        top_p=0.95,
        stream=True,
        stop=None,
    )

    full_response = ""
    for chunk in completion:
        full_response += chunk.choices[0].delta.content or ""
    
    return full_response



# FastAPI endpoint to handle the request and generate use cases
@app.post("/generate-use-cases/")
def generate_use_cases(request: CompanyInfoRequest):
    company_info = get_company_info(request.company_name)
    print(company_info)
    industry = request.industry
    use_cases = groq_api_call(company_info, industry)
    print(use_cases)
    return {"company_info": company_info, "use_cases": use_cases}


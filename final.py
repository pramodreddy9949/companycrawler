from fastapi import FastAPI
from pydantic import BaseModel
import requests
import ollama
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.responses import JSONResponse


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
def generate_ai_usecases(company_info, industry, model="gemma3"):
    system_prompt = """
    You are an expert AI strategist specializing in Artificial Intelligence and Generative AI (GenAI) applications.

    Your job is to:
    - Read the company overview and identify its key business activities.
    - Understand its industry segment.
    - Suggest 5 tailored AI/GenAI/ML use cases that improve the company's internal operations or customer experience.
    - Each use case should have a short explanation.
    - At least one use case should use Generative AI (like AI chat, report generation, or intelligent search).
    """

    user_prompt = f"""
    Company Overview:
    {company_info}

    Industry:
    {industry}

    Please generate the use cases now.
    """

    response = ollama.chat(model=model, messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ])

    return response['message']['content']

# FastAPI endpoint to handle the request and generate use cases
@app.post("/generate-use-cases/")
def generate_use_cases(request: CompanyInfoRequest):
    company_info = get_company_info(request.company_name)
    print(company_info)
    industry = request.industry
    use_cases = generate_ai_usecases(company_info, industry)
    print(use_cases)
    return {"company_info": company_info, "use_cases": use_cases}


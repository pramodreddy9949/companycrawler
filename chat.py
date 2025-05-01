import ollama

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
if __name__ == "__main__":
    company_info = """
Deloitte is a global professional services firm that provides consulting, audit, tax, and advisory services. 
It operates in multiple industries including finance, healthcare, and government. The firm focuses on helping 
clients with digital transformation, risk management, and strategic operations.
    """
    industry = "Consulting / Professional Services"

    output = generate_ai_usecases(company_info, industry)
    print("\n--- Generated AI/GenAI Use Cases ---\n")
    print(output)

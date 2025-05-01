import requests

def get_company_info(company_name):
    search_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{company_name.replace(' ', '_')}"
    response = requests.get(search_url)

    if response.status_code == 200:
        data = response.json()
        return data.get("extract", "No extract data found.")
    else:
        return "Company not found on Wikipedia."

# Test
if __name__ == "__main__":

    company = input("Enter company name: ")
    info = get_company_info(company)
    print("\n--- Company Overview ---\n")
    print(info)

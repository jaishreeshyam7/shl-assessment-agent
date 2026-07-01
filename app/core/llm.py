import os

from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env")

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.5-flash")


def generate_response(user_query: str, recommendations: list):

    prompt = f"""
You are an SHL Assessment Recommendation Assistant.

User Query:
{user_query}

Retrieved Assessments:
{recommendations}

Instructions:
- Recommend only from the retrieved assessments.
- Do not invent any new assessment.
- Briefly explain why they match.
- Keep the answer concise and professional.
"""

    response = model.generate_content(prompt)

    return response.text




#temproray
if __name__ == "__main__":

    sample = [
        {
            "name": "Java 8 (New)"
        },
        {
            "name": "Core Java (Entry Level) (New)"
        }
    ]

    print(
        generate_response(
            "Hiring a Java Developer",
            sample
        )
    )
def generate_comparison(user_query: str, recommendations: list):

    prompt = f"""
You are an SHL Assessment Recommendation Assistant.

The user wants to compare assessments.

User Query:
{user_query}

Assessments:
{recommendations}

Instructions:
- Compare ONLY the assessments provided.
- Explain the purpose of each assessment.
- Mention differences.
- Mention when each should be used.
- Recommend the better assessment depending on the hiring need.
- Do NOT invent any assessment.
"""

    response = model.generate_content(prompt)

    return response.text


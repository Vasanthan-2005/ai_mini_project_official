from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv(dotenv_path="../.env", override=True)

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key = os.getenv("GROQ_API_KEY")
)

def format_with_llm(user_query, recipes):

    context = ""

    for r in recipes:
        context += f"""
Recipe: {r['name']}
Ingredients: {r['ingredients']}
Steps: {r['steps']}
Match Score: {r['score']}
"""

    prompt = f"""
User has: {user_query}

Top recipes (ranked best first):
{context}

IMPORTANT RULES:
- The FIRST recipe is the best match.
- You MUST select ONLY the first recipe as "best_recipe".
- Do NOT choose any other recipe.
- Do NOT change ranking.

Return ONLY valid JSON.

Format:
{{
  "best_recipe": "",
  "why": "",
  "missing_ingredients": [],
  "steps": [],
  "tips": ""
}}
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    content = response.choices[0].message.content

    try:
        return json.loads(content)
    except:
        return {
            "error": "Invalid JSON from LLM",
            "raw": content
        }
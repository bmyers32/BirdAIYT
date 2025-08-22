
import json
import openai
import random

class FactGenerator:
    def __init__(self, fact_db_path, api_key):
        self.fallback_facts = json.load(open(fact_db_path))
        openai.api_key = api_key

    def get_fact(self, species):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "user", "content": f"Give me one unique, fun fact about a {species} bird."}
                ],
                max_tokens=60,
                temperature=0.7,
            )
            return response.choices[0].message.content.strip()
        except Exception:
            return random.choice(self.fallback_facts.get(species, ["Birds are cool!"]))

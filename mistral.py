import requests
from dotenv import load_dotenv
import os

load_dotenv()
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY") 
MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {MISTRAL_API_KEY}",
    "Content-Type": "application/json"
}

def mistral_call(prompt):
    data = {
        "model": "mistral-medium",
        "messages": [
            {"role": "system", "content": "You are a clinical pharmacist assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    response = requests.post(MISTRAL_API_URL, headers=HEADERS, json=data)
    result = response.json()
    return result['choices'][0]['message']['content'] if 'choices' in result else "❌ Error: No response from Mistral."


def get_interactions(drug_info_list: list) -> str:
    drugs = "\n".join([f"- {d}" for d in drug_info_list])
    prompt = f"""
A patient is taking the following medications:\n{drugs}

Please analyze **potential drug-drug interactions** only. List any risks and mechanisms involved.
"""
    return mistral_call(prompt)


def get_dosage_safety(drug_info_list: list) -> str:
    drugs = "\n".join([f"- {d}" for d in drug_info_list])
    prompt = f"""
A patient is on these medications:\n{drugs}

Evaluate the **dosage safety** for each drug based on typical adult doses. Flag any concerns.
"""
    return mistral_call(prompt)


def get_clinical_warnings(drug_info_list: list) -> str:
    drugs = "\n".join([f"- {d}" for d in drug_info_list])
    prompt = f"""
Given these prescribed drugs:\n{drugs}

Provide any **clinical warnings** related to age, organ function, side effects, or special populations.
"""
    return mistral_call(prompt)


def get_recommendations(drug_info_list: list) -> str:
    drugs = "\n".join([f"- {d}" for d in drug_info_list])
    prompt = f"""
A patient is currently taking:\n{drugs}

Give **final recommendations** to improve safety, monitoring, or therapeutic outcomes.
"""
    return mistral_call(prompt)

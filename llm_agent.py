import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def analyze_medical_report(report_text):
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a hospital clinical decision support AI. "
                    "Do NOT diagnose. "
                    "Provide:\n"
                    "1. Risk trend\n"
                    "2. Escalation suggestion\n"
                    "3. Nurse care instructions\n"
                )
            },
            {
                "role": "user",
                "content": report_text
            }
        ]
    )

    return response.choices[0].message.content

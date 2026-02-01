import os
from dotenv import load_dotenv

load_dotenv()

try:
    from groq import Groq
    GROQ_AVAILABLE = True
except Exception:
    GROQ_AVAILABLE = False


def analyze_medical_report(report_text: str) -> str:
    """
    Safe LLM wrapper.
    NEVER crashes the system.
    """

    api_key = os.getenv("GROQ_API_KEY")

    # 🔴 Case 1: No API key or Groq not installed
    if not api_key or not GROQ_AVAILABLE:
        return (
            "LLM unavailable. Fallback recommendation:\n"
            "- Review patient manually\n"
            "- Consider Emergency or Surgical consult\n"
            "- Monitor vitals closely"
        )

    try:
        client = Groq(api_key=api_key)

        response = client.chat.completions.create(
           model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a hospital clinical decision support AI. "
                        "Do NOT diagnose. "
                        "Provide:\n"
                        "1. Risk trend\n"
                        "2. Department recommendation\n"
                        "3. Doctor role\n"
                        "4. Resources needed"
                    )
                },
                {
                    "role": "user",
                    "content": report_text
                }
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        # 🔴 NEVER crash agentic system
        return (
            "LLM error occurred. Safe fallback activated.\n"
            f"Error: {str(e)}\n"
            "Recommendation:\n"
            "- Escalate to senior doctor\n"
            "- Continue monitoring\n"
            "- Re-run report later"
        )

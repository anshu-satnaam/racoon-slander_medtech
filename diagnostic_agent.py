from pypdf import PdfReader
from llm_agent import analyze_medical_report
from agent_state import set_state

MAX_CHARS = 3000  # safe for Groq


def extract_text_from_pdf(file_path: str) -> str:
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text


def chunk_text(text: str, size: int):
    return [text[i:i + size] for i in range(0, len(text), size)]


def diagnostic_support(patient_id: str, file_path: str):
    text = extract_text_from_pdf(file_path)
    chunks = chunk_text(text, MAX_CHARS)

    summaries = []

    for idx, chunk in enumerate(chunks[:3]):  # limit to first 3 chunks
        prompt = f"""
        You are a clinical decision support system.
        DO NOT give a final diagnosis.
        Summarize key findings, red flags, and possible conditions.

        Medical report section {idx+1}:
        {chunk}
        """
        response = analyze_medical_report(prompt)
        summaries.append(response)

    final_prompt = f"""
    Combine the following medical summaries.
    Provide:
    - Possible conditions
    - Red flags
    - Confidence notes
    - Recommendation for doctor review only

    Summaries:
    {summaries}
    """

    final_result = analyze_medical_report(final_prompt)

    set_state(patient_id, "diagnostic_support", final_result)

    return {
        "note": "For doctor review only",
        "ai_suggestions": final_result
    }

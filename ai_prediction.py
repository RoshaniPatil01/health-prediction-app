import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load API key from .env file
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini only if API key exists
if API_KEY:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
else:
    model = None


def predict(glucose, haemoglobin, cholesterol):

    # Your existing rule-based prediction
    if glucose > 180:
        result = "🚨 High risk of Diabetes."

    elif glucose > 140:
        result = "⚠️ Pre-diabetic condition possible."

    elif cholesterol > 240:
        result = "⚠️ High cholesterol detected."

    elif haemoglobin < 12:
        result = "⚠️ Low haemoglobin. Possible anemia detected."

    elif haemoglobin > 18:
        result = "⚠️ High haemoglobin levels."

    else:
        result = "✅ All parameters are within normal range."

    # If Gemini API is available, get explanation
    if model:
        try:
            prompt = f"""
            You are a medical assistant.

            Result: {result}

            Blood Test Values:
            Glucose: {glucose}
            Haemoglobin: {haemoglobin}
            Cholesterol: {cholesterol}

            Explain the result in simple language.
            Give 2 health tips.
            Keep the response under 50 words.
            """

            response = model.generate_content(prompt)

            return f"{result}\n\n{response.text}"

        except Exception:
            return result

    # If API is not available, return normal result
    return result
# import google.generativeai as genai

# API_KEY = "YOUR_GEMINI_API_KEY"

# genai.configure(api_key=API_KEY)

# model = genai.GenerativeModel("gemini-1.5-flash")

# def predict(glucose, haemoglobin, cholesterol):
#     prompt = f"""
#     You are a medical assistant.

#     Analyze these blood test results:
#     Glucose: {glucose}
#     Haemoglobin: {haemoglobin}
#     Cholesterol: {cholesterol}

#     Give:
#     - Health risk
#     - Simple advice
#     Keep it under 50 words.
#     """

#     response = model.generate_content(prompt)
#     return response.text







def predict(glucose, haemoglobin, cholesterol):

    if glucose > 180:
        return "🚨 High risk of Diabetes. Please consult a doctor immediately."
    
    elif glucose > 140:
        return "⚠️ Pre-diabetic condition possible. Maintain diet and exercise."

    elif cholesterol > 240:
        return "⚠️ High cholesterol detected. Risk of heart disease."

    elif haemoglobin < 12:
        return "⚠️ Low haemoglobin. Possible anemia detected."

    elif haemoglobin > 18:
        return "⚠️ High haemoglobin levels. Requires medical attention."

    else:
        return "✅ All parameters are within normal range. Healthy condition."
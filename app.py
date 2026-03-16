# app.py - Main Flask application for AI Business Idea Generator
# Enter your skills, budget, and interests — AI suggests business ideas!

from flask import Flask, render_template, request, jsonify
from groq import Groq
import os

# Initialize Flask app
app = Flask(__name__)

# Groq API client — API key is set directly here
api_key = st.text_input("Enter your Groq API Key", type="password")


def build_prompt(skills: str, budget: str, interest: str, experience: str, business_type: str) -> str:
    """
    Build a structured prompt for the AI to generate business ideas.

    Args:
        skills      : User's skills e.g. coding, cooking, teaching
        budget      : Investment budget range e.g. Low, Medium, High
        interest    : User's interests/hobbies e.g. fitness, food, tech
        experience  : Experience level e.g. Beginner, Intermediate, Expert
        business_type: Online, Offline, or Both

    Returns:
        A detailed prompt string for the AI
    """
    return f"""You are an expert business consultant and startup advisor.

A person wants to start a business with the following details:
- Skills: {skills}
- Interests/Passions: {interest}
- Available Budget: {budget}
- Experience Level: {experience}
- Preferred Business Type: {business_type}

Please suggest exactly 3 unique and practical business ideas tailored to this person.

For each idea use EXACTLY this format:

---
### Idea [number]: [Business Name]
**Business Type:** {business_type}
**Budget Required:** {budget}
**Difficulty Level:** [Easy / Medium / Hard]
**Monthly Income Potential:** [estimated range in INR]
**Time to First Income:** [e.g. 1-3 months]

**What is this business?**
[2-3 lines explaining the business idea clearly]

**Why it suits you?**
[Explain why this matches their skills, budget and interests]

**How to Start — Step by Step:**
1. [step]
2. [step]
3. [step]
4. [step]
5. [step]

**Tools / Resources Needed:**
- [tool or resource]
- [tool or resource]

**Pro Tips:**
- [practical tip to succeed]
- [practical tip to succeed]
---

Make ideas realistic, actionable, and specific to the Indian market. Be encouraging and motivating!
"""


@app.route("/")
def index():
    """Render the main page."""
    return render_template("index.html")


@app.route("/get-ideas", methods=["POST"])
def get_ideas():
    """
    Handle the business idea generation request.
    Receives user inputs from frontend, calls Groq API, returns AI ideas.
    """
    data = request.get_json()

    skills        = data.get("skills",        "").strip()
    budget        = data.get("budget",        "Low").strip()
    interest      = data.get("interest",      "").strip()
    experience    = data.get("experience",    "Beginner").strip()
    business_type = data.get("business_type", "Online").strip()

    # Validate required fields
    if not skills:
        return jsonify({"error": "Please enter your skills!"}), 400
    if not interest:
        return jsonify({"error": "Please enter your interests!"}), 400

    try:
        # Call Groq AI
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": build_prompt(skills, budget, interest, experience, business_type)
                }
            ],
            model="llama-3.3-70b-versatile",  # Latest supported Groq model
            temperature=0.8,                   # Higher creativity for business ideas
            max_tokens=3000,                   # More tokens for detailed ideas
        )

        # Extract AI response
        ideas_text = chat_completion.choices[0].message.content
        return jsonify({"ideas": ideas_text})

    except Exception as e:
        return jsonify({"error": f"AI error: {str(e)}"}), 500


if __name__ == "__main__":
    # Run Flask development server
    app.run(debug=True, port=5000)

from groq import Groq
import streamlit as st

st.set_page_config(page_title="AI Business Idea Generator", page_icon="💡")
st.title("💡 AI Business Idea Generator")
st.write("Enter your details and get 3 unique business ideas instantly!")

skills        = st.text_input("Your Skills", placeholder="e.g. coding, cooking, teaching")
interest      = st.text_input("Your Interests", placeholder="e.g. fitness, food, tech")
budget        = st.selectbox("Budget", ["Low (under ₹10,000)", "Medium (₹10,000-₹1,00,000)", "High (above ₹1,00,000)"])
experience    = st.selectbox("Experience Level", ["Beginner", "Intermediate", "Expert"])
business_type = st.selectbox("Business Type", ["Online", "Offline", "Both"])

if st.button("Generate Business Ideas"):
    if not skills or not interest:
        st.warning("Please fill in your skills and interests!")
    else:
        with st.spinner("Generating your ideas..."):
            try:
                client = Groq(api_key=st.secrets["GROQ_API_KEY"])
                prompt = f"""You are an expert business consultant.
Suggest exactly 3 unique business ideas for:
- Skills: {skills}
- Interests: {interest}
- Budget: {budget}
- Experience: {experience}
- Type: {business_type}
For each idea provide name, income potential, difficulty, what it is, how to start in 5 steps, and 2 pro tips.
Be specific to Indian market!"""
                response = client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model="llama-3.3-70b-versatile",
                    temperature=0.8,
                    max_tokens=3000,
                )
                st.success("Here are your business ideas!")
                st.markdown(response.choices[0].message.content)
            except Exception as e:
                st.error(f"Error: {str(e)}")

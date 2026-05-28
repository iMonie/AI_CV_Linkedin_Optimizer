import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("AI CV + LinkedIn Optimizer 🚀")

cv = st.text_area("Paste your CV")
email = st.text_input("Enter your email")

st.info("⚠️ Payment required before generating result")

if st.button("I HAVE PAID"):
    if cv and email:

        with st.spinner("Optimizing your CV..."):

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "user", "content": f"""
                    Improve this CV professionally and create:
                    - ATS optimized CV
                    - LinkedIn headline
                    - LinkedIn summary

                    {cv}
                    """}
                ]
            )

            result = response.choices[0].message.content

            st.success("✅ Done!")

            st.download_button("Download Result", result)

    else:
        st.warning("Please fill all fields")
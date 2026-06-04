import streamlit as st
from openai import OpenAI
import smtplib
from email.mime.text import MIMEText
import time
import random
from datetime import datetime, timedelta
import urllib.parse

st.set_page_config(page_title="AI CV + LinkedIn Optimizer", page_icon="🚀")

st.markdown("""
<style>
.stApp {background: linear-gradient(135deg, #eef2ff, #ffffff);color: #111;}
h1, h2, h3, h4, p {color: #111 !important;font-weight: 600;}
.premium-card {background: white;padding: 20px;border-radius: 15px;border: 2px solid #2563eb;box-shadow: 0 0 25px rgba(37, 99, 235, 0.4);}
.basic-card {background: white;padding: 20px;border-radius: 15px;border: 1px solid #ddd;}
textarea, input {background-color: #ffffff !important;color: #111 !important;border-radius: 10px;border: 1px solid #ddd;}
.stButton>button {background-color: #2563eb;color: white;border-radius: 10px;font-weight: bold;}
.stDownloadButton>button {background-color: #16a34a;color: white;border-radius: 10px;}
</style>
""", unsafe_allow_html=True)

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def send_email(to_email, content):
    try:
        msg = MIMEText(content)
        msg['Subject'] = "🚀 Your AI Optimized CV + LinkedIn"
        msg['From'] = st.secrets["EMAIL_ADDRESS"]
        msg['To'] = to_email
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(st.secrets["EMAIL_ADDRESS"], st.secrets["EMAIL_PASSWORD"])
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        st.error(f"Email error: {e}")
        return False

query_params = st.query_params
ref = query_params.get("ref")

if "ref_count" not in st.session_state:
    st.session_state.ref_count = 0

if ref:
    st.session_state.ref_count += 1

user_id = str(random.randint(10000, 99999))
ref_link = f"https://aicvlinkedinoptimizer-hlhavswrjy84dp8obmejp4.streamlit.app/?ref={user_id}"

st.markdown(f"🔥 **{random.randint(12,47)} people are using this right now**")

if "end_time" not in st.session_state:
    st.session_state.end_time = datetime.now() + timedelta(minutes=15)

remaining = st.session_state.end_time - datetime.now()
if remaining.total_seconds() > 0:
    st.warning(f"⏳ Offer expires in {int(remaining.total_seconds()//60)}:{int(remaining.total_seconds()%60):02d}")
else:
    st.error("❌ Offer expired!")

st.title("🚀 AI CV + LinkedIn Optimizer")
st.write("🔥 Beat 99% of applicants.")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 💼 Basic")
    if st.button("Start Free"):
        st.session_state.plan = "basic"

with col2:
    st.markdown("### 💎 Premium")
    if st.button("Upgrade Now 🚀"):
        st.session_state.plan = "premium"

plan = st.session_state.get("plan", "basic")

cv = st.text_area("Paste CV")
email = st.text_input("Email")

if cv and email:
    if st.button("🚀 Generate My CV"):

        progress = st.progress(0)
        for i in range(100):
            time.sleep(0.01)
            progress.progress(i + 1)

        if plan == "basic":
            prompt = f"""
Improve this CV professionally:
- ATS optimized
- Better bullet points
- Clean format

CV:
{cv}
"""
        else:
            prompt = f"""
You are a WORLD-CLASS recruiter and career strategist.

RETURN YOUR ANSWER IN CLEAR SECTIONS EXACTLY LIKE THIS:

=== FULL CV REWRITE ===
Rewrite the CV with strong bullet points, metrics, and achievements.

=== LINKEDIN HEADLINE ===
Create a powerful headline.

=== LINKEDIN ABOUT ===
Write a compelling About section.

=== KEY SKILLS ===
List optimized skills.

=== EXPERIENCE IMPROVEMENTS ===
Rewrite experience with metrics.

=== ACHIEVEMENTS ===
Add measurable achievements.

=== JOB TARGETING STRATEGY ===
Give advice to tailor CV.

=== COVER LETTER ===
Write a strong tailored cover letter.

CV:
{cv}
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        result = response.choices[0].message.content

        st.success("🎉 Done!")
        st.download_button("Download", result)

        if send_email(email, result):
            st.success("Sent to email!")

        if plan == "basic":
            st.warning("Upgrade to unlock LinkedIn + Cover Letter 🚀")

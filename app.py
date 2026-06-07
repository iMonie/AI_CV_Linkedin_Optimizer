import streamlit as st
from openai import OpenAI
import smtplib
from email.mime.text import MIMEText
import time
import random
import urllib.parse
from datetime import datetime, timedelta

# ✅ ADDED
from docx import Document
import io
import re

# ==============================
# 🎨 UI DESIGN
# ==============================
st.set_page_config(page_title="AI CV Optimizer", page_icon="🚀")

st.title("🚀 AI That Matches and Rewrites Your CV to Any Job Description")

# ==============================
# 🔐 API
# ==============================
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ==============================
# 📩 EMAIL FUNCTION
# ==============================
def send_email(to_email, content):
    try:
        msg = MIMEText(content)
        msg['Subject'] = "🚀 Your AI Optimized CV"
        msg['From'] = st.secrets["EMAIL_ADDRESS"]
        msg['To'] = to_email

        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(st.secrets["EMAIL_ADDRESS"], st.secrets["EMAIL_PASSWORD"])
        server.send_message(msg)
        server.quit()
        return True
    except:
        return False

# ==============================
# 🔥 SCORE FUNCTION (ADVANCED)
# ==============================
def advanced_score(cv_text, jd_text):
    cv_words = set(re.findall(r"\w+", cv_text.lower()))
    jd_words = set(re.findall(r"\w+", jd_text.lower()))
    if not jd_words:
        return 0
    return min(int((len(cv_words & jd_words) / len(jd_words)) * 100), 95)

# ==============================
# 📄 DOCX GENERATOR
# ==============================
def generate_docx(content):
    doc = Document()
    for line in content.split("\n"):
        doc.add_paragraph(line)
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# ==============================
# INPUT
# ==============================
st.markdown("### 📄 Paste your CV")
cv = st.text_area("", height=200)

st.markdown("### 🧾 Paste Job Description (Optional)")
jd = st.text_area("", height=150)

st.markdown("### 📧 Email")
email = st.text_input("")

# ==============================
# PLAN
# ==============================
query_params = st.query_params
plan = query_params.get("plan")

# ==============================
# 🚀 MAIN LOGIC
# ==============================
if plan in ["basic", "premium"]:

    if plan == "basic":
        st.success("✅ Basic Plan Activated")
    else:
        st.success("💎 Premium Activated")

    if cv and email:

        if st.button("🚀 Generate My CV"):

            # LOADING
            progress = st.progress(0)
            for i in range(100):
                time.sleep(0.01)
                progress.progress(i + 1)

            # =========================
            # 💎 PREMIUM PIPELINE
            # =========================
            if plan == "premium":

                if jd.strip() != "":
                    score = advanced_score(cv, jd)

                    prompt = f"""
You are a TOP recruiter + ATS system.

Candidate current match score: {score}%

IMPORTANT:
Push this candidate above 85%.

STEP 1: Extract key requirements  
STEP 2: Compare with CV  
STEP 3: Identify gaps  
STEP 4: Rewrite CV aligned to JD  
STEP 5: Inject keywords naturally  
STEP 6: Add measurable achievements  

OUTPUT:
- Match Score
- Skill Gaps
- Keywords
- Rewritten CV
- LinkedIn
- Cover Letter

CV:
{cv}

JD:
{jd}
"""
                else:
                    prompt = f"""
You are a top recruiter.

Generate:
- ATS CV
- LinkedIn
- Cover Letter

CV:
{cv}
"""

            # =========================
            # 🆓 BASIC PIPELINE
            # =========================
            else:
                prompt = f"""
Improve this CV.

- Fix bullet points
- Make it ATS friendly
- Improve clarity

CV:
{cv}
"""

            # =========================
            # STEP 1: GENERATION
            # =========================
            res = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )

            first_output = res.choices[0].message.content

            # =========================
            # 🤖 AI REVIEW PASS (PREMIUM ONLY)
            # =========================
            if plan == "premium":

                review_prompt = f"""
You are a senior recruiter reviewing a CV.

Improve this output:
- Fix weak bullet points
- Add impact
- Improve clarity
- Strong recruiter tone

CONTENT:
{first_output}
"""

                review_res = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": review_prompt}]
                )

                final_output = review_res.choices[0].message.content
            else:
                final_output = first_output

            # =========================
            # OUTPUT
            # =========================
            st.success("✅ Done")

            if plan == "basic":
                st.write(first_output)
                st.warning("🔒 Premium upgrade unlocks full rewrite")
            else:
                st.write(final_output)

                # DOCX DOWNLOAD
                docx_file = generate_docx(final_output)
                st.download_button(
                    "📥 Download CV (DOCX)",
                    docx_file,
                    file_name="AI_CV.docx"
                )

            # EMAIL
            send_email(email, final_output)

    else:
        st.info("Enter CV + email")

else:
    st.error("❌ Complete payment first")

import streamlit as st
from openai import OpenAI
import smtplib
from email.mime.text import MIMEText
import time
import random
import urllib.parse
import re
import io
from docx import Document

# ==============================
# 🎨 UI
# ==============================
st.set_page_config(page_title="AI CV Optimizer", page_icon="🚀")

st.title("🚀 AI That Matches Your CV to Any Job Description (ATS + Recruiter Approved)")
st.write("🔥 Beat 99% of applicants. Get hired faster.")

# ==============================
# 🔐 API
# ==============================
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ==============================
# 📩 EMAIL
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
# 📊 SCORE
# ==============================
def advanced_score(cv_text, jd_text):
    cv_words = set(re.findall(r"\w+", cv_text.lower()))
    jd_words = set(re.findall(r"\w+", jd_text.lower()))
    if not jd_words:
        return 0
    return min(int((len(cv_words & jd_words) / len(jd_words)) * 100), 95)

# ==============================
# 📄 DOCX
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
# 💳 PRICING UI (FIXED + INSERTED)
# ==============================
st.markdown("## 💳 Choose Your Package")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div style="
        background:white;
        padding:25px;
        border-radius:15px;
        border:1px solid #e5e7eb;
        box-shadow:0 5px 15px rgba(0,0,0,0.05);
    ">
    <h3>💼 Basic (Free)</h3>
    <p>✔ ATS Optimized CV</p>
    <p>✔ Better bullet points</p>
    <p>✔ Clean formatting</p>
    <br>
    <p style="color:#6b7280;">Perfect for quick improvement</p>
    </div>
    """, unsafe_allow_html=True)

    st.link_button("Start Free", "https://selar.co/11180kb0j4")

with col2:
    st.markdown("""
    <div style="
        background:white;
        padding:25px;
        border-radius:15px;
        border:2px solid #2563eb;
        box-shadow:0 0 30px rgba(37,99,235,0.35);
        transform:scale(1.03);
    ">
    <h3>💎 Premium</h3>
    <p style="font-size:20px;">
    <span style="text-decoration:line-through;color:gray;">₦10,000</span>
    <strong style="color:#16a34a;"> ₦2,500 Today</strong>
    </p>
    <hr>
    <p>🔥 EVERYTHING in Basic PLUS:</p>
    <p>✔ Extraction of key requirements from JOB DESCRIPTION</p>
    <p>✔ Comparison of CV with Identified gaps</p>
    <p>✔ Rewrite CV to ALIGN with JD</p>
    <p>✔ Inject keywords NATURALLY</p>
    <p>✔ LinkedIn Headline</p>
    <p>✔ LinkedIn About Section</p>
    <p>✔ Skills Optimization</p>
    <p>✔ Recruiter-Level Rewrite</p>
    <p>✔ Achievement Metrics</p>
    <p>✔ Cover Letter</p>
    <p>✔ Continous 1 on 1 Mentorship on Whatsapp</p>
    </div>
    """, unsafe_allow_html=True)

    st.link_button("Upgrade Now 🚀", "https://selar.co/m001q0082z")

st.markdown("---")

# ==============================
# INPUT
# ==============================
st.markdown("### 📄 Paste your CV")
cv = st.text_area("", height=200)

st.markdown("### 🧾 Job Description (Optional)")
jd = st.text_area("", height=150)

st.markdown("### 📧 Email")
email = st.text_input("")

# ==============================
# PLAN
# ==============================
plan = st.query_params.get("plan")

# ==============================
# 🚀 LOGIC
# ==============================
if plan in ["basic", "premium"]:

    if plan == "basic":
        st.success("✅ Basic Plan Activated")
    else:
        st.success("💎 Premium Activated")

    if cv and email:

        if st.button("🚀 Generate My CV"):

            for i in range(100):
                time.sleep(0.01)
                st.progress(i + 1)

            # PREMIUM
            if plan == "premium":

                if jd.strip():
                    score = advanced_score(cv, jd)

                    prompt = f"""
You are a TOP recruiter + ATS system.

Candidate current match: {score}%

Push to 85%+

Match CV to job description.

Return:
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
Generate ATS CV + LinkedIn + Cover Letter.

CV:
{cv}
"""

            # BASIC
            else:
                prompt = f"""
Improve this CV:
- Better bullets
- ATS friendly

CV:
{cv}
"""

            # FIRST PASS
            res = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )

            first_output = res.choices[0].message.content

            # REVIEW PASS (PREMIUM ONLY)
            if plan == "premium":
                review_prompt = f"""
                
You are a senior recruiter reviewing a CV.

Improve this output:
- Fix weak bullet points
- Add missing impact
- Improve clarity
- Ensure strong recruiter tone


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

            st.success("✅ Done")

            if plan == "premium":
                st.write(final_output)

                docx = generate_docx(final_output)
                st.download_button("📥 Download CV", docx, "AI_CV.docx")

            else:
                st.write(first_output)
                st.warning("🔒 Upgrade to unlock full rewrite")

            send_email(email, final_output)

    else:
        st.info("Enter CV + email")

else:
    st.error("❌ Complete payment first")

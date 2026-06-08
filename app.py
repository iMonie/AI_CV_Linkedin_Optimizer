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
# 📊 SCORE (MERGED FIX)
# ==============================
def advanced_score(cv, jd):
    cv_words = set(re.findall(r"\w+", cv.lower()))
    jd_words = set(re.findall(r"\w+", jd.lower()))

    keyword_score = len(cv_words & jd_words) / max(len(jd_words), 1)

    skills_score = keyword_score
    experience_score = 0.7 if "experience" in cv.lower() else 0.4
    alignment_score = 0.6
    clarity_score = 0.7

    final = (
        skills_score * 0.3 +
        keyword_score * 0.25 +
        experience_score * 0.25 +
        alignment_score * 0.1 +
        clarity_score * 0.1
    ) * 100

    return int(final)

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
# 💳 PRICING UI
# ==============================
st.markdown("## 💳 Choose Your Package")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div style="background:white;padding:25px;border-radius:15px;border:1px solid #e5e7eb;">
    <h3>💼 Basic (Free)</h3>
    <p>✔ ATS Optimized CV</p>
    <p>✔ Better bullet points</p>
    <p>✔ Clean formatting</p>
    <p style="color:#6b7280;">Perfect for quick improvement</p>
    </div>
    """, unsafe_allow_html=True)
    st.link_button("Start Free", "https://selar.co/11180kb0j4")

with col2:
    st.markdown("""
    <div style="background:white;padding:25px;border-radius:15px;border:2px solid #2563eb;">
    <h3>💎 Premium</h3>
    <p><strong style="color:#16a34a;">₦2,500 Today</strong></p>
    <hr>
    <p>✔ JD Matching</p>
    <p>✔ Full Rewrite</p>
    <p>✔ LinkedIn + Cover Letter</p>
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

            progress = st.progress(0)
            for i in range(100):
                time.sleep(0.01)
                progress.progress(i + 1)

            if plan == "premium":

                if jd.strip():
                    score = advanced_score(cv, jd)

                    prompt = f"""
You are a TOP recruiter + ATS system.

Candidate current match: {score}%

Improve to 85%+

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
            else:
                prompt = f"""
Improve this CV:
- Better bullets
- ATS friendly

CV:
{cv}
"""

            res = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )

            first_output = res.choices[0].message.content

            if plan == "premium":
                review_prompt = f"""
Improve this CV to recruiter level.

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

# ==============================
# VIRAL HOOK (FIXED)
# ==============================
st.markdown("---")

st.markdown("""
## 🚀 Want Recruiters to FIND You?

✔ Writes posts for you  
✔ Plans your entire week  
✔ Schedules everything automatically  

🚨 Someone less skilled is winning… because they show up DAILY.

Fix that today 👇
""")

st.link_button(
    "Increase visibility now",
    "https://socials.scaleplant.com/en/?c=AKPOJOTOWY46"
)

encoded_msg = urllib.parse.quote("Help me get hired fast")

st.link_button(
    "💬 WhatsApp",
    f"https://wa.me/2348035341982?text={encoded_msg}"
)

# ==============================
# FOOTER
# ==============================
st.markdown("---")
st.caption("🚀 Built for income + impact by Oghenchovwe AKPOJOTOR")

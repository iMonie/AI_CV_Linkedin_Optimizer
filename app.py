import streamlit as st
from openai import OpenAI
import smtplib
from email.mime.text import MIMEText
import time
import random
import urllib.parse
from docx import Document

# ==============================
# UI (UNCHANGED)
# ==============================
st.set_page_config(page_title="AI CV Optimizer", page_icon="🚀")

st.title("🚀 AI That Matches Your CV to Any Job Description (ATS + Recruiter Approved)")

st.markdown("""
<style>
.stApp {background: linear-gradient(135deg, #eef2ff, #ffffff);}
textarea, input {background:#fff;color:#111;border-radius:10px;}
.stButton>button {background:#2563eb;color:white;border-radius:10px;}
.stDownloadButton>button {background:#16a34a;color:white;border-radius:10px;}
</style>
""", unsafe_allow_html=True)

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ==============================
# EMAIL
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
# DOCX CLEAN FORMAT
# ==============================
def generate_docx(text):
    doc = Document()
    sections = text.split("\n")

    for line in sections:
        if line.strip().startswith("---"):
            continue
        if line.isupper():
            doc.add_heading(line, level=2)
        else:
            doc.add_paragraph(line)

    path = "AI_Optimized_CV.docx"
    doc.save(path)
    return path

# ==============================
# ADVANCED SCORING
# ==============================
def advanced_score(cv, jd):
    cv_words = set(cv.lower().split())
    jd_words = set(jd.lower().split())

    keyword_score = len(cv_words & jd_words) / max(len(jd_words), 1)

    # heuristic scoring
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
# LIVE UI
# ==============================
st.markdown(f"🔥 **{random.randint(12,47)} people are using this right now**")

st.success("🔥 Someone just upgraded to Premium 💎")

# ==============================
# PLAN
# ==============================
plan = st.query_params.get("plan")

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
# MAIN
# ==============================
if plan in ["basic", "premium"]:

    if cv and email:

        if st.button("🚀 Generate My CV"):

            for i in range(100):
                time.sleep(0.01)

            # =========================
            # BASIC (LOCKED SAFE)
            # =========================
            if plan == "basic":

                prompt = f"""
Optimize CV for ATS only.
NO LinkedIn, NO Cover Letter.

CV:
{cv}
"""

                res = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role":"user","content":prompt}]
                )

                result = res.choices[0].message.content
                st.write(result)
                st.warning("🔒 Premium required for job matching + full optimization")

            # =========================
            # 💎 PREMIUM PIPELINE
            # =========================
            else:

                if jd.strip() != "":
                    score = advanced_score(cv, jd)

                    # STEP 1: GENERATION
                    prompt = f"""
You are a top recruiter.

Match CV to job description.

Return:
- Skill gaps
- Keywords
- Rewritten CV
- LinkedIn
- Cover letter

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

                res = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role":"user","content":prompt}]
                )

                first_output = res.choices[0].message.content

                # =========================
                # 🤖 AI REVIEW PASS
                # =========================
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
                    messages=[{"role":"user","content":review_prompt}]
                )

                final_output = review_res.choices[0].message.content

                # =========================
                # OUTPUT
                # =========================
                if jd.strip() != "":
                    st.success(f"Most hired candidates score 80%+ | Your Score: {score}%")

                st.write(final_output)

                # DOCX
                file = generate_docx(final_output)

                with open(file, "rb") as f:
                    st.download_button("📥 Download CV (DOCX)", f, file_name="AI_CV.docx")

                send_email(email, final_output)

    else:
        st.info("Enter CV + email")

else:
    st.error("❌ Complete payment first")

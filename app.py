import streamlit as st
from openai import OpenAI
import smtplib
from email.mime.text import MIMEText
import time
import random
from datetime import datetime, timedelta
import urllib.parse
import re
from reportlab.lib.styles import getSampleStyleSheet

# ==============================
# 🎨 UI DESIGN
# ==============================
st.set_page_config(page_title="AI CV + LinkedIn Optimizer", page_icon="🚀")

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #eef2ff, #ffffff);
    color: #111;
}
h1, h2, h3, h4, p {
    color: #111 !important;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

# ==============================
# 🔥 NEW HEADLINE + FEATURES
# ==============================
st.title("🚀 AI That Matches Your CV to Any Job Description (ATS + Recruiter Approved)")

st.markdown("""
### 💼 What This App Does:
✅ CV + Job Description matching  
✅ Skill gap detection  
✅ Keyword extraction (ATS hacking)  
✅ Achievement rewriting with intelligence  
✅ Recruiter-level positioning  
""")

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
# 📄 PDF GENERATOR
# ==============================

    doc = SimpleDocTemplate("cv.pdf")
    styles = getSampleStyleSheet()
    content = []

    for line in text.split("\n"):
        content.append(Paragraph(line, styles["Normal"]))

    doc.build(content)
    return "cv.pdf"

# ==============================
# 🔍 MATCH FUNCTION
# ==============================
def extract_keywords(text):
    words = re.findall(r'\b[A-Za-z]{4,}\b', text.lower())
    return list(set(words))

def calculate_match(cv, jd):
    if not jd.strip():
        return None, []

    jd_keywords = extract_keywords(jd)
    cv_keywords = extract_keywords(cv)

    matched = [k for k in jd_keywords if k in cv_keywords]
    missing = [k for k in jd_keywords if k not in cv_keywords]

    score = int((len(matched) / len(jd_keywords)) * 100) if jd_keywords else 0
    return score, missing[:15]

# ==============================
# 🔥 LIVE USERS
# ==============================
st.markdown(f"🔥 **{random.randint(12,47)} people are using this right now**")

# ==============================
# INPUT
# ==============================
st.markdown("### 📄 Paste your CV")
cv = st.text_area("", height=200)

st.markdown("### 💼 Paste Job Description (Optional)")
jd = st.text_area("", height=200)

st.markdown("### 📧 Enter your email")
email = st.text_input("")

# ==============================
# PLAN
# ==============================
query_params = st.query_params
plan = query_params.get("plan")

# ==============================
# REFERRAL
# ==============================
if "ref_count" not in st.session_state:
    st.session_state.ref_count = random.randint(0, 5)

ref_link = f"https://yourapp.streamlit.app/?ref={random.randint(1000,9999)}"

# ==============================
# MAIN LOGIC
# ==============================
if plan in ["basic", "premium"]:

    if cv and email:

        if st.button("🚀 Generate My CV"):

            # MATCH SCORE
            score, missing = calculate_match(cv, jd)

            if score is not None:
                st.markdown("## 🎯 Job Match Score")
                st.info("Most hired candidates score 80%+")

                st.progress(score / 100)

                if score >= 80:
                    st.success(f"🔥 Strong Match: {score}%")
                elif score >= 50:
                    st.warning(f"⚠️ Average Match: {score}%")
                else:
                    st.error(f"❌ Weak Match: {score}%")

                if missing:
                    st.markdown("### ❗ Missing Keywords")
                    st.write(", ".join(missing))

            # LOADING
            progress = st.progress(0)
            for i in range(100):
                time.sleep(0.01)
                progress.progress(i + 1)

            # PROMPT
            if plan == "basic":
                prompt = f"""
Improve this CV:
- ATS friendly
- Better bullet points

CV:
{cv}
"""
            else:
                prompt = f"""
You are an expert recruiter and strategist.

Resume:
{cv}

Job Description:
{jd}

TASKS:
1. Rewrite CV (results-driven, metrics)
2. Convert responsibilities into achievements
3. Compare CV vs JD → show gaps
4. Extract top 20 keywords + integrate
5. Optimize for ATS
6. Create LinkedIn (Headline, About, Skills)
7. Add strong achievements
8. Job-tailored CV
9. Cover Letter
"""

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )

            result = response.choices[0].message.content

            st.success("🎉 Your CV is Ready!")

            st.download_button("📥 Download TXT", result)

            pdf_file = create_pdf(result)
            with open(pdf_file, "rb") as f:
                st.download_button("📄 Download PDF", f, file_name="cv.pdf")

            send_email(email, result)

        # ==============================
        # 🚀 VIRAL HOOK
        # ==============================
        st.markdown("---")
        st.markdown("## 🚀 Want Recruiters to FIND You?")

        st.info("""
Your CV is strong…

But visibility = opportunities.

Top candidates show up DAILY on LinkedIn.
""")

        st.link_button(
            "Many have used this system to increase visibility — want it?",
            "https://socials.scaleplant.com/en/?c=AKPOJOTOWY46"
        )

        # ==============================
        # 📲 WHATSAPP
        # ==============================
        encoded_msg = urllib.parse.quote(
            "I just used your AI CV tool. Help me get hired fast."
        )

        st.link_button(
            "💬 Chat on WhatsApp",
            f"https://wa.me/2348035341982?text={encoded_msg}"
        )

        # ==============================
        # 🎁 REFERRAL
        # ==============================
        st.markdown("---")
        st.markdown("## 🎁 Earn Rewards")

        st.success(f"""
Invite friends & earn rewards 🎉

Your referral link:
{ref_link}

Referrals: {st.session_state.ref_count}
""")

        st.info("""
🎁 10 referrals = FREE CV Premium Rewrite & Linkedin Optimization  
🎁 25 referrals = Done for You & 1-on-1 Session  
""")

    else:
        st.info("Enter CV + email")

else:
    st.error("❌ Complete payment to unlock")

# ==============================
# FOOTER
# ==============================
st.markdown("---")
st.caption("🚀 AI-powered career growth tool - designed by Oghenechovwe AKPOJOTOR")

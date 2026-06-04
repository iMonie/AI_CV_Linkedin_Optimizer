import streamlit as st
from openai import OpenAI
import smtplib
from email.mime.text import MIMEText
import time
import random
from datetime import datetime, timedelta
import urllib.parse
import re

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
h1, h2, h3 {
    color: #111 !important;
}
</style>
""", unsafe_allow_html=True)

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
# 🔍 KEYWORD MATCH FUNCTION
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
# HEADER
# ==============================
st.title("🚀 AI CV Optimizer + Job Match")

# ==============================
# INPUT
# ==============================
st.markdown("### 📄 Paste your CV")
cv = st.text_area("", height=200)

st.markdown("### 💼 Paste Job Description (Optional)")
jd = st.text_area("", height=200)

st.markdown("### 📧 Email")
email = st.text_input("")

# ==============================
# PLAN
# ==============================
query_params = st.query_params
plan = query_params.get("plan")

# ==============================
# MAIN
# ==============================
if plan in ["basic", "premium"]:

    if cv and email:

        if st.button("🚀 Generate"):

            # ==============================
            # 🔥 MATCH SCORE DISPLAY
            # ==============================
            score, missing = calculate_match(cv, jd)

            if score is not None:
                st.markdown("## 🎯 Job Match Score")

                st.progress(score / 100)

                if score >= 80:
                    st.success(f"🔥 Strong Match: {score}%")
                elif score >= 50:
                    st.warning(f"⚠️ متوسط Match: {score}%")
                else:
                    st.error(f"❌ Weak Match: {score}%")

                if missing:
                    st.markdown("### ❗ Missing Keywords")
                    st.write(", ".join(missing))

            # ==============================
            # ⏳ LOADING
            # ==============================
            progress = st.progress(0)
            for i in range(100):
                time.sleep(0.01)
                progress.progress(i + 1)

            # ==============================
            # PROMPT
            # ==============================
            if plan == "basic":
                prompt = f"""
Improve this CV professionally:
- ATS friendly
- Better bullet points

CV:
{cv}
"""
            else:
                prompt = f"""
You are an expert recruiter.

Resume:
{cv}

Job Description:
{jd}

TASKS:
- Rewrite CV (results-driven)
- Add achievements with metrics
- Compare CV vs JD → show gaps
- Extract & integrate top 20 keywords
- Optimize for ATS
- Create LinkedIn (Headline, About, Skills)
- Create Cover Letter
- Create Job-tailored CV
"""

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )

            result = response.choices[0].message.content

            st.success("Done ✅")

            st.download_button("Download", result)

            send_email(email, result)

        # ==============================
        # 🚀 VIRAL HOOK
        # ==============================
        st.markdown("---")
        st.markdown("## 🚀 Want Recruiters to FIND You?")

        st.info("""
Top candidates show up DAILY on LinkedIn.
""")

        st.link_button(
            "Increase visibility now",
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

    else:
        st.info("Enter CV + email")

else:
    st.error("Complete payment")

# ==============================
# FOOTER
# ==============================
st.caption("🚀 Built to get you hired faster")

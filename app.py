import streamlit as st
from openai import OpenAI
import smtplib
from email.mime.text import MIMEText
import time
import random
from datetime import datetime, timedelta
import urllib.parse

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
.premium-card {
    background: white;
    padding: 20px;
    border-radius: 15px;
    border: 2px solid #2563eb;
    box-shadow: 0 0 25px rgba(37, 99, 235, 0.4);
}
.basic-card {
    background: white;
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #ddd;
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
        msg['Subject'] = "🚀 Your AI Optimized CV + LinkedIn"
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
# HEADER
# ==============================
st.title("🚀 AI CV + LinkedIn Optimizer")

# ==============================
# PLAN
# ==============================
query_params = st.query_params
plan = query_params.get("plan")

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
# REFERRAL STATE
# ==============================
if "ref_count" not in st.session_state:
    st.session_state.ref_count = random.randint(0, 5)

ref_link = f"https://yourapp.streamlit.app/?ref={random.randint(1000,9999)}"

# ==============================
# MAIN
# ==============================
if plan in ["basic", "premium"]:

    if cv and email:

        if st.button("🚀 Generate"):

            progress = st.progress(0)
            for i in range(100):
                time.sleep(0.01)
                progress.progress(i + 1)

            if plan == "basic":
                prompt = f"""
Improve this CV:
- Make ATS friendly
- Improve bullet points

CV:
{cv}
"""

            else:
                prompt = f"""
You are an expert recruiter and strategist.

=== CONTEXT ===
Resume:
{cv}

Job Description (if provided):
{jd}

=== TASKS ===

1. Rewrite CV to be highly competitive and results-driven.

2. Turn responsibilities into strong achievements with metrics.
If key data is missing, highlight where metrics can be added.

3. Compare CV vs Job Description:
- Identify missing skills
- Show gaps clearly
- Suggest what to reframe vs what to learn

4. Extract top 20 keywords from Job Description
- Integrate them naturally into CV

5. Optimize for ATS + recruiter psychology

6. Create:
- LinkedIn Headline
- LinkedIn About
- Skills Section
- Improved Experience bullets

7. Position candidate as TOP 1%

8. Create:
- Job-tailored CV
- Cover Letter

IMPORTANT:
Return results in clearly separated sections.
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
        # 🧲 REFERRAL SYSTEM
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
    st.error("Complete payment")

# ==============================
# FOOTER
# ==============================
st.caption("Built for serious job seekers 🚀")

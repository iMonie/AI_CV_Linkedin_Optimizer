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

st.markdown("""<style>
.stApp {background: linear-gradient(135deg, #eef2ff, #ffffff);}
</style>""", unsafe_allow_html=True)

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
# 🔥 HEADER
# ==============================
st.title("🚀 AI CV + LinkedIn Optimizer")

# ==============================
# INPUT
# ==============================
cv = st.text_area("Paste your CV")
email = st.text_input("Email")

plan = st.query_params.get("plan")

# ==============================
# MAIN LOGIC
# ==============================
if plan in ["basic", "premium"]:

    if cv and email:

        if st.button("🚀 Generate My CV"):

            progress = st.progress(0)
            status = st.empty()

            for i in range(100):
                time.sleep(0.01)
                progress.progress(i + 1)

            # ==============================
            # PROMPT
            # ==============================
            if plan == "basic":
                prompt = f"""
Improve this CV professionally:
- Make it ATS friendly
- Improve bullet points
- Clean formatting

CV:
{cv}
"""
            else:
                prompt = f"""
You are an expert recruiter and strategist.

1. Rewrite this CV to be highly competitive.
2. Rewrite it to be results-driven with strong metrics - quantified, and impactful.
3. Optimize for ATS and recruiter psychology & visibility.
4. Suggest improvements for structure and keywords.
5. Create a strong LinkedIn profile including:
   - LinkedIn Headline
   - LinkedIn About Section
   - Key Skills Section
   - Experience bullet improvements
6. Position candidate as top 1%
7. Add strong achievements
8. Job tailored CV
9. Create Cover Letter 

CV:
{cv}
"""

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )

        result = response.choices[0].message.content

        st.success("🎉 CV Ready!")
        st.download_button("Download", result)

        send_email(email, result)

            # ==============================
            # 🚀 VIRAL HOOK
            # ==============================
            st.markdown("---")
            st.markdown("## 🚀 Want Recruiters to FIND You?")

            st.info("""
Your CV is strong...

But visibility gets jobs.

Top candidates show up daily on LinkedIn.
""")

            st.link_button(
                "Grow on LinkedIn",
                "https://socials.scaleplant.com/en/?c=AKPOJOTOWY46"
            )

            # ==============================
            # 📲 WHATSAPP CLOSER
            # ==============================
            st.markdown("## 💬 Get Personal Help")

            msg = """
Hi, I used your AI CV tool.

I want help getting a job fast.
"""

            encoded = urllib.parse.quote(msg)

            st.link_button(
                "Chat on WhatsApp",
                f"https://wa.me/2348035341982?text={encoded}"
            )

            # ==============================
            # 💰 OFFER
            # ==============================
            st.markdown("## 💎 Guaranteed Results Package")

            st.warning("""
✔ Done-for-you CV  
✔ LinkedIn optimization  
✔ 1-on-1 strategy  

💰 ₦5,000
""")

            premium_msg = urllib.parse.quote(
                "I want the 5k package"
            )

            st.link_button(
                "Secure Spot",
                f"https://wa.me/2348035341982?text={premium_msg}"
            )

else:
    st.error("❌ Complete payment to unlock")

# ==============================
# FOOTER
# ==============================
st.markdown("---")
st.caption("Built for speed & income 🚀")

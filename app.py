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
# 🔗 REFERRAL SYSTEM
# ==============================
query_params = st.query_params
ref = query_params.get("ref")

if "ref_count" not in st.session_state:
    st.session_state.ref_count = 0

if ref:
    st.session_state.ref_count += 1

user_id = str(random.randint(10000, 99999))
ref_link = f"https://yourapp.streamlit.app/?ref={user_id}"

# ==============================
# 🔥 LIVE USERS
# ==============================
live_users = random.randint(12, 47)
st.markdown(f"🔥 **{live_users} people are using this right now**")

# ==============================
# ⏳ COUNTDOWN
# ==============================
end_time = datetime.now() + timedelta(minutes=15)
remaining = end_time - datetime.now()
st.warning(f"⏳ Offer expires in {remaining.seconds//60} minutes")

# ==============================
# 🎯 HEADER
# ==============================
st.title("🚀 AI CV + LinkedIn Optimizer")
st.write("🔥 Beat 99% of applicants. Get hired faster.")

st.markdown("---")

# ==============================
# 💳 PAYMENT
# ==============================
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 💼 Basic (Free)")
    st.link_button("Start Free", "https://selar.co/11180kb0j4")

with col2:
    st.markdown("### 💎 Premium")
    st.markdown("~~₦10,000~~  **₦1,000 Today**")
    st.link_button("Upgrade Now", "https://selar.co/m001q0082z")

st.markdown("---")

# ==============================
# 📥 INPUT
# ==============================
cv = st.text_area("📄 Paste your CV", height=200)
email = st.text_input("📧 Enter your email")

plan = query_params.get("plan", "basic")

# ==============================
# 🚀 GENERATION
# ==============================
if cv and email:

    if st.button("🚀 Generate My CV"):

        progress = st.progress(0)
        status = st.empty()

        steps = [
            "🔍 Analyzing CV...",
            "🧠 Applying recruiter logic...",
            "⚡ Optimizing bullet points...",
            "📈 Adding achievements...",
            "🎯 Finalizing..."
        ]

        for i in range(100):
            time.sleep(0.02)
            progress.progress(i + 1)
            status.text(random.choice(steps))

        # ==============================
        # ✅ YOUR EXACT PROMPT (UNCHANGED)
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

        # ==============================
        # AI CALL
        # ==============================
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        result = response.choices[0].message.content

        # ==============================
        # OUTPUT
        # ==============================
        st.success("🎉 CV Ready!")
        st.download_button("Download", result)

        send_email(email, result)

        # ==============================
        # EXTRA UI
        # ==============================
        st.markdown("---")
        st.markdown("## 💬 Get Help Fast")

        msg = "I want help getting a job fast"
        encoded = urllib.parse.quote(msg)

        st.link_button(
            "Chat on WhatsApp",
            f"https://wa.me/YOUR_NUMBER?text={encoded}"
        )

        st.markdown("---")
        st.markdown("## 🎁 Referral Rewards")

        st.success(f"Your link: {ref_link}")
        st.write(f"Referrals: {st.session_state.ref_count}")

else:
    st.info("Enter CV + email")

# ==============================
# FOOTER
# ==============================
st.markdown("---")
st.caption("🚀 Built for income + impact")

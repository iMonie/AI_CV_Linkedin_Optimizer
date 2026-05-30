import streamlit as st
from openai import OpenAI
import smtplib
from email.mime.text import MIMEText
import time
import random

# ==============================
# 🎨 CUSTOM DARK UI
# ==============================
st.set_page_config(page_title="AI CV + LinkedIn Optimizer", page_icon="🚀")

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0a192f, #020c1b);
    color: white;
}
h1, h2, h3, h4, p {
    color: white !important;
    font-weight: bold;
}
textarea, input {
    background-color: #112240 !important;
    color: white !important;
    border-radius: 10px;
}
.stButton>button {
    background-color: #64ffda;
    color: black;
    border-radius: 10px;
    font-weight: bold;
}
.stDownloadButton>button {
    background-color: #00c853;
    color: white;
    border-radius: 10px;
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
# 🔥 FAKE LIVE USERS COUNTER
# ==============================
live_users = random.randint(12, 47)
st.markdown(f"🔥 **{live_users} people are using this right now**")

# ==============================
# 🎯 HEADER
# ==============================
st.title("🚀 AI CV + LinkedIn Optimizer")
st.write("🔥 Beat 95% of applicants. Get hired faster.")

st.markdown("---")

# ==============================
# 💬 TESTIMONIALS
# ==============================
st.markdown("## 💬 What Users Are Saying")

col1, col2, col3 = st.columns(3)

with col1:
    st.success("⭐️⭐️⭐️⭐️⭐️\n\n'I got 3 interviews in 1 week!' — Sarah")

with col2:
    st.success("⭐️⭐️⭐️⭐️⭐️\n\n'Recruiters started replying instantly' — David")

with col3:
    st.success("⭐️⭐️⭐️⭐️⭐️\n\n'My CV finally looks professional!' — Chioma")

st.markdown("---")

# ==============================
# 💳 PAYMENT
# ==============================
st.markdown("## 💳 Choose Your Package")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 💼 Basic (Free)")
    st.write("""
✔ ATS Optimized CV  
✔ Better bullet points  
✔ Clean formatting  
""")
    st.link_button("Start Free", "https://selar.co/11180kb0j4")

with col2:
    st.markdown("### 💎 Premium (LIMITED OFFER)")
    st.write("""
🔥 EVERYTHING in Basic PLUS:

✔ LinkedIn Headline
✔ LinkedIn About Section
✔ Skills Optimization
✔ Recruiter-Level Rewrite
✔ Achievement Metrics
✔ Cover Letter
✔ Job-tailored CV 

⏳ Limited slots today
""")
    st.link_button("Upgrade Now 🚀", "https://selar.co/m001q0082z")

st.markdown("---")

# ==============================
# 🔍 PLAN CHECK
# ==============================
query_params = st.query_params
plan = query_params.get("plan")

# ==============================
# 📥 INPUT
# ==============================
st.markdown("### 📄 Paste your CV here")
cv = st.text_area(" ", height=200)

st.markdown("### 📧 Enter your email")
email = st.text_input(" ")

# ==============================
# 🚀 MAIN LOGIC
# ==============================
if plan in ["basic", "premium"]:

    if plan == "basic":
        st.success("✅ Basic Plan Activated")
        st.warning("🚀 Upgrade to Premium for 10x better results")
        st.link_button("Upgrade Now", "https://selar.co/m001q0082z")

    else:
        st.success("💎 Premium Activated")

    if cv and email:

        if st.button("🚀 Generate My CV"):

            # ==============================
            # ⚡ ANIMATED LOADING
            # ==============================
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
            # 🤖 AI
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

            st.success("🎉 Your CV is Ready!")

            st.download_button("📥 Download", result, file_name="optimized_cv.txt")

            if send_email(email, result):
                st.success("📩 Sent to your email!")
            else:
                st.warning("⚠️ Email failed")

    else:
        st.info("Enter CV + email")

else:
    st.error("❌ Complete payment to unlock")

# ==============================
# FOOTER
# ==============================
st.markdown("---")
st.caption("🚀 AI-powered career growth tool")

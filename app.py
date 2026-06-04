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
transform: scale(1.02);
}
.basic-card {
background: white;
padding: 20px;
border-radius: 15px;
border: 1px solid #ddd;
}
textarea, input {
background-color: #ffffff !important;
color: #111 !important;
border-radius: 10px;
border: 1px solid #ddd;
}
.stButton>button {
background-color: #2563eb;
color: white;
border-radius: 10px;
font-weight: bold;
}
.stDownloadButton>button {
background-color: #16a34a;
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
    except Exception as e:
        st.error(f"Email error: {e}")
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
ref_link = f"https://aicvlinkedinoptimizer-hlhavswrjy84dp8obmejp4.streamlit.app/?ref={user_id}"

# ==============================
# 🔥 LIVE USERS
# ==============================
live_users = random.randint(12, 47)
st.markdown(f"🔥 **{live_users} people are using this right now**")

# ==============================
# ⏳ COUNTDOWN
# ==============================
if "end_time" not in st.session_state:
    st.session_state.end_time = datetime.now() + timedelta(minutes=15)

remaining = st.session_state.end_time - datetime.now()

if remaining.total_seconds() > 0:
    minutes = int(remaining.total_seconds() // 60)
    seconds = int(remaining.total_seconds() % 60)
    st.warning(f"⏳ Offer expires in {minutes}:{seconds:02d}")
else:
    st.error("❌ Offer expired! Price returned to ₦10,000")

# ==============================
# 🎯 HEADER
# ==============================
st.title("🚀 AI CV + LinkedIn Optimizer")
st.write("🔥 Beat 99% of applicants. Get PREMIUM. Get hired x10 faster.")

st.markdown("---")

# ==============================
# 💳 PAYMENT (UPDATED LOGIC ONLY)
# ==============================
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="basic-card">', unsafe_allow_html=True)
    st.markdown("### 💼 Basic (Free)")
    st.write("""
✔ ATS Optimized CV  
✔ Better bullet points  
✔ Clean formatting  
""")
    if st.button("Start Free"):
        st.session_state.plan = "basic"
    st.link_button("Continue Free", "https://selar.co/11180kb0j4")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    st.markdown("### 💎 Premium")
    st.markdown("~~₦10,000~~  **₦1,000 Today**")
    st.write("""
🔥 EVERYTHING in Basic PLUS:

✔ LinkedIn Headline  
✔ LinkedIn About Section  
✔ Skills Optimization  
✔ Recruiter-Level Rewrite  
✔ Achievement Metrics  
✔ Cover Letter  
✔ Job-tailored CV  
""")
    if st.button("Upgrade Now 🚀"):
        st.session_state.plan = "premium"
    st.link_button("Pay Here", "https://selar.co/m001q0082z")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# ==============================
# 📥 INPUT
# ==============================
st.markdown("### 📄 Paste your CV here")
cv = st.text_area(" ", height=200)

st.markdown("### 📧 Enter your email")
email = st.text_input(" ")

# ==============================
# 🧠 PLAN DEFAULT FIXED
# ==============================
plan = st.session_state.get("plan", "basic")

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

1. Rewrite this CV to be highly competitive and impactful.
2. Rewrite it to be results-driven with strong metrics and quantified.
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
        st.download_button("📥 Download", result)

        if send_email(email, result):
            st.success("📩 Sent to your email!")

        # 🔥 PREMIUM TEASE
        if plan == "basic":
            st.warning("""
⚠️ This is the FREE version.

Upgrade to unlock:
✔ LinkedIn optimization  
✔ Recruiter positioning 
✔ A results-driven CV with strong metrics
✔ CV that is optimized for ATS and recruiter psychology & visibility.
✔ Suggest improvements for structure and keywords
✔ Cover letter  

Upgrade now 🚀
""")

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

        st.link_button("Start Growing x10 FASTER", "https://socials.scaleplant.com/en/?c=AKPOJOTOWY46")

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
        # 🧲 REFERRAL SYSTEM UI
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

# ==============================
# FOOTER
# ==============================
st.markdown("---")
st.caption("🚀 Designed for income & impact by Oghenechovwe AKPOJOTOR")

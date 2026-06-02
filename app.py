import streamlit as st
from openai import OpenAI
import smtplib
from email.mime.text import MIMEText
import time
import random
from datetime import datetime, timedelta
import urllib.parse  # ✅ ADDED

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

/* Premium Glow */
.premium-card {
    background: white;
    padding: 20px;
    border-radius: 15px;
    border: 2px solid #2563eb;
    box-shadow: 0 0 25px rgba(37, 99, 235, 0.4);
    transform: scale(1.02);
}

/* Basic Card */
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
    except:
        return False

# ==============================
# 🔥 LIVE USERS COUNTER
# ==============================
live_users = random.randint(12, 47)
st.markdown(f"🔥 **{live_users} people are using this right now**")

# ==============================
# 🛒 FAKE PURCHASE POPUP
# ==============================
names = ["John", "David", "Sarah", "Chioma", "Michael", "Aisha", "Emeka", "Efe", "Musa", "Angela"]
cities = ["Lagos", "Abuja", "Port Harcourt", "Ibadan", "Warri", "Benin", "Asaba", "Enugu"]

popup_placeholder = st.empty()

name = random.choice(names)
city = random.choice(cities)

message = random.choice([
    f"🔥 {name} from {city} just upgraded to Premium 💎",
    f"🚀 {name} just optimized their CV",
    f"💼 {name} just unlocked Premium features",
])

popup_placeholder.success(message)

# ==============================
# 🎯 HEADER
# ==============================
st.title("🚀 AI CV + LinkedIn Optimizer")
st.write("🔥 Beat 99% of applicants. Get PREMIUM. Get hired X10 faster.")

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
    st.markdown('<div class="basic-card">', unsafe_allow_html=True)
    st.markdown("### 💼 Basic  (Free)")
    st.write("""
✔ ATS Optimized CV  
✔ Better bullet points  
✔ Clean formatting  
""")
    st.link_button("Start Free", "https://selar.co/11180kb0j4")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    st.markdown("### 💎 Premium")
    st.markdown("~~₦10,000~~  **₦1,000 (Today Only)**")
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
    st.link_button("Upgrade Now 🚀", "https://selar.co/m001q0082z")
    st.markdown('</div>', unsafe_allow_html=True)

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

            progress = st.progress(0)
            status = st.empty()

            for i in range(100):
                time.sleep(0.02)
                progress.progress(i + 1)
                status.text(random.choice([
                    "Analyzing CV...",
                    "Applying recruiter logic...",
                    "Optimizing...",
                    "Finalizing..."
                ]))

            prompt = f"Rewrite this CV professionally:\n{cv}"

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )

            result = response.choices[0].message.content

            st.success("🎉 Your CV is Ready!")
            st.download_button("📥 Download", result)

            send_email(email, result)

            # ==============================
            # 🚀 VIRAL HOOK (NEW)
            # ==============================
            st.markdown("---")
            st.markdown("## 🚀 Want Recruiters to FIND You?")

            st.info("""
Your CV is now strong…

But jobs come from VISIBILITY.

Top candidates show up daily on LinkedIn.
""")

            st.link_button(
                "Start Growing on LinkedIn",
                "https://socials.scaleplant.com/en/?c=AKPOJOTOWY46"
            )

            # ==============================
            # 📲 WHATSAPP CLOSER (ENHANCED)
            # ==============================
            st.markdown("## 💬 Get Personal Help (FASTEST WAY TO GET HIRED)")

            msg = """
Hi, I just used your AI CV tool.

I want serious help getting a job fast.
I am ready to take action.
"""

            encoded = urllib.parse.quote(msg)

            st.link_button(
                "Chat on WhatsApp",
                f"https://wa.me/2348035341982?text={encoded}"
            )

            # ==============================
            # 💰 ₦5K OFFER (ENHANCED POSITIONING)
            # ==============================
            st.markdown("## 💎 Want GUARANTEED Results?")

            st.warning("""
🔥 AI Career Acceleration Package

✔ Done-for-you CV rewrite  
✔ LinkedIn optimization  
✔ 1-on-1 strategy session  
✔ Visibility system  

💰 ₦5,000
""")

            premium_msg = urllib.parse.quote(
                "I want the 5k career acceleration package"
            )

            st.link_button(
                "Secure Your Spot Now",
                f"https://wa.me/2348035341982?text={premium_msg}"
            )

else:
    st.error("❌ Complete payment to unlock")

# ==============================
# FOOTER
# ==============================
st.markdown("---")
st.caption("🚀 AI-powered career growth tool - designed by Oghenechovwe AKPOJOTOR")

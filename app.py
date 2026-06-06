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

st.set_page_config(page_title="AI CV Optimizer", page_icon="🚀")

st.title("🚀 AI That Matches Your CV to Any Job Description (ATS + Recruiter Approved)")

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
    except:
        return False

# ==============================
# 🔥 LIVE USERS COUNTER
# ==============================
live_users = random.randint(12, 47)
st.markdown(f"🔥 **{live_users} people are using this right now**")

# ==============================
# 🛒 POPUP
# ==============================
names = ["John", "David", "Sarah", "Chioma", "Michael"]
cities = ["Lagos", "Abuja", "Port Harcourt"]

st.success(f"🔥 {random.choice(names)} from {random.choice(cities)} just upgraded to Premium 💎")

# ==============================
# HEADER
# ==============================
st.title("🚀 AI CV + LinkedIn Optimizer")
st.write("🔥 Beat 99% of applicants. Get PREMIUM. Get hired X10 faster.")

st.markdown("---")

# ==============================
# 💳 PAYMENT UI
# ==============================
st.markdown("## 💳 Choose Your Package")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div style="
        background:white;
        padding:25px;
        border-radius:15px;
        border:1px solid #e5e7eb;
        box-shadow:0 5px 15px rgba(0,0,0,0.05);
    ">
    <h3>💼 Basic (Free)</h3>
    <p>✔ ATS Optimized CV</p>
    <p>✔ Better bullet points</p>
    <p>✔ Clean formatting</p>
    <br>
    <p style="color:#6b7280;">Perfect for quick improvement</p>
    </div>
    """, unsafe_allow_html=True)

    st.link_button("Start Free", "https://selar.co/11180kb0j4")

with col2:
    st.markdown("""
    <div style="
        background:white;
        padding:25px;
        border-radius:15px;
        border:2px solid #2563eb;
        box-shadow:0 0 30px rgba(37,99,235,0.35);
        transform:scale(1.03);
    ">
    <h3>💎 Premium</h3>
    <p style="font-size:20px;">
    <span style="text-decoration:line-through;color:gray;">₦10,000</span>
    <strong style="color:#16a34a;"> ₦1,000 Today</strong>
    </p>
    <hr>
    <p>🔥 EVERYTHING in Basic PLUS:</p>
    <p>✔ LinkedIn Headline</p>
    <p>✔ LinkedIn About Section</p>
    <p>✔ Skills Optimization</p>
    <p>✔ Recruiter-Level Rewrite</p>
    <p>✔ Achievement Metrics</p>
    <p>✔ Cover Letter</p>
    <p>✔ Job-tailored CV</p>
    </div>
    """, unsafe_allow_html=True)

    st.link_button("Upgrade Now 🚀", "https://selar.co/m001q0082z")

st.markdown("---")

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

st.markdown("### 🧾 Paste Job Description (Optional)")
jd = st.text_area("", height=150)

st.markdown("### 📧 Email")
email = st.text_input("")

# ==============================
# 🚀 MAIN LOGIC
# ==============================
if plan in ["basic", "premium"]:

    if plan == "basic":
        st.success("✅ Basic Plan Activated")
        st.warning("🚀 Upgrade to Premium for full results")
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
                status.text("Processing...")

            # ==============================
            # STRICT PROMPT CONTROL
            # ==============================
            if plan == "basic":

                prompt = f"""
You are a professional CV optimizer.

STRICT RULE:
- ONLY optimize CV
- DO NOT include LinkedIn
- DO NOT include Cover Letter
- DO NOT include extra sections

OUTPUT:
- Clean ATS CV
- Improved bullet points
- Better formatting

CV:
{cv}
"""

            else:
                if jd and jd.strip() != "":
                    prompt = f"""
You are a TOP 1% recruiter.

Most hired candidates score 80%+

1. Match Score (%)
2. Skill gaps
3. Top 20 keywords
4. Achievement rewrite
5. Full ATS CV
6. LinkedIn profile
7. Cover Letter

CV:
{cv}

JOB DESCRIPTION:
{jd}
"""
                else:
                    prompt = f"""
You are a TOP recruiter.

Provide:
- Full ATS CV
- LinkedIn profile
- Cover Letter

CV:
{cv}
"""

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )

            result = response.choices[0].message.content

            st.success("✅ Done")

            # ==============================
            # OUTPUT CONTROL
            # ==============================
            if plan == "basic":
                st.write(result)

                st.warning("🔒 LinkedIn + Cover Letter locked in Premium")

                st.link_button("Upgrade to Premium 🚀", "https://selar.co/m001q0082z")

            else:
                st.write(result)

            st.download_button("📥 Download", result)
            send_email(email, result)

        # ==============================
        # VIRAL HOOK
        # ==============================
        st.markdown("---")

        st.markdown("""
## 🚀 Want Recruiters to FIND You?

I found a tool that:

✔ Writes posts for you  
✔ Plans your entire week  
✔ Schedules everything automatically  

Basically… it removes excuses.

🚨 Don’t Stay Invisible  
Someone less skilled than you is winning…  
Because they show up DAILY.  

You don’t.

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

    else:
        st.info("Enter CV + email")

else:
    st.error("❌ Complete payment first")

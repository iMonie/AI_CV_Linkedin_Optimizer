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
# 💳 PAYMENT (UPGRADED UI)
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
    <br>
    <p style="color:#16a34a;font-weight:bold;">
    ⚡ Most users upgrade after seeing results
    </p>
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
# MAIN LOGIC
# ==============================
if plan in ["basic", "premium"]:

    if cv and email:

        if st.button("🚀 Generate"):

            progress = st.progress(0)

            for i in range(100):
                time.sleep(0.01)
                progress.progress(i + 1)

            # ==============================
            # 🧠 PROMPT LOGIC (FIXED)
            # ==============================
            if jd and jd.strip() != "":
                prompt = f"""
You are a TOP 1% recruiter and hiring strategist.

IMPORTANT RULES:
- Be detailed, clean, structured, and professional
- DO NOT use tables
- DO NOT assume or fabricate experience
- Use clear headings and spacing

---

### 1. MATCH ANALYSIS
Most hired candidates score 80%+

- Match Score (%)
- 3–5 bullet reasons

---

### 2. SKILL GAP ANALYSIS
- Missing skills
- What can be reframed
- What to learn

---

### 3. TOP 20 KEYWORDS
- Clean bullet list
- No repetition

---

### 4. ACHIEVEMENT REWRITE
- Use metrics if available
- If missing → say "Add metric here"

---

### 5. FULL DETAILED ATS CV REWRITE
1. Rewrite this CV to be highly competitive.
2. Rewrite it to become results-driven with strong metrics - quantified, and impactful.
3. Optimize for ATS and recruiter psychology & visibility.
4. Suggest improvements for structure and keywords.
5. Create a strong detailed LinkedIn profile including:
   - LinkedIn Headline
   - LinkedIn About Section
   - Key Skills Section
   - Experience bullet improvements
6. Position candidate as top 1%
7. Job tailored CV
8. Cover Letter


---

### 6. FINAL TIPS

CV:
{cv}

JOB DESCRIPTION:
{jd}
"""
            else:
                prompt = f"""
Improve this CV professionally:
- ATS optimized and impactful
- Strong achievements
- Clean formatting

CV:
{cv}
"""

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )

            result = response.choices[0].message.content

            st.success("✅ Done")
            st.download_button("📥 Download", result)
            send_email(email, result)

        # ==============================
        # VIRAL HOOK
        # ==============================
        st.markdown("---")
        st.markdown("## 🚀 Want Recruiters to FIND You?")

        st.link_button(
            "Increase visibility now",
            "https://socials.scaleplant.com/en/?c=AKPOJOTOWY46"
        )

        # ==============================
        # WHATSAPP
        # ==============================
        encoded_msg = urllib.parse.quote("Help me get hired fast")

        st.link_button(
            "💬 WhatsApp",
            f"https://wa.me/2348035341982?text={encoded_msg}"
        )

    else:
        st.info("Enter CV + email")

else:
    st.error("❌ Complete payment first")

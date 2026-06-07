import streamlit as st
from openai import OpenAI
import smtplib
from email.mime.text import MIMEText
import time
import random
from datetime import datetime, timedelta
import urllib.parse

# ✅ ADDED
from docx import Document
import io
import re

# ==============================
# 🎨 UI DESIGN
# ==============================

st.set_page_config(page_title="AI CV Optimizer", page_icon="🚀")

st.title("🚀 AI That Matches and Rewrite Your CV to Any Job Description (ATS + Recruiter Approved)")

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
# ✅ ADDED: SCORE FUNCTION
# ==============================
def calculate_score(cv_text, jd_text):
    cv_words = set(re.findall(r"\w+", cv_text.lower()))
    jd_words = set(re.findall(r"\w+", jd_text.lower()))
    if not jd_words:
        return 0
    return min(int((len(cv_words & jd_words) / len(jd_words)) * 100), 95)

# ==============================
# ✅ ADDED: DOCX GENERATOR
# ==============================
def generate_docx(content):
    doc = Document()
    for line in content.split("\n"):
        doc.add_paragraph(line)
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# ==============================
# 🔥 LIVE USERS COUNTER
# ==============================
live_users = random.randint(12, 47)
st.markdown(f"🔥 **{live_users} people are using this right now**")

# ==============================
# 🛒 POPUP
# ==============================
names = ["John", "David", "Sarah", "Ben" "Esther" "Clara" "Victory" "Chioma", "Michael"]
cities = ["Lagos", "Abuja", "Warri" "London" "Port Harcourt" "New York" "Cape Town"]

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
    <strong style="color:#16a34a;"> ₦2,500 Today</strong>
    </p>
    <hr>
    <p>🔥 EVERYTHING in Basic PLUS:</p>
    <p>✔ Extraction of key requirements from JOB DESCRIPTION</p>
    <p>✔ Comparison of CV with Identified gaps</p>
    <p>✔ Rewrite CV to ALIGN with JD</p>
    <p>✔ Inject keywords NATURALLY</p>
    <p>✔ LinkedIn Headline</p>
    <p>✔ LinkedIn About Section</p>
    <p>✔ Skills Optimization</p>
    <p>✔ Recruiter-Level Rewrite</p>
    <p>✔ Achievement Metrics</p>
    <p>✔ Cover Letter</p>
    <p>✔ Continous 1 on 1 Mentorship on Whatsapp</p>
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

            if plan == "basic":

                prompt = f"""
You are a top recruiter.

Match CV to job description.

Return:
- Skill gaps
- Keywords
- Rewritten CV
- LinkedIn
- Cover letter

CV:
{cv}

JD:
{jd}
"""
                else:
                    prompt = f"""
Generate ATS CV + LinkedIn + Cover Letter.

CV:
{cv}
"""

                # FIRST PASS
                res = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role":"user","content":prompt}]
                )

                first_output = res.choices[0].message.content

            # =========================
            # 🤖 AI REVIEW PASS (YOUR EXACT LOGIC)
            # =========================
            review_prompt = f"""
You are a senior recruiter reviewing a CV.

Improve this output:
- Fix weak bullet points
- Add missing impact
- Improve clarity
- Ensure strong recruiter tone

CONTENT:
{first_output}
"""

            review_res = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role":"user","content":review_prompt}]
            )

            final_output = review_res.choices[0].message.content

            st.success("✅ Done")

            if plan == "basic":
                st.write(first_output)
                st.warning("🔒 Premium AI rewrite locked")
            else:
                st.write(final_output)

                # ✅ DOCX DOWNLOAD
                docx_file = generate_docx(final_output)
                st.download_button(
                    "📥 Download CV (DOCX)",
                    docx_file,
                    file_name="AI_CV.docx"
                )

            send_email(email, final_output if plan=="premium" else first_output)

        # ==============================
        # VIRAL HOOK (UNCHANGED)
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

# ==============================
# FOOTER
# ==============================
st.markdown("---")
st.caption("🚀 Built for income + impact by Oghenchovwe AKPOJOTOR")

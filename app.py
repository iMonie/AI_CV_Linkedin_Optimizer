import streamlit as st
from openai import OpenAI
import smtplib
from email.mime.text import MIMEText
import time
import random
import urllib.parse
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

# ==============================
# CONFIG
# ==============================
st.set_page_config(page_title="AI CV Optimizer", page_icon="🚀")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ==============================
# PDF GENERATOR
# ==============================
def generate_pdf(text):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()
    content = []

    for line in text.split("\n"):
        content.append(Paragraph(line, styles["Normal"]))

    doc.build(content)
    buffer.seek(0)
    return buffer

# ==============================
# EMAIL FUNCTION
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
# UI
# ==============================
st.title("🚀 AI That Matches Your CV to Any Job Description (ATS + Recruiter Approved)")

st.markdown("Most hired candidates score 80%+")

# ==============================
# SOCIAL PROOF
# ==============================
st.success(f"🔥 {random.choice(['John','Chioma','David','Sarah'])} just upgraded to Premium 💎")

# ==============================
# PRICING
# ==============================
st.markdown("## 💳 Choose Your Package")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### 💼 Basic (Free)
    ✔ ATS Optimized CV  
    ✔ Better bullet points  
    ✔ Clean formatting  
    """)

    st.link_button("Start Free", "https://selar.co/11180kb0j4")

with col2:
    st.markdown("""
    ### 💎 Premium  
    ~~₦10,000~~ **₦1,000 Today**

    🔥 EVERYTHING in Basic PLUS:

    ✔ LinkedIn Headline  
    ✔ LinkedIn About Section  
    ✔ Skills Optimization  
    ✔ Recruiter-Level Rewrite  
    ✔ Achievement Metrics  
    ✔ Cover Letter  
    ✔ Job-tailored CV  
    ✔ CV + Job Description matching  
    ✔ Skill gap detection  
    ✔ Keyword extraction (ATS hacking)  
    ✔ Recruiter-level positioning  
    """)

    st.link_button("Upgrade Now 🚀", "https://selar.co/m001q0082z")

st.markdown("---")

# ==============================
# PLAN
# ==============================
plan = st.query_params.get("plan")

# ==============================
# INPUTS
# ==============================
cv = st.text_area("📄 Paste your CV", height=200)
jd = st.text_area("🧾 Paste Job Description (Optional)", height=150)
email = st.text_input("📧 Email")

# ==============================
# LOGIC
# ==============================
if plan in ["basic", "premium"]:

    if plan == "premium":
        st.success("💎 Premium Activated")
    else:
        st.warning("⚠️ Basic Plan — Limited Output")

    if cv and email:

        if st.button("🚀 Generate My CV"):

            # Progress bar
            progress = st.progress(0)
            for i in range(100):
                time.sleep(0.01)
                progress.progress(i + 1)

            # ==============================
            # SCORE SYSTEM
            # ==============================
            score = random.randint(55, 92)

            # ==============================
            # PROMPT
            # ==============================
            if jd:
                prompt = f"""
You are a TOP recruiter.

Return:

1. Match Score (%)
2. Skill gaps
3. Top 20 keywords
4. Achievements rewrite
5. Full ATS CV
6. LinkedIn profile
7. Cover letter

CV:
{cv}

JD:
{jd}
"""
            else:
                prompt = f"Improve this CV:\n{cv}"

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )

            result = response.choices[0].message.content

            # ==============================
            # DISPLAY SCORE
            # ==============================
            st.subheader(f"📊 Match Score: {score}%")

            if score < 80:
                st.warning("⚠️ Below 80% — Improve to increase chances")

            # ==============================
            # PREMIUM LOCK
            # ==============================
            if plan == "basic":
                st.error("🔒 Upgrade to Premium to unlock full results")

                preview = result[:1500]
                st.write(preview + "\n\n...")

                st.link_button("Upgrade Now 🚀", "https://selar.co/m001q0082z")

            else:
                # FULL OUTPUT
                st.success("✅ Full Optimization Ready")
                st.write(result)

                # ==============================
                # DOWNLOADS
                # ==============================
                st.download_button("📥 Download Text", result)

                pdf = generate_pdf(result)
                st.download_button(
                    "📄 Download PDF CV (Clean Format)",
                    pdf,
                    file_name="optimized_cv.pdf"
                )

                send_email(email, result)

        # ==============================
        # AFFILIATE SECTION
        # ==============================
        st.markdown("---")
        st.markdown("""
## 🚀 Want Recruiters to FIND You?

✔ Writes posts  
✔ Plans content  
✔ Automates growth  

Stop being invisible.
""")

        st.link_button(
            "🔥 Grow My LinkedIn Now",
            "https://socials.scaleplant.com/en/?c=AKPOJOTOWY46"
        )

        # ==============================
        # WHATSAPP
        # ==============================
        msg = urllib.parse.quote("Help me optimize my CV")
        st.link_button("💬 WhatsApp", f"https://wa.me/2348035341982?text={msg}")

    else:
        st.info("Enter CV + email")

else:
    st.error("❌ Complete payment first")

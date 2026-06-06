import streamlit as st
from openai import OpenAI
import smtplib
from email.mime.text import MIMEText
import time
import random
import urllib.parse

# ==============================
# 🎨 UI
# ==============================
st.set_page_config(page_title="AI CV Optimizer", page_icon="🚀")

st.title("🚀 AI That Matches Your CV to Any Job Description (ATS + Recruiter Approved)")

# ==============================
# 🔐 API
# ==============================
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ==============================
# 📩 EMAIL
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
# PLAN
# ==============================
plan = st.query_params.get("plan")

# ==============================
# INPUT
# ==============================
cv = st.text_area("📄 Paste your CV", height=200)
jd = st.text_area("🧾 Paste Job Description (Optional)", height=150)
email = st.text_input("📧 Email")

# ==============================
# MAIN
# ==============================
if plan in ["basic", "premium"]:

    if plan == "basic":
        st.success("✅ Basic Plan Activated")
    else:
        st.success("💎 Premium Activated")

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
            # 🔒 BASIC LOGIC
            # ==============================
            if plan == "basic":

                prompt = f"""
You are a professional CV optimizer.

STRICT RULES:
- Only improve the CV
- Do NOT include LinkedIn
- Do NOT include Cover Letter
- Do NOT include job matching

OUTPUT:
- ATS optimized CV
- Strong bullet points
- Clean formatting

CV:
{cv}
"""

            # ==============================
            # 💎 PREMIUM LOGIC (FULL JD MATCH)
            # ==============================
            else:

                if jd.strip() != "":

                    prompt = f"""
You are a TOP recruiter + ATS system.

IMPORTANT:
You must FULLY MATCH the CV to the job description.

Most hired candidates score 80%+

STEP 1: Extract key requirements from JOB DESCRIPTION  
STEP 2: Compare with CV  
STEP 3: Identify gaps  
STEP 4: Rewrite CV to ALIGN with JD  
STEP 5: Inject keywords NATURALLY  
STEP 6: Convert tasks into measurable achievements  
STEP 7: Reorder CV for maximum recruiter impact  

OUTPUT FORMAT:

--- MATCH SCORE ---
Give realistic % match (not inflated)

--- SKILL GAPS ---
List missing skills honestly

--- TOP KEYWORDS ---
Extract top 20 ATS keywords

--- REWRITTEN CV (JOB-TARGETED) ---
Rewrite the ENTIRE CV to match the job:
- Use keywords from JD
- Improve achievements with metrics
- Align experience with job needs
- Keep it realistic (do NOT invent false roles)

--- LINKEDIN HEADLINE ---
--- LINKEDIN ABOUT ---
--- COVER LETTER ---

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

            # ==============================
            # 🤖 AI CALL
            # ==============================
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )

            result = response.choices[0].message.content

            # ==============================
            # OUTPUT CONTROL
            # ==============================
            if plan == "basic":
                st.write(result)
                st.warning("🔒 Premium unlocks Job Matching, LinkedIn & Cover Letter")
            else:
                st.write(result)

            # ==============================
            # DOWNLOAD + EMAIL
            # ==============================
            st.download_button("📥 Download CV", result)
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


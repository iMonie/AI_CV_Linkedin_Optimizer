import streamlit as st
from openai import OpenAI
from docx import Document
import io
import re
import urllib.parse

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="AI CV Optimizer", layout="centered")

# ==============================
# HEADER
# ==============================
st.title("🚀 AI That Matches Your CV to Any Job Description (ATS + Recruiter Approved)")
st.caption("🔥 Beat 99% of applicants")

# ==============================
# INPUTS
# ==============================
cv = st.text_area("📄 Paste your CV", height=250)
jd = st.text_area("🧾 Paste Job Description (Optional)", height=200)
email = st.text_input("📧 Email")

premium = st.checkbox("💎 Premium Activated")

# ==============================
# SCORING FUNCTION
# ==============================
def calculate_score(cv_text, jd_text):
    cv_words = set(re.findall(r"\w+", cv_text.lower()))
    jd_words = set(re.findall(r"\w+", jd_text.lower()))

    if not jd_words:
        return 0

    match = cv_words.intersection(jd_words)
    score = int((len(match) / len(jd_words)) * 100)

    return min(score, 95)


# ==============================
# DOCX EXPORT
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
# MAIN BUTTON
# ==============================
if st.button("🚀 Optimize Now"):

    if cv and email:

        # ==============================
        # BASIC (FREE)
        # ==============================
        if not premium:

            prompt = f"""
Rewrite this CV to be ATS optimized.
Improve bullet points.
Keep it clean and professional.

CV:
{cv}
"""

            res = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )

            output = res.choices[0].message.content

            st.subheader("✅ Optimized CV")
            st.write(output)

        # ==============================
        # 💎 PREMIUM LOGIC (FULL SYSTEM)
        # ==============================
        else:

            if jd.strip() != "":

                score = calculate_score(cv, jd)

                prompt = f"""
You are a TOP recruiter + ATS system.

IMPORTANT:
You must FULLY MATCH the CV to the job description.

Most hired candidates score 80%+

STEP 1: Extract key requirements
STEP 2: Compare with CV
STEP 3: Identify gaps
STEP 4: Rewrite CV aligned to JD
STEP 5: Inject keywords naturally
STEP 6: Add metrics
STEP 7: Optimize structure

OUTPUT:

--- MATCH SCORE ---
Give realistic %

--- SKILL GAPS ---
--- TOP 20 KEYWORDS ---
--- FULL REWRITTEN CV ---
--- LINKEDIN HEADLINE ---
--- LINKEDIN ABOUT ---
--- COVER LETTER ---

CV:
{cv}

JOB DESCRIPTION:
{jd}
"""

            else:

                score = 75

                prompt = f"""
You are a TOP recruiter.

Provide:
- ATS CV
- LinkedIn
- Cover letter

CV:
{cv}
"""

            res = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )

            first_output = res.choices[0].message.content

            # =========================
            # 🤖 AI REVIEW PASS
            # =========================
            review_prompt = f"""
You are a senior recruiter reviewing a CV.

Improve this output:
- Fix weak bullet points
- Add impact
- Improve clarity
- Ensure strong tone

CONTENT:
{first_output}
"""

            review_res = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": review_prompt}]
            )

            final_output = review_res.choices[0].message.content

            # ==============================
            # SCORE DISPLAY
            # ==============================
            st.markdown("## 📊 Match Score")
            st.markdown("**Most hired candidates score 80%+**")

            st.progress(score / 100)
            st.write(f"### {score}% Match")

            if score < 60:
                st.error("❌ Low match — major improvements needed")
            elif score < 80:
                st.warning("⚠️ متوسط match — optimize more")
            else:
                st.success("🔥 Strong match — recruiter ready")

            # ==============================
            # OUTPUT
            # ==============================
            st.subheader("💎 Premium Results")
            st.write(final_output)

            # ==============================
            # DOWNLOAD DOCX
            # ==============================
            docx_file = generate_docx(final_output)

            st.download_button(
                label="📥 Download CV (DOCX)",
                data=docx_file,
                file_name="Optimized_CV.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )

    else:
        st.info("Enter CV + email")

# ==============================
# YOUR ORIGINAL UI (UNCHANGED)
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

import streamlit as st
from openai import OpenAI
import smtplib
from email.mime.text import MIMEText

# ==============================
# 🎨 CUSTOM DARK UI
# ==============================
st.set_page_config(page_title="AI CV + LinkedIn Optimizer", page_icon="🚀", layout="centered")

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0a192f, #020c1b);
    color: white;
}
h1, h2, h3, h4 {
    color: #ffffff;
}
.stTextInput > div > div > input, 
.stTextArea textarea {
    background-color: #112240;
    color: white;
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
# 🔐 LOAD API KEY
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
# 🎯 HEADER
# ==============================
st.title("🚀 AI CV + LinkedIn Optimizer")
st.write("🔥 Stand out. Get hired faster. Beat 95% of applicants.")

st.markdown("---")

# ==============================
# 💳 PAYMENT OPTIONS
# ==============================
st.markdown("## 💳 Choose Your Package")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 💼 Basic (Free)")
    st.write("""
✔ ATS Optimized CV  
✔ Improved bullet points  
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

⏳ Limited-time access
""")
    st.link_button("Upgrade Now 🚀", "https://selar.co/m001q0082z")

st.markdown("---")

# ==============================
# 🔍 CHECK PLAN
# ==============================
query_params = st.query_params
plan = query_params.get("plan")

# ==============================
# 📥 USER INPUT
# ==============================
cv = st.text_area("📄 Paste your CV here")
email = st.text_input("📧 Enter your email")

# ==============================
# 🚀 MAIN LOGIC
# ==============================
if plan in ["basic", "premium"]:

    if plan == "basic":
        st.success("✅ Basic Plan Activated")

        # 🔥 UPSELL
        st.warning("🚀 Upgrade to Premium to unlock LinkedIn optimization + recruiter rewrite")
        st.link_button("Upgrade to Premium", "https://selar.co/m001q0082z")

    elif plan == "premium":
        st.success("💎 Premium Activated — Full Access")

    if cv and email:

        if st.button("🚀 Generate My CV"):

            with st.spinner("⚡ Optimizing..."):

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
You are an expert recruiter.

1. Rewrite this CV to be highly competitive.
2. Make it results-driven with strong metrics - quantified, and impactful.
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

                st.success("🎉 Done! Your CV is ready")

                st.download_button("📥 Download", result, file_name="optimized_cv.txt")

                if send_email(email, result):
                    st.success("📩 Sent to your email!")
                else:
                    st.warning("⚠️ Email failed")

    else:
        st.info("Enter CV + email to proceed")

else:
    st.error("❌ Please complete payment to unlock access")

# ==============================
# 🔥 FOOTER (TRUST BOOST)
# ==============================
st.markdown("---")
st.caption("Trusted by job seekers | Built with AI 🚀")

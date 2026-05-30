import streamlit as st
from openai import OpenAI
import smtplib
from email.mime.text import MIMEText

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
# 🎨 UI
# ==============================
st.set_page_config(page_title="AI CV + LinkedIn Optimizer", page_icon="🚀")

st.title("🚀 AI CV + LinkedIn Optimizer")
st.write("Get a recruiter-level CV + LinkedIn makeover that gets you hired X10 faster.")

st.markdown("---")

# ==============================
# 💳 PAYMENT OPTIONS
# ==============================
st.markdown("## 💳 Choose Your Package")

col1, col2 = st.columns(2)

with col1:
    st.subheader("💼 Basic - ₦0 (FREE)")
    st.write("""
✔ ATS Optimized CV  
✔ Improved bullet points  
✔ Cleaner formatting  
""")
    st.link_button("Pay for Basic", "https://selar.co/11180kb0j4")

with col2:
    st.subheader("💎 Premium - ₦0 (LIMITED Offer)")
    st.write("""
🔥 EVERYTHING in Basic PLUS:

✔ LinkedIn Headline  
✔ LinkedIn About Section  
✔ Skills & Keyword Optimization  
✔ Recruiter-Level Rewrite  
✔ Strong Achievement Metrics  
✔ Job-winning positioning  
""")
    st.link_button("Go Premium 🚀", "https://selar.co/m001q0082z")

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
        st.warning("🚀 Want 10x better results? Upgrade to Premium for LinkedIn + recruiter-level rewrite!")
        st.link_button("Upgrade to Premium", "https://https://selar.co/m001q0082z")

    elif plan == "premium":
        st.success("💎 Premium Plan Activated — Full Access Unlocked!")

    if cv and email:

        if st.button("🚀 Generate My Optimized CV"):

            with st.spinner("Optimizing your CV..."):

                # ==============================
                # 🤖 DIFFERENT AI PROMPTS
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

                else:  # PREMIUM
                    prompt = f"""
You are an expert recruiter and career strategist.

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
7. Job tailored CV
8. Cover Letter

CV:
{cv}
"""

                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}]
                )

                result = response.choices[0].message.content

                st.success("🎉 Your CV is ready!")

                # DOWNLOAD
                st.download_button(
                    "📥 Download Result",
                    result,
                    file_name="optimized_cv.txt"
                )

                # EMAIL
                if send_email(email, result):
                    st.success("📩 Sent to your email!")
                else:
                    st.warning("⚠️ Email failed")

    else:
        st.info("Fill your CV + email to proceed")

else:
    st.error("❌ Please complete payment to unlock access")

import streamlit as st
from openai import OpenAI
import smtplib
from email.mime.text import MIMEText

# ==============================
# 🔐 LOAD API KEY (SAFE)
# ==============================
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ==============================
# 📩 EMAIL FUNCTION
# ==============================
def send_email(to_email, content):
    try:
        msg = MIMEText(content)
        msg['Subject'] = "Your Optimized CV + LinkedIn 🚀"
        msg['From'] = st.secrets["EMAIL_ADDRESS"]
        msg['To'] = to_email

        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(st.secrets["EMAIL_ADDRESS"], st.secrets["EMAIL_PASSWORD"])
        server.send_message(msg)
        server.quit()

        return True
    except Exception as e:
        return False

# ==============================
# 🎨 UI DESIGN
# ==============================
st.set_page_config(page_title="AI CV Optimizer", page_icon="🚀")

st.title("🚀 AI CV + LinkedIn Optimizer")
st.write("Upgrade your CV to a professional, ATS-optimized version + LinkedIn Professional Profile Summary")

st.markdown("---")

# ==============================
# 💳 PAYMENT SECTION (MANUAL)
# ==============================
st.markdown("## 💳 Payment Required")

st.info("""
Pay a token of ₦1,000 to continue:

Bank: Opay  
Name: Akpojotor Oghenechovwe  
Account Number: 8035341982  

After payment, click **I HAVE PAID**
""")

# ==============================
# 📥 USER INPUT
# ==============================
cv = st.text_area("📄 Paste your CV here")
email = st.text_input("📧 Enter your email")

# ==============================
# 🚀 PROCESS BUTTON
# ==============================
if st.button("✅ I HAVE PAID"):

    if not cv or not email:
        st.warning("⚠️ Please fill all fields")
    
    else:
        st.info("🔍 Verifying payment... Please wait")

        # 👉 FOR NOW: manual trust system
        # Later we replace with Paystack verification

        with st.spinner("🤖 Optimizing your CV..."):

            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {
                            "role": "user",
                            "content": f"""
You are an expert recruiter and career strategist.

1. Optimize this CV for ATS systems and recruiter visibility.
2. Rewrite it to be results-driven, quantified, and impactful.
3. Suggest improvements for structure and keywords.
4. Create a strong LinkedIn profile including:
   - Headline
   - About section
   - Key skills
   - Experience bullet improvements

CV:
{cv}
"""
                        }
                    ]
                )

                result = response.choices[0].message.content

                st.success("✅ Done! Your CV is ready")
                
                st.markdown("## 💳 Get Full CV + LinkedIn Optimization")
st.markdown("[Pay ₦5,000 here](https://paystack.com/pay/YOUR-LINK)")


                # ==============================
                # 📥 DOWNLOAD
                # ==============================
                st.download_button(
                    label="📥 Download Result",
                    data=result,
                    file_name="optimized_cv.txt"
                )

                # ==============================
                # 📩 SEND EMAIL
                # ==============================
                if send_email(email, result):
                    st.success("📩 Sent to your email!")
                else:
                    st.warning("⚠️ Could not send email")

            except Exception as e:
                st.error(f"❌ Error: {e}")

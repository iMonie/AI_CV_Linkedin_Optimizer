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
h1, h2, h3 {
    font-weight: 700;
}
.premium-card {
    background: white;
    padding: 20px;
    border-radius: 15px;
    border: 2px solid #2563eb;
    box-shadow: 0 0 25px rgba(37, 99, 235, 0.4);
}
.basic-card {
    background: white;
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #ddd;
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
# 🔗 REFERRAL SYSTEM
# ==============================
query_params = st.query_params
plan = query_params.get("plan", "basic")
ref = query_params.get("ref")

if "ref_count" not in st.session_state:
    st.session_state.ref_count = 0

if ref:
    st.session_state.ref_count += 1

user_id = str(random.randint(10000, 99999))
ref_link = f"https://yourapp.streamlit.app/?ref={user_id}"

# ==============================
# 🔥 LIVE USERS + COUNTDOWN
# ==============================
st.markdown(f"🔥 **{random.randint(15,50)} people are using this right now**")

# ==============================
# ⏳ REAL DYNAMIC COUNTDOWN
# ==============================
if "end_time" not in st.session_state:
    st.session_state.end_time = datetime.now() + timedelta(minutes=15)

remaining = st.session_state.end_time - datetime.now()

if remaining.total_seconds() > 0:
    minutes = int(remaining.total_seconds() // 60)
    seconds = int(remaining.total_seconds() % 60)

    st.warning(f"⏳ Offer expires in {minutes}:{seconds:02d}")

    # Auto-refresh every second
    time.sleep(1)
    st.rerun()

else:
    st.error("❌ Offer expired! Price returned to ₦10,000")

# ==============================
# 🎯 HEADER
# ==============================
st.title("🚀 AI CV + LinkedIn Optimizer")
st.write("🔥 Beat 99% of applicants. Get PREMIUM. Get hired X10 faster.")

st.markdown("---")

# ==============================
# 💬 TESTIMONIALS
# ==============================
col1, col2, col3 = st.columns(3)

with col1:
    st.success("⭐️⭐️⭐️⭐️⭐️\n'I got 3 interviews in 1 week!'")

with col2:
    st.success("⭐️⭐️⭐️⭐️⭐️\n'Recruiters started replying instantly'")

with col3:
    st.success("⭐️⭐️⭐️⭐️⭐️\n'My CV finally looks professional!'")

st.markdown("---")

# ==============================
# 💳 PAYMENT
# ==============================
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="basic-card">', unsafe_allow_html=True)
    st.markdown("### 💼 Basic (Free)")
    st.write("✔ ATS CV\n✔ Bullet Improvements\n✔ Clean Format")
    st.link_button("Start Free", "https://selar.co/11180kb0j4?plan=basic")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    st.markdown("### 💎 Premium")
    st.markdown("~~₦10,000~~ **₦1,000 Today**")
    st.write("✔ LinkedIn Optimization\n✔ Achievements\n✔ Cover Letter\n✔ Recruiter Rewrite")
    st.link_button("Upgrade Now 🚀", "https://selar.co/m001q0082z?plan=premium")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# ==============================
# 📥 INPUT
# ==============================
cv = st.text_area("📄 Paste your CV", height=200)
email = st.text_input("📧 Enter your email")

# ==============================
# 🚀 GENERATION
# ==============================
if plan in ["basic", "premium"]:

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
            # 🔥 YOUR ORIGINAL PROMPT (UNCHANGED)
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
            else:
                prompt = f"""
You are an expert recruiter and strategist.

1. Rewrite this CV to be highly competitive.
2. Rewrite it to be results-driven with strong metrics - quantified, and impactful.
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

            st.success("🎉 CV Ready!")
            st.download_button("📥 Download", result)

            if send_email(email, result):
                st.success("📩 Sent to your email!")

            # ==============================
            # 🚀 VIRAL HOOK
            # ==============================
            st.markdown("---")
            st.markdown("## 🚀 Want Recruiters to FIND You?")
            st.info("Top candidates don’t just apply… they show up DAILY.")

            st.link_button("Start Growing on Linkedin", "https://socials.scaleplant.com/en/?c=AKPOJOTOWY46")

            # ==============================
            # 📲 WHATSAPP FUNNEL
            # ==============================
            st.markdown("## 💬 Get Personalized Help")

            msg = urllib.parse.quote(
                "Hi, I used your AI CV tool. I want help getting hired fast."
            )

            st.link_button(
                "Chat on WhatsApp",
                f"https://wa.me/2348035341982?text={msg}"
            )

            # ==============================
            # 💰 ₦5K OFFER
            # ==============================
            st.markdown("## 💎 Want GUARANTEED Results?")
            st.warning("₦5,000 Career Acceleration Package")

            premium_msg = urllib.parse.quote(
                "I want the ₦5,000 career acceleration package"
            )

            st.link_button(
                "Secure Your Spot",
                f"https://wa.me/2348035341982?text={premium_msg}"
            )

            # ==============================
            # 🧲 REFERRAL SYSTEM
            # ==============================
            st.markdown("---")
            st.markdown("## 🎁 Earn Rewards")

            st.success(f"""
Your referral link:
{ref_Link}

Referrals: {st.session_state.ref_count}
""")

            st.info("""
🎁 10 referrals = FREE Premium CV upgrade  
🎁 20 referrals = Done for You & 1-on-1 session
""")

    else:
        st.info("Enter CV + email")

else:
    st.error("❌ Complete payment to unlock")

# ==============================
# FOOTER
# ==============================
st.markdown("---")
st.caption("🚀 Built for income & impact by Oghenechovwe AKPOJOTOR")

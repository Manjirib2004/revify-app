# revify_full_app.py
import streamlit as st
import pandas as pd

# ---------------- App Configuration ----------------
st.set_page_config(page_title="Revify - Mobile Review Sentiment", layout="wide")
st.title("📱 Revify – Mobile Review Sentiment Analyzer")
st.write("Analyze customer emotions from mobile product reviews using AI and NLP.")

# ---------------- Helper Function ----------------
def predict_sentiment(review):
    review = str(review).lower()
    positive = ['good', 'great', 'awesome', 'nice', 'love', 'best', 'fast', 'excellent', 'smooth']
    negative = ['bad', 'worst', 'slow', 'hate', 'problem', 'poor', 'battery', 'lag', 'heating']
    pos = sum(word in review for word in positive)
    neg = sum(word in review for word in negative)
    if pos > neg:
        return "Positive 😀"
    elif neg > pos:
        return "Negative 😞"
    else:
        return "Neutral 😐"

# ---------------- Mobile Selection ----------------
st.subheader("🔹 Select or Enter Mobile Product")
mobile_list = [
    "Samsung Galaxy S24",
    "iPhone 15 Pro",
    "OnePlus 12",
    "Xiaomi 14 Ultra",
    "Realme GT 6",
    "Vivo V30 Pro",
    "Oppo Reno 12",
    "Motorola Edge 50",
    "Nothing Phone 2a",
    "Google Pixel 8"
]

selected_mobile = st.selectbox("Choose a mobile:", ["-- Select Mobile --"] + mobile_list)
custom_mobile = st.text_input("Or type your mobile name manually:")
mobile_name = custom_mobile.strip() if custom_mobile.strip() else selected_mobile
if mobile_name and mobile_name != "-- Select Mobile --":
    st.info(f"📱 Selected Mobile: **{mobile_name}**")

# ---------------- Single Review Prediction ----------------
st.subheader("📝 Single Review Prediction")
user_review = st.text_area("Enter a mobile review:", placeholder="Type your review here...")

if st.button("Analyze Sentiment"):
    if not mobile_name or mobile_name == "-- Select Mobile --":
        st.warning("Please select or enter a mobile name first.")
    elif not user_review.strip():
        st.warning("Please enter a review before analysis.")
    else:
        result = predict_sentiment(user_review)
        st.success(f"**Mobile:** {mobile_name}\n\n**Predicted Sentiment:** {result}")

# ---------------- Batch Review Analysis ----------------
st.markdown("---")
st.subheader("📂 Batch Review Analysis (CSV Upload)")
uploaded_file = st.file_uploader("Upload a CSV file with columns: 'mobile', 'review'", type=['csv'])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        # Auto-clean column names
        df.columns = df.columns.str.strip().str.lower()
        if 'mobile' not in df.columns or 'review' not in df.columns:
            st.error("❌ CSV must contain columns named 'mobile' and 'review'.")
        else:
            # Apply sentiment prediction
            df['Predicted_Sentiment'] = df['review'].apply(predict_sentiment)
            st.success("✅ Batch sentiment analysis completed!")
            st.subheader("Sample Data")
            st.dataframe(df.head(20))
            # Download results
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("⬇️ Download Results", data=csv, file_name="sentiment_results.csv", mime="text/csv")
    except Exception as e:
        st.error(f"Error reading CSV: {e}")

st.markdown("---")
st.caption("Developed with ❤️ using Streamlit | Revify © 2025")

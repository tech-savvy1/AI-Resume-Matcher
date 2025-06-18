import streamlit as st
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer, util

# Load the embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# App layout
st.set_page_config(page_title="AI Resume Matcher", layout="centered")
st.title("🤖 AI Resume Matcher")
st.markdown("Upload your resume (PDF) and paste the job description. Get your match score instantly!")

# Upload resume
pdf_file = st.file_uploader("📄 Upload your Resume (PDF only)", type=["pdf"])

# Job description input
job_description = st.text_area("📝 Paste the Job Description Here", height=200)

# Match Button
if st.button("🚀 Match Resume"):
    if pdf_file is not None and job_description.strip():
        # Extract resume text
        pdf_reader = PdfReader(pdf_file)
        resume_text = ""
        for page in pdf_reader.pages:
            resume_text += page.extract_text()

        # Encode both texts
        resume_embedding = model.encode(resume_text, convert_to_tensor=True)
        jd_embedding = model.encode(job_description, convert_to_tensor=True)

        # Calculate similarity
        similarity = util.cos_sim(resume_embedding, jd_embedding).item()
        score = round(similarity * 100, 2)

        # Verdict
        if score >= 75:
            verdict = "🟢 Great Match!"
        elif score >= 50:
            verdict = "🟡 Decent Match. Consider tailoring your resume more."
        else:
            verdict = "🔴 Poor Match. Resume needs improvement."

        # Display results
        st.markdown(f"### ✅ Match Score: `{score}%`")
        st.markdown(f"**Verdict:** {verdict}")
    else:
        st.warning("Please upload a resume and paste a job description.")

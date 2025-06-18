import streamlit as st
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')  # small, fast LLM for embeddings

st.title("AI Resume Screener")

resume_file = st.file_uploader("Upload Resume (PDF)", type="pdf")
job_description = st.text_area("Paste Job Description")

if resume_file and job_description:
    reader = PdfReader(resume_file)
    resume_text = "\n".join([page.extract_text() for page in reader.pages])

    # Convert to vector embeddings
    resume_embedding = model.encode(resume_text, convert_to_tensor=True)
    jd_embedding = model.encode(job_description, convert_to_tensor=True)

    # Similarity score
    similarity = util.cos_sim(resume_embedding, jd_embedding).item()
    match_percent = round(similarity * 100, 2)
    st.success(f"Match Score: {match_percent}%")
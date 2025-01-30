import streamlit as st
import subprocess
subprocess.run(["pip", "install", "google-generativeai"])
import google.generativeai as genai
import pdfplumber
import textwrap

# Configure Gemini API
genai.configure(api_key="Your-google-gemini-api-key")

# Function to summarize text with better accuracy
def summarize_text(text, summary_type="detailed"):
    model = genai.GenerativeModel("gemini-pro")

    # Define prompt based on summary type
    if summary_type == "short":
        prompt = f"Summarize this in 2-3 sentences, keeping it very concise:\n\n{text}"
    elif summary_type == "bullet":
        prompt = f"Summarize this into bullet points, keeping all important details:\n\n{text}"
    else:
        prompt = f"Summarize this in a detailed yet clear way, preserving key points:\n\n{text}"

    response = model.generate_content(prompt)
    return response.text

# Function to split long text into smaller chunks (if needed)
def split_text(text, max_length=4000):
    return textwrap.wrap(text, max_length, break_long_words=False, replace_whitespace=False)

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    with pdfplumber.open(pdf_file) as pdf:
        text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
    return text if text.strip() else None  # Return None if empty

# ---- Streamlit UI ----
st.set_page_config(page_title="Summarizer AI ", page_icon="📝", layout="centered")

# Title
st.title("📄 Summarizer AI")
st.write("🔹 Upload a PDF or enter text to generate a summary using Summarizer AI.")

# Summary Type Selection
summary_type = st.radio("Choose summary style:", ["Detailed", "Short", "Bullet Points"], horizontal=True)

# Text Input
user_input = st.text_area("✍️ Enter text to summarize:", "", height=150)

if st.button("Summarize Text ✨"):
    if user_input:
        with st.spinner("Summarizing... ⏳"):
            if len(user_input) > 4000:
                text_chunks = split_text(user_input)
                summary = "\n\n".join([summarize_text(chunk, summary_type.lower()) for chunk in text_chunks])
            else:
                summary = summarize_text(user_input, summary_type.lower())

        st.subheader("📌 Summary:")
        st.write(summary)
    else:
        st.warning("Please enter some text!")

# PDF Upload
st.divider()
st.subheader("📂 Upload a PDF to Summarize")
uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

pdf_text = None  # Initialize

if uploaded_file:
    with st.spinner("Extracting text from PDF... ⏳"):
        pdf_text = extract_text_from_pdf(uploaded_file)

    if pdf_text:
        with st.expander("📜 Extracted Text Preview (click to expand)"):
            st.write(pdf_text[:2000] + "...")  # Show only a preview

    else:
        st.error("❌ Could not extract text from the PDF. It may be scanned or empty.")

    # Summarization Button (Only if text extraction succeeded)
    if pdf_text and st.button("Summarize PDF 📑"):
        with st.spinner("Summarizing PDF content... ⏳"):
            if len(pdf_text) > 4000:
                text_chunks = split_text(pdf_text)
                pdf_summary = "\n\n".join([summarize_text(chunk, summary_type.lower()) for chunk in text_chunks])
            else:
                pdf_summary = summarize_text(pdf_text, summary_type.lower())

        st.subheader("📌 PDF Summary:")
        st.write(pdf_summary)

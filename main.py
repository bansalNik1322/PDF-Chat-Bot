from langchain.text_splitter import CharacterTextSplitter
from fpdf import FPDF
from chromadb import Documents, EmbeddingFunction, Embeddings
import chromadb
from PyPDF2 import PdfReader

# To create the User Interface
import streamlit as st
# for PDF text extraction
import PyPDF2  
import pathlib
import textwrap
import google.generativeai as genai
from IPython.display import display
from IPython.display import Markdown


from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))


import os
os.environ['GOOGLE_API_KEY'] = "AIzaSyDTbvUJYckOPIcXgEkVBg0eM4bZ2x4x-XU"
# Creating Gemini Pro Model

genai.configure(api_key=os.environ['GOOGLE_API_KEY'])

model = genai.GenerativeModel('gemini-pro')


def getPdfText(pdf):
    text = ""
    pdfreader = PdfReader(pdf)
    for page in pdfreader.pages:
        text += page.extract_text()
    return text 


def createTextChunks(text):
    textSplliter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = textSplliter.split_text(text)
    return chunks



class GeminiEmbeddingFunction(EmbeddingFunction):
  def __call__(self, input) -> Embeddings:
    model = 'models/embedding-001'
    # `title` is an optional field and omitted here.    
    return genai.embed_content(model=model, content=input, task_type="retrieval_document")["embedding"]
  

def createChromDB(documents, name):
  chromaClient = chromadb.Client()
  db = chromaClient.create_collection(name=name, embedding_function=GeminiEmbeddingFunction(documents))

  for i, d in enumerate(documents):
    db.add(
      documents=d,
      ids=str(i)
    )
  return db




# Set page title and layout
st.set_page_config(page_title="AI Test Generation Bot (Upload Page)", layout="wide")

st.title("Upload Your PDF File")  # Singular "File"

# Upload section with progress bar and clear instructions
uploaded_file = st.file_uploader("Drag and drop your PDF file here, or click to browse.", type="pdf", accept_multiple_files=False)  # Changed to accept_multiple_files=False
if uploaded_file:
    try:
        progress_bar = st.progress(0)
        st.write(f"File uploaded: {uploaded_file.name}")

        try:
            with open(uploaded_file.name, "rb") as pdfFile:
        
            # Getting the text from pdf
                rawPdfText = getPdfText(pdfFile)

                # Creating text chunks
                textChunks = createTextChunks(rawPdfText)
                
                # Creating google embedding and vector store
                # chromaDB = createChromDB(textChunks, "pdfDatabase")

            st.success("Text extraction successful!")

            try:
                question_type = st.selectbox("Select question type:", options=["Short Answer", "Long Answer"])
                difficulty = st.selectbox("Select difficulty:", options=["Easy", "Medium", "Hard"])

                if st.button("Generate Question List"):
                    try:
                        questionsList = model.generate_content(f"Create a list of 10 to 30 {question_type} type {difficulty} level questions with their ans  from the given text : {rawPdfText}", stream=True)
                        text_string = "".join(chunk.text for chunk in questionsList)

                        pdf = FPDF()
                        pdf.add_page()
                        pdf.set_font("Arial", size=12)
                        pdf.multi_cell(0, 5, txt=text_string)
                        pdf_output = pdf.output(dest="S").encode("latin-1")

                        st.write("Generating question list...")
                        st.download_button(
                            label="Download Question List PDF",
                            data=pdf_output,
                            file_name="question_list.pdf",
                            mime="application/pdf",
                        )
                        st.write("Question list generated successfully!")
                    except Exception as e:
                        st.error(f"Error during question generation or PDF creation: {e}")
            except Exception as e:
                st.error(f"Error during user input or button click: {e}")
        except Exception as e:
            st.error(f"Error during PDF reading or text extraction: {e}")
    except Exception as e:
        st.error(f"General error: {e}")





        
# PDF-Chat-Bot
This project introduces an innovative AI-powered bot that streamlines test development by automatically generating questions from provided PDF materials. 

https://github.com/bansalNik1322/PDF-Chat-Bot/assets/103099655/59f66946-e985-4591-bebd-bbb3059ca041


Here's a comprehensive documentation of the code, including key functionalities and steps:

1. Imports:
  Text processing: langchain.text_splitter, PyPDF2
  PDF creation: fpdf, reportlab
  Embedding database: chromadb
  UI framework: streamlit
  Google AI model: google.generativeai

2. Functions:
  getPdfText(pdf): Extracts text from a PDF file.
  createTextChunks(text): Splits text into smaller chunks for embedding.
  GeminiEmbeddingFunction: Class for generating embeddings using Google's embedding model.
  createChromDB(documents, name): Creates a ChromaDB collection with embeddings. (Not currently used)

3. User Interface:
  Page title and layout: Sets title and wide layout.
  File uploader: Allows user to upload a single PDF file.
  Progress bar: Displays progress during PDF processing.
  Question type selector: User chooses question type (short or long answer).
  Difficulty level selector: User selects question difficulty (easy, medium, hard).
  Generate Question List button: Triggers question generation and download.

4. Main Logic:
  File upload:
  Reads uploaded PDF file.
  Extracts text using getPdfText.
  Creates text chunks using createTextChunks.
  (Commented out) Creates ChromaDB collection with embeddings.
  Shows success message upon text extraction.
  Question generation:
  Prompts the Gemini model to generate questions based on user-specified type and difficulty.
  Creates a PDF file containing generated questions.
  Offers a download button for the question list PDF.

5. Error Handling:
  Incorporates try-except blocks to handle potential errors during:
  PDF reading/text extraction
  User input/button click
  Question generation/PDF creation
  General errors
Key Points:

  Uses Streamlit for a web-based UI.
  Extracts text from PDFs using PyPDF2.
  Splits text into chunks for embedding (but doesn't currently use them).
  Leverages Google AI's Gemini model for question generation.
  Generates a PDF document containing the generated questions.
  Provides informative error messages for a user-friendly experience.



  

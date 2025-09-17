# Financial Document Q&A Assistant
## 🎯Overview
This web application allows users to upload financial documents (PDF or Excel) and ask questions in plain English about revenue, expenses, profits, and other financial metrics. The app extracts text and numerical data from the uploaded documents and provides accurate, interactive answers.

## 📝 Features
- Upload multiple PDF or Excel financial statements.
- Supports Income Statements, Balance Sheets, and Cash Flow Statements.
- Extracts key metrics like revenue, expenses, and profit.
- Ask natural language questions and get instant answers.
- Conversational interface supports follow-up questions.
- Reset session to upload new files and start fresh.
- Error handling for invalid files or processing failures.

## ⚙️ Technical Implementation
- Built using Streamlit for the web interface.
- Uses Ollama local Small Language Models (SLMs) for NLP and question answering.
- Handles multiple file formats and various layouts.
- Implements session management to avoid reprocessing files unnecessarily.
- Provides feedback and status updates during file processing.

## Installation & Running Locally
1. Clone the repository:
```
git clone https://github.com/vamshigoud1108/finance_qa_assistant.git
cd finance_qa_assistant
```
2. Create and activate a virtual environment:
```
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```
3. Install dependencies:
```
pip install -r requirements.txt
```
4. Run the Streamlit app:
```
streamlit run app.py
```
5. Open the app in your browser at ```http://localhost:8501```

## 🗂️ Usage
1. Upload one or multiple **financial documents** in the sidebar.

2. Click **"Process Files"** to extract data and create the vector store.

3. Ask questions in the chat input at the bottom.

4. Click **"Reset Session"** to remove uploaded files and start fresh.

## ▶️ Demo
![project-demo](project-demo.gif)

## 📂 File Structure
```
Financial-QA-Assistant/
│
├─ app.py              # Main Streamlit app
├─ file_handler.py          # File extraction logic (PDF/Excel)
├─ llm_pipeline.py         # Data split, vector store, QA chain
├─ config.py           # Model and API configuration
├─ requirements.txt    # Python dependencies
└─ README.md           # Project description
```
## ✅ Success Criteria
- Users can upload financial documents successfully.
- Key metrics are extracted correctly.
- The app provides accurate answers to questions about uploaded files.
- Users can interact with the system conversationally.

## ⚠️ Notes
- Ensure Ollama SLM is installed and running for NLP queries.

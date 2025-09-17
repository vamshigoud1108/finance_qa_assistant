import streamlit as st

from file_handler import extract_text_from_file
from llm_pipeline import split_data
from llm_pipeline import build_vectorstore
from llm_pipeline import build_qa_chain

# Initialize session state
if 'qa_chain' not in st.session_state:
   st.session_state.qa_chain = None
if "vector_store" not in st.session_state:
   st.session_state.vector_store = None
if "uploaded_files" not in st.session_state:
   st.session_state.uploaded_files = []
if 'uploader_key' not in st.session_state:
   st.session_state.uploader_key = 0

st.title("📊 Finance Q&A Assistant")

if st.session_state.qa_chain is None:
  st.markdown("""
  Upload your **financial documents** (PDF or Excel).  
  - Supports: Income Statements, Balance Sheets, Cash Flow Statements  
  - Extracts key metrics like revenue, expenses, and profit  
  - Ask questions in plain English and get instant answers  
  """)

with st.sidebar:

  # Reset button
  if st.sidebar.button("🔄 Reset Session"):
     try:
        if st.session_state.vector_store:
           st.session_state.vector_store.delete(delete_all=True)
        st.session_state.qa_chain = None
        st.session_state.vector_store = None
        st.session_state.uploaded_files = []
        st.session_state.uploader_key += 1
        st.success("Session reset. Upload new files to start fresh")
        st.rerun()
     
     except Exception as e:
        st.error(f"Failed to reset: {e}")
  
  # Upload Section
  st.header("Upload Section")
  uploaded_files = st.file_uploader(
    "Uploaded Files",
    type=['pdf', 'xlsx','xls'],
    accept_multiple_files=True,
    key=st.session_state.uploader_key
  )
  process_button = st.button("⚡ Process Files")
  if process_button:
    if uploaded_files:
        with st.spinner('Processing files...'):
           
          file_text = ""
          for upload_file in uploaded_files:
            file_text += extract_text_from_file(upload_file)

          # Split documents, build vector store, QA chain
          splitted_docs = split_data(file_text)
          vector_store = build_vectorstore(splitted_docs)
          qa_chain = build_qa_chain(vector_store) 

          # Saving to session state
          st.session_state.qa_chain = qa_chain
          st.session_state.vector_store = vector_store
          st.session_state.uploaded_files = uploaded_files

        st.success("✅ Files uploaded and processed! You can now ask questions.")
      
    else:
      st.warning("Please upload at least one file before processing.")


# Chat Input
user_question = st.chat_input('Ask a question based on the uploaded files')
if user_question:
        if st.session_state.qa_chain is not None:
          with st.spinner("Fetching answer... ⏳"):
              try:
                 
                response = st.session_state.qa_chain({"question": user_question})
                st.write("**Answer:**", response['answer'])
              
              except Exception as e:
                 st.error(f"Failed to fetch answer: {e}")
        
        else:
           st.warning("⚠️ Please upload and process files before asking questions.")
else:
    if st.session_state.qa_chain is None and not st.session_state.get("uploaded_files"):
        st.info("Upload and process a financial file in the sidebar to start asking questions.")
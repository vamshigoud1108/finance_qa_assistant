from PyPDF2 import PdfReader
import pandas as pd
import streamlit as st

def extract_text_from_file(uploaded_file):
  try:

    file_text = ""

    # Handling PDF file
    if uploaded_file.type == "application/pdf":
      reader = PdfReader(uploaded_file)
      for page in reader.pages:
        file_text += page.extract_text() or "" 
    
    else: 
      # Handling Excel file
      file_extension = uploaded_file.name.split('.')[-1].lower()
      if file_extension in ['xlsx','xlsm']:
        df = pd.read_excel(uploaded_file, engine="openpyxl")

      elif file_extension == "xls":
        df = pd.read_excel(uploaded_file, engine="xlrd")
      
      else:
          raise ValueError(f"Unsupported Excel file format: {file_extension}")
      
      file_text = df.to_string()
    
    return file_text.strip()

  
  except Exception as e:
    st.error(f"Failed to extract text:{e}")
    return ""
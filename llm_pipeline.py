from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from pinecone import Pinecone
from langchain_pinecone import PineconeSparseVectorStore, PineconeVectorStore
from langchain_ollama import OllamaLLM
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
import config as config
from langchain.prompts import PromptTemplate
from langchain.schema import Document
import streamlit as st


# Splitting the data into chunks
def split_data(file_text,chunk_size=800,chunk_overlap=200):
  try:
    if not file_text:
      return []
    
    docs = [Document(page_content=file_text)]
    text_splitter = RecursiveCharacterTextSplitter(
      chunk_size=chunk_size,
      chunk_overlap=chunk_overlap
    )
    return text_splitter.split_documents(docs)
  
  except Exception as e:
    st.error(f"Failed to split data: {e}")

# Building vectorstore
def build_vectorstore(splitted_docs):
  try:
    embeddings = HuggingFaceEmbeddings(model_name=config.MODEL_NAME)
    pc = Pinecone(api_key=config.PINECONE_API_KEY)

    vectorstore = PineconeVectorStore.from_documents(
      documents=splitted_docs,
      embedding=embeddings,
      index_name=config.INDEX_NAME
    )
    return vectorstore
  
  except Exception as e:
    st.error(f"Failed to build vector store: {e}")
    return None


# Build QA Chain
def build_qa_chain(vectorstore):

  try:

    # Initializig LLM
    llm = OllamaLLM(model='smollm',temperature=0.4)

    # Retriever
    retriever = vectorstore.as_retriever(
      search_type = 'similarity',
      search_kwargs={'k':3}
    )

    # Memory
    memory = ConversationBufferMemory(
      memory_key="chat_history",
      return_messages=True
    )
  
    # Prompt Template
    prompt = PromptTemplate(
      template = config.PROMPT_TEMPLATE,
      input_variables=['context','question']
    )

    # qa_chain
    qa_chain = ConversationalRetrievalChain.from_llm(
      llm=llm,
      retriever=retriever,
      memory=memory,
      chain_type='stuff',
      combine_docs_chain_kwargs={'prompt':prompt}
    )
    return qa_chain
  
  except Exception as e:
    st.error(f"Failed to build Qa chain: {e}")
    return None
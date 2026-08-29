import os
import requests
import streamlit as st
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain

# --- 1. UI Configuration ---
st.set_page_config(
    page_title="PRISM | Full-Stack Academic Mentor", 
    page_icon="💠", 
    layout="wide"
)

st.title("💠 PRISM: Full-Stack AI Mentor & Notes Manager")
st.caption("FastAPI REST CRUD Backend + Streamlit AI RAG Frontend")

# FastAPI Backend URL
API_URL = "http://127.0.0.1:8000/notes/"

# --- 2. Sidebar Configuration ---
with st.sidebar:
    st.header("⚙️ Configuration")
    # Paste your real Groq API key here inside the quotes
    user_api_key = "" 
    
    st.markdown("---")
    st.header("🎯 Navigation")
    app_mode = st.radio("Choose Section:", ["AI Academic Mentor (RAG)", "Study Notes (FastAPI CRUD)"])
    
    if app_mode == "AI Academic Mentor (RAG)":
        selected_subject = st.selectbox(
            "Select Subject:",
            ["Biology (NCERT Core)"]
        )

# --- 3. Database Initialization for RAG ---
PDF_DIRECTORY = "pdfs"
DB_DIRECTORY = "chroma_storage"

@st.cache_resource(show_spinner=False)
def initialize_database():
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    if os.path.exists(DB_DIRECTORY) and os.listdir(DB_DIRECTORY):
        return Chroma(persist_directory=DB_DIRECTORY, embedding_function=embeddings)
    
    all_chunks = []
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    if os.path.exists(PDF_DIRECTORY):
        pdf_files = [f for f in os.listdir(PDF_DIRECTORY) if f.endswith('.pdf')]
        for pdf in pdf_files:
            loader = PyMuPDFLoader(os.path.join(PDF_DIRECTORY, pdf))
            all_chunks.extend(text_splitter.split_documents(loader.load()))
        if all_chunks:
            return Chroma.from_documents(all_chunks, embeddings, persist_directory=DB_DIRECTORY)
    return None

if "vector_store" not in st.session_state:
    with st.spinner("Indexing Local Corpus..."):
        st.session_state.vector_store = initialize_database()

# --- 4. App Mode 1: AI Chat Mentor ---
if app_mode == "AI Academic Mentor (RAG)":
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_input = st.chat_input("Ask a question or paste a numerical problem...")

    if user_input:
        if not st.session_state.vector_store:
            st.warning("⚠️ Corpus missing. Ensure your formula/NCERT PDFs are inside the 'pdfs/' folder.")
        else:
            st.session_state.messages.append({"role": "user", "content": user_input})
            with st.chat_message("user"):
                st.markdown(user_input)

            # Using an active, reliable Groq model
            llm = ChatGroq(groq_api_key=user_api_key, model_name="openai/gpt-oss-120b")
            
            # Cleanly formatted system prompt
            system_prompt = (
                f"You are PRISM, an elite academic mentor for NEET/JEE. "
                f"Current Subject: {selected_subject}. "
                "Use the provided context as the absolute source of truth. "
                "Context: {context}"
            )
            
            prompt = ChatPromptTemplate.from_messages([("system", system_prompt), ("human", "{input}")])
            retriever = st.session_state.vector_store.as_retriever(search_kwargs={"k": 4})
            rag_chain = create_retrieval_chain(retriever, create_stuff_documents_chain(llm, prompt))

            with st.chat_message("assistant"):
                with st.spinner("Analyzing corpus..."):
                    response = rag_chain.invoke({"input": user_input})
                    answer = response["answer"]
                    st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})

# --- 5. App Mode 2: FastAPI CRUD Notes Manager ---
elif app_mode == "Study Notes (FastAPI CRUD)":
    st.subheader("📝 Student Notes Manager (Powered by FastAPI REST API)")
    
    # Fetch existing notes via GET request
    try:
        response = requests.get(API_URL)
        notes = response.json() if response.status_code == 200 else []
    except Exception:
        notes = []
        st.error("⚠️ Could not connect to FastAPI backend. Ensure your backend server is running (`python -m uvicorn backend:app --reload`)!")

    # CREATE Note Form (POST)
    with st.form("create_note_form"):
        st.write("### Create New Study Note")
        new_title = st.text_input("Title")
        new_subject = st.selectbox("Subject", ["Physics", "Chemistry", "Biology"])
        new_content = st.text_area("Content / Formula Summary")
        submit_create = st.form_submit_button("Create Note")
        
        if submit_create and new_title and new_content:
            payload = {"title": new_title, "content": new_content, "subject": new_subject}
            res = requests.post(API_URL, json=payload)
            if res.status_code == 201:
                st.success("Note created successfully!")
                st.rerun()
            else:
                st.error("Failed to create note.")

    st.markdown("---")
    st.write("### Existing Notes (Read, Update, Delete)")
    
    if not notes:
        st.info("No saved notes found. Create one above!")
    else:
        for note in notes:
            with st.expander(f"{note['subject']} - {note['title']} (ID: {note['id']})"):
                # UPDATE Form (PUT)
                with st.form(f"update_form_{note['id']}"):
                    up_title = st.text_input("Update Title", value=note['title'], key=f"title_{note['id']}")
                    up_subject = st.selectbox("Update Subject", ["Biology"], index=["Biology"].index(note['subject']), key=f"subj_{note['id']}")
                    up_content = st.text_area("Update Content", value=note['content'], key=f"cont_{note['id']}")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        submit_update = st.form_submit_button("Update Note")
                    with col2:
                        submit_delete = st.form_submit_button("Delete Note")
                    
                    if submit_update:
                        payload = {"title": up_title, "content": up_content, "subject": up_subject}
                        res = requests.put(f"{API_URL}{note['id']}", json=payload)
                        if res.status_code == 200:
                            st.success("Note updated!")
                            st.rerun()
                        else:
                            st.error("Update failed.")
                            
                    if submit_delete:
                        res = requests.delete(f"{API_URL}{note['id']}")
                        if res.status_code == 200:
                            st.success("Note deleted!")
                            st.rerun()
                        else:
                            st.error("Deletion failed.")
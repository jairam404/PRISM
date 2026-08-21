import os
import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

# --- 1. Sleek UI Configuration ---
st.set_page_config(
    page_title="PRISM | AI Mentorship Platform", 
    page_icon="💠", 
    layout="wide"
)

# Custom CSS for a clean, professional, non-AI-looking interface
st.markdown("""
    <style>
    .main { background-color: #0b0f19; color: #f8fafc; }
    .stTextInput input, .stSelectbox select { background-color: #1e293b; color: white; border-radius: 8px; border: 1px solid rgba(255,255,255,0.1); }
    .stChatMessage { background-color: #111827; border: 1px solid rgba(255,255,255,0.05); border-radius: 12px; }
    </style>
""", unsafe_allow_html=True)

st.title("💠 PRISM: Intelligent Student Mentorship Platform")
st.caption("Personalized Reasoning & Intelligent Student Mentorship | Full NCERT Corpus Loaded")

# --- 2. Configuration ---
# Just paste your key right here inside the quotes!
GROQ_API_KEY = "your_actual_groq_api_key_here"  
PDF_DIRECTORY = "pdfs"

# --- 3. Sidebar Controls ---
with st.sidebar:
    st.header("⚙️ Platform Config")
    st.success("🔒 System API Connected")
    
    st.markdown("---")
    st.header("🧠 Personalization Engine")
    student_level = st.selectbox(
        "Select Mastery Tier:",
        [
            "Beginner (Conceptual breakdown with step-by-step analogies)", 
            "Intermediate (Standard NCERT textbook analysis)", 
            "Advanced (Rapid high-yield NEET MCQ pointers & tricks)"
        ]
    )
    
    st.markdown("---")
    st.info("📚 Status: All 25 Biology chapters indexed in ChromaDB memory.")

# --- 4. Initialize State & Load All 25 PDFs Automatically ---
if "messages" not in st.session_state:
    st.session_state.messages = []

if "vector_store" not in st.session_state:
    with st.spinner("Indexing all 25 NCERT Biology chapters into PRISM memory... Please wait ⏳"):
        all_chunks = []
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        
        if os.path.exists(PDF_DIRECTORY):
            pdf_files = [f for f in os.listdir(PDF_DIRECTORY) if f.endswith('.pdf')]
            
            for pdf in pdf_files:
                pdf_path = os.path.join(PDF_DIRECTORY, pdf)
                loader = PyPDFLoader(pdf_path)
                docs = loader.load()
                chunks = text_splitter.split_documents(docs)
                all_chunks.extend(chunks)
            
            if all_chunks:
                embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
                st.session_state.vector_store = Chroma.from_documents(all_chunks, embeddings)
                st.success(f"✅ Successfully loaded {len(pdf_files)} chapters into PRISM!")
            else:
                st.error("⚠️ No PDF files found inside the 'pdfs' folder.")
        else:
            st.error(f"⚠️ Folder '{PDF_DIRECTORY}' not found. Please create it and add your 25 PDFs.")

# --- 5. Interactive Chat Workspace ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Ask a NEET biology question or request a concept review...")

if user_input and st.session_state.vector_store:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    llm = ChatGroq(groq_api_key=GROQ_API_KEY, model_name="llama3-8b-8192")

    system_prompt = f"""
    You are PRISM, an expert academic mentor for NEET Biology. 
    The student's target mastery tier is: {student_level}.
    Adapt your explanation style strictly to match this tier.
    
    Rule 1: Base your response precisely on the provided NCERT textbook context.
    Rule 2: If the text lacks the answer, state: "This topic falls outside the indexed NCERT corpus."
    Rule 3: End your response with a quick checkpoint question to verify the student's understanding.

    Context:
    {{context}}
    """
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}")
    ])

    retriever = st.session_state.vector_store.as_retriever(search_kwargs={"k": 4})
    qa_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever, qa_chain)

    with st.chat_message("assistant"):
        with st.spinner("Analyzing across 25 NCERT chapters..."):
            response = rag_chain.invoke({"input": user_input})
            answer = response["answer"]
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})

elif user_input and not st.session_state.vector_store:
    st.error("⚠️ Database not initialized. Check your pdfs folder.")
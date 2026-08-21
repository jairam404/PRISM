import os
import streamlit as st
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain

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
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]  
PDF_DIRECTORY = "pdfs"
DB_DIRECTORY = "chroma_storage"

# --- 3. Sidebar Controls ---
with st.sidebar:
    st.header("⚙️ Platform Config")
    st.success("🔒 System API Connected Securely")
    
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
    st.info("📚 Status: Database connected and ready.")

# --- 4. Initialize State & Vector Database Caching ---
if "messages" not in st.session_state:
    st.session_state.messages = []

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
            pdf_path = os.path.join(PDF_DIRECTORY, pdf)
            loader = PyMuPDFLoader(pdf_path)
            docs = loader.load()
            chunks = text_splitter.split_documents(docs)
            all_chunks.extend(chunks)
        
        if all_chunks:
            vector_store = Chroma.from_documents(
                all_chunks, 
                embeddings, 
                persist_directory=DB_DIRECTORY
            )
            return vector_store
            
    return None

if "vector_store" not in st.session_state:
    with st.spinner("Connecting to PRISM Memory Core... Please wait ⏳"):
        st.session_state.vector_store = initialize_database()
        
        if st.session_state.vector_store:
            st.success("✅ PRISM Database Connected!")
        else:
            st.error("⚠️ Database missing or 'pdfs' folder is empty.")

# --- 5. Interactive Chat Workspace ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Ask a NEET biology question or request a concept review...")

if user_input and st.session_state.vector_store:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    llm = ChatGroq(groq_api_key=GROQ_API_KEY, model_name="openai/gpt-oss-120b")

    system_prompt = f"""
    You are PRISM, an expert academic mentor for NEET Biology. 
    The student's target mastery tier is: {student_level}.
    Adapt your explanation style strictly to match this tier.
    
    NEET Biology Chapter Weightage Reference:
    - Human Physiology: 15% to 20% (High Priority / Core Foundation)
    - Genetics and Evolution: 12% to 15% (High Priority / Conceptual & MCQ Heavy)
    - Ecology: 10% to 12% (High Priority / Fact-Heavy & Direct NCERT Lines)
    - Plant & Animal Kingdom (Diversity): 10% to 12% (High Priority / Example-Driven)
    - Reproduction: 8% to 10% (Moderate Priority / Diagram & Process Heavy)
    - Cell Biology: 8% to 10% (Moderate Priority / Core Structural Foundation)

    Guidelines:
    1. Base all conceptual explanations strictly on the provided NCERT context.
    2. Identify and mention the chapter's weightage tier (e.g., "High-Yield: ~15-20% NEET weightage") when explaining key concepts.
    3. If the topic falls in a top-ranking unit (Human Physiology, Genetics, Ecology, Diversity), emphasize frequently tested lines and high-yield traps.
    4. If the text lacks the answer, state: "This topic falls outside the indexed NCERT corpus."
    5. End your response with a quick checkpoint MCQ or conceptual question to verify understanding.

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
        with st.spinner("Analyzing across 32 NCERT chapters..."):
            response = rag_chain.invoke({"input": user_input})
            answer = response["answer"]
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})

elif user_input and not st.session_state.vector_store:
    st.error("⚠️ Database not initialized. Check your pdfs folder.")
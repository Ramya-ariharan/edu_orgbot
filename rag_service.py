import os
from dotenv import load_dotenv
load_dotenv()

from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate

# --------------------------------------------------
# CONFIG
# --------------------------------------------------
DATA_PATH = "data/education.pdf"
COLLECTION_NAME = "education"
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# --------------------------------------------------
# LLM
# --------------------------------------------------
llm = ChatGroq(
    temperature=0,
    groq_api_key=GROQ_API_KEY,
    model_name="llama-3.1-8b-instant",
)

# --------------------------------------------------
# EMBEDDINGS
# --------------------------------------------------
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# --------------------------------------------------
# PROMPT
# --------------------------------------------------
system_prompt = (
    "You are a helpful academic counselor for our education institute. "
    "Use the retrieved context to answer student questions clearly. "
    "Keep replies in MAX three sentences and be friendly and confident. "
    "If you don’t know the answer, politely ask them to contact our admin at 9874563210. "
    "If the student asks about customized courses or combinations, confirm availability and guide them to admin. "
    "If asked about job scope or demand, give realistic trends or percentages. "
    "Be supportive and motivating.\n\n{context}"
)

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{input}")
])

# --------------------------------------------------
# VECTORSTORE (BUILT ONCE)
# --------------------------------------------------
def _build_vectorstore():
    loader = PyPDFLoader(DATA_PATH)
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    splits = splitter.split_documents(docs)

    vectorstore = Chroma.from_documents(
        documents=splits,
        embedding=embeddings,
        collection_name=COLLECTION_NAME
    )
    return vectorstore


vectorstore = _build_vectorstore()
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# --------------------------------------------------
# RAG CHAIN (BUILT ONCE)
# --------------------------------------------------
qa_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, qa_chain)

# --------------------------------------------------
# PUBLIC FUNCTION (USE THIS IN FASTAPI)
# --------------------------------------------------
def get_answer(question: str) -> str:
    response = rag_chain.invoke({"input": question})
    return response["answer"]

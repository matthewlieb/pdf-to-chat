import os
import dotenv
import fitz
import streamlit as st
from langchain import hub
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate

# Load environment variables
dotenv.load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")

# Initialize the language model
llm = ChatOpenAI(model="gpt-4o")

# Define a Document class to wrap the dictionary
class Document:
    def __init__(self, page_content, metadata=None):
        self.page_content = page_content
        self.metadata = metadata if metadata is not None else {}

# Load, chunk and index the contents of the PDF documents
def load_pdfs(uploaded_files):
    docs = []
    for uploaded_file in uploaded_files:
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        for page_num, page in enumerate(doc):
            docs.append(Document(page.get_text(), metadata={"page_number": page_num + 1, "file_name": uploaded_file.name}))
    return docs

# Streamlit application
st.title("PDF Question and Answer with Sources")
st.write("Upload one or more PDF documents and enter a question:")

uploaded_files = st.file_uploader("Choose PDF files", type="pdf", accept_multiple_files=True)

if uploaded_files:
    docs = load_pdfs(uploaded_files)
    
    # Split the documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)

    # Create a vector store
    vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())

    # Retrieve and generate using the relevant snippets of the PDF
    retriever = vectorstore.as_retriever()
    
    system_prompt = (
        "You are an assistant for question-answering tasks. "
        "Use the following pieces of retrieved context to answer "
        "the question. If you don't know the answer, say that you "
        "don't know. Use three sentences maximum and keep the "
        "answer concise."
        "\n\n"
        "{context}"
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "{input}"),
        ]
    )

    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)

    question = st.text_input("Question:")
    if st.button("Submit"):
        if question:
            result = rag_chain.invoke({"input": question})
            st.write("Response:")
            st.write(result['answer'])

            st.write("Sources:")
            for doc in result['context']:
                st.write(f"- Page {doc.metadata['page_number']} from {doc.metadata['file_name']}")

    # Cleanup (optional, depending on your use case)
    vectorstore.delete_collection()
else:
    st.write("Please upload PDF files to proceed.")

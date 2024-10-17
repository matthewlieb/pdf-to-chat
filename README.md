# 📄 PDF to Chat

Welcome to the **PDF to Chat** repository! This Streamlit application allows users to upload PDF documents, ask questions about the contents, and receive concise answers along with relevant sources from the PDFs. The app leverages LangChain, OpenAI, and Chroma for efficient question-answering.

## 📋 Table of Contents

1. [Features](#features)
2. [Setup](#setup)
3. [Usage](#usage)
4. [How It Works](#how-it-works)
5. [Dependencies](#dependencies)
6. [Acknowledgements](#acknowledgements)
7. [License](#license)

## ✨ Features

- **📁 PDF Upload**: Upload one or more PDF files to be processed.
- **❓ Question and Answer**: Ask questions related to the content of the PDFs.
- **📝 Concise Answers**: Get concise answers to your questions.
- **🔍 Source References**: See which parts of the PDFs were used to generate the answer.

## 🛠 Setup

### Prerequisites

- Python 3.7 or higher
- An OpenAI API key
- An environment variable for LangChain API key

### Installation

1. **Clone the repository:**

```bash
git clone https://github.com/matthewlieb/pdf-to-chat.git
cd pdf-to-chat
```

2. **Create and activate a virtual environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install the required packages:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Set up environment variables:**

    Create a `.env` file in the project directory and add your OpenAI and LangChain API keys:

    ```bash
    touch .env
    ```

    Add the following lines to the `.env` file:

    ```dotenv
    OPENAI_API_KEY=your_openai_api_key
    LANGCHAIN_API_KEY=your_langchain_api_key
    ```

## 🚀 Usage

1. **Run the Streamlit application:**

    ```bash
    streamlit run app.py
    ```

2. **Upload PDFs and Ask Questions:**

    - Open the application in your browser (usually at `http://localhost:8501`).
    - Upload one or more PDF documents.
    - Enter a question related to the content of the uploaded PDFs.
    - Click on the "Submit" button to get your answer and the sources from the PDFs.

## 🧐 How It Works

### Components

- **PDF Loading and Splitting**: Uploaded PDFs are loaded and split into smaller chunks for efficient processing.
- **Vector Store**: The chunks are stored in a Chroma vector store for quick retrieval based on the input question.
- **Question Answering**: A retrieval-augmented generation (RAG) chain retrieves relevant document chunks and generates an answer using the OpenAI language model.
- **Source Attribution**: The sources (chunks of PDF content) used to generate the answer are displayed to the user.

### Detailed Steps

1. **PDF Loading**:
    - The PDFs are read using the `fitz` library (PyMuPDF).
    - Each page of the PDFs is converted into text and stored with metadata (page number and file name).

2. **Text Splitting**:
    - The documents are split into smaller chunks using `RecursiveCharacterTextSplitter` to handle large documents effectively.

3. **Vector Store Creation**:
    - The chunks are embedded using OpenAI's embeddings and stored in a Chroma vector store.

4. **Retrieval and Generation**:
    - A retriever fetches relevant chunks from the vector store based on the input question.
    - A language model (OpenAI's GPT) generates a concise answer using the retrieved context.

5. **Displaying Results**:
    - The generated answer is displayed along with the sources (relevant PDF chunks).

## 📦 Dependencies

- `streamlit`
- `python-dotenv`
- `langchain`
- `langchain-openai`
- `langchain-chroma`
- `fitz` (PyMuPDF)

You can install all dependencies using:

```bash
pip install -r requirements.txt
```

## 📄 License

This repository is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.

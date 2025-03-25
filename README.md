# 🏙️ **RealEstate Research Tool**

Engineered a Streamlit-based web app that cuts LLM API costs by ~70% and research time by ~50% using Retrieval-Augmented Generation (RAG) for real estate insights. Users input URLs and ask domain-specific questions, receiving precise answers via LangChain’s UnstructuredURLLoader, HuggingFace’s all-MiniLM-L6-v2 embeddings, ChromaDB for retrieval, and Llama3 (via Groq) with source references.

### Features

- Load URLs to fetch article content.
- Process article content through LangChain's UnstructuredURL Loader
- Construct an embedding vector using HuggingFace embeddings and leverage ChromaDB as the vectorstore, to enable swift and effective retrieval of relevant information.
- Interact with the LLM's (Llama3 via Groq) by inputting queries and receiving answers along with source URLs.

### Usage

The web app will open in your browser after the set-up is complete.

- On the sidebar, you can input URLs directly.

- Initiate the data loading and processing by clicking "Process URLs."

- Observe the system as it performs text splitting, generates embedding vectors using HuggingFace's Embedding Model.

- The embeddings will be stored in ChromaDB.

- One can now ask a question and get the answer based on those news articles

![product screenshot](image.png)

### Set-up

1. Run the following command to install all dependencies. 

    ```bash
    pip install -r requirements.txt
    ```

2. Create a .env file with your GROQ credentials as follows:
    ```text
    GROQ_MODEL=MODEL_NAME_HERE
    GROQ_API_KEY=GROQ_API_KEY_HERE
    ```

3. Run the streamlit app by running the following command.

    ```bash
    streamlit run main.py
    ```


---

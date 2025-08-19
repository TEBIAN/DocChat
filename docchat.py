import streamlit as st
import os
from langchain_community.document_loaders import UnstructuredHTMLLoader, Docx2txtLoader, PyPDFLoader
import tempfile
from langchain.chains import ConversationalRetrievalChain
from langchain_ollama  import ChatOllama
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.memory import ConversationBufferMemory
from langchain_core.messages import SystemMessage

# Set Streamlit page config
st.set_page_config(page_title="DocChat", page_icon="📄")

def main():
    st.title("📄 DocChat - Chat with Your Documents")
    st.markdown("Upload a PDF, Word, or HTML file and ask questions about its content.")

    # Initialize session state
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "vectorstore" not in st.session_state:
        st.session_state.vectorstore = None

    # Sidebar for settings
    with st.sidebar:
        st.header("Settings")
        chunk_size = st.slider("Chunk Size", 500, 2000, 1000)
        temperature = st.slider("LLM Temperature", 0.0, 1.0, 0.7)

        uploaded_file = st.file_uploader(
            "Upload a document",
            type=["pdf", "docx", "html"]
        )

        if uploaded_file:
            with st.spinner("Processing document..."):
                try:
                    # Save the uploaded file temporarily
                    suffix = "." + uploaded_file.name.split(".")[-1]
                    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
                        tmp_file.write(uploaded_file.getvalue())
                        file_path = tmp_file.name

                    st.success(f"File uploaded: {uploaded_file.name}")

                    if file_path.endswith(".pdf"):
                        st.success("PDF recognized")
                        loader = PyPDFLoader(file_path)
                    elif file_path.endswith(".docx"):
                        st.success("Word document recognized")
                        loader = Docx2txtLoader(file_path)
                    elif file_path.endswith(".html"):
                        st.success("HTML document recognized")
                        loader = UnstructuredHTMLLoader(file_path)
                    else:
                        st.error("Unsupported file format")
                        return
                    
                    documents = loader.load()

                    # Split text into chunks
                    text_splitter = RecursiveCharacterTextSplitter(
                        chunk_size=chunk_size,
                        chunk_overlap=int(chunk_size/10))
                    chunks = text_splitter.split_documents(documents)
                    

                    # Create embeddings
                    embeddings = OllamaEmbeddings(model="nomic-embed-text:latest")
                    
                    # Create vector store
                    vectorstore = FAISS.from_documents(chunks, embeddings)
                    st.session_state.vectorstore = vectorstore

                    # Create conversation chain
                    memory = ConversationBufferMemory(
                        memory_key="chat_history",
                        return_messages=True
                    )
                    # Define system instructions
                    system_prompt = SystemMessage(
                        content=(
                            "You are a helpful AI assistant specialized in answering questions "
                            "from the provided document. Always give concise, accurate, and well-structured answers. "
                            "If the answer is not in the document, say 'Sorry! I don't know' instead of guessing."
                            "If user ask any question is not in the documents, say 'Sorry! I can answer questions about the document only.'"
                        )
                    )
                    st.session_state.conversation = ConversationalRetrievalChain.from_llm(
                        llm=ChatOllama(model="llama2:latest", temperature=temperature),
                        retriever=vectorstore.as_retriever(),
                        memory=memory
                    )
                    st.success("🚀 DocChat is ready! Ask your questions below.")
                    
                    # Clean up temporary file
                    os.unlink(file_path)
                    
                except Exception as e:
                    st.error(f"Error processing document: {str(e)}")
                    return
        else:
            st.warning("👆Please upload a file to continue.")   

    # Chat interface

    if "messages" not in st.session_state:
        conversation_chain.combine_docs_chain.llm_chain.prompt.messages.insert(0, system_prompt)
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask a question about the document"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        if st.session_state.conversation:
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    try:
                        response = st.session_state.conversation.invoke({"question": prompt})
                        st.markdown(response["answer"])
                        st.session_state.messages.append({"role": "assistant", "content": response["answer"]})
                    except Exception as e:
                        error_msg = f"Error generating response: {str(e)}"
                        st.error(error_msg)
                        st.session_state.messages.append({"role": "assistant", "content": error_msg})
        else:
            st.warning("Please upload a document first")

if __name__ == "__main__":
    main()
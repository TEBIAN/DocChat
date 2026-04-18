#  DocChat - Chat with Your Documents  

**DocChat** is a powerful document-based Q&A application built with **LangChain** and **Streamlit**. Upload your documents (PDF, Word, HTML) and chat with them using AI-powered natural language processing.  

##  Features  

✅ **Multi-Document Support** - Process PDFs, Word docs, and HTML files  
✅ **Conversational Memory** - Maintains chat history for context-aware responses  
✅ **Local AI** - Processing using Ollama with llama2  
✅ **Clean UI** - Intuitive Streamlit interface with chat history  
✅ **Efficient Processing** - Chunking and vector embeddings for fast retrieval 
✅ **Vector search** - fast document retrieval 

## Installation  

1. **Clone the repository**  
```bash
git clone https://github.com/TEBIAN/DocChat.git
cd docchat
```

2. **Create and activate virtual environment**  
Windows:
```powershell
python -m venv venv
.\venv\Scripts\activate
```

Linux/MacOS:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**  
```bash
pip install -r requirements.txt
```

##  Requirements  

- Python 3.8+   
- Ollama (for local LLM support)+ nomic-embed-text:latest and llama2:latest

##  Running the App  

```bash
streamlit run docchat.py
```  

The app will open in your browser at `http://localhost:8501`.  

##  Configuration  

Customize settings via the sidebar:  
- **OpenAI API Key**: Required for default LLM/embeddings or use local ollama  
- **Embedding Model**: Choose between OpenAI or HuggingFace or local Ollama  
- **Chunk Size**: Adjust document processing size (500-2000 chars)  
- **Temperature**: Control response creativity (0.0-1.0)  

##  Supported File Formats  

| Format | Loader |  
|--------|--------|  
| PDF | `PyPDFLoader` |  
| Word (.docx) | `Docx2txtLoader` |  
| HTML | `UnstructuredHTMLLoader` |  

*(More formats can be added via LangChain's document loaders)*  

##  How It Works  

1. **Document Processing**  
   - Files are split into optimized chunks  
   - Text converted to vector embeddings  
   - Stored in Chroma vector database  

2. **Question Answering**  
   - User queries are matched with relevant document chunks  
   - LLM generates answers using retrieved context  
   - Conversation history maintained for follow-up questions  

##  Advanced Features  

```python
# Example: Adding PowerPoint support
from langchain.document_loaders import UnstructuredPowerPointLoader

loaders['.pptx'] = UnstructuredPowerPointLoader
```

##  Deployment Options  

1. **Streamlit Sharing**  
   [![Deploy](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://streamlit.io/cloud)  

2. **Docker**  
```bash
docker build -t docchat .
docker run -p 8501:8501 docchat
```

3. **AWS/GCP**  
   - Package with Docker and deploy to ECS/Cloud Run  

##  License  

MIT License - See [LICENSE](LICENSE)  

##  Support & Contribution  

Found a bug? Want a new feature?  
- [Open an issue](https://github.com/TEBIAN/DocChat.git/issues)  
- Submit a PR  

---

**Happy Document Chatting!** 🎉  

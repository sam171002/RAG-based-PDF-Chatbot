# 🤖 DocuMentor-RAG: Your Intelligent PDF Companion

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![LangChain](https://img.shields.io/badge/LangChain-🦜️🔗-orange)
![Streamlit](https://img.shields.io/badge/Streamlit-UI%20Framework-red)
![Gemini](https://img.shields.io/badge/Google-Gemini%20AI-lightblue)
![RAG](https://img.shields.io/badge/Architecture-RAG-brightgreen)

**DocuMentor** - AI-powered document assistant that reads PDFs so you don't have to! Ask questions in natural language and get instant answers with proper citations. ✨

## 🚀 What Makes This Special?

- **📄 PDF Intelligence**: Upload any PDF and chat with it like a knowledgeable expert
- **🔍 Smart Citations**: Every answer comes with clickable page references
- **💬 Conversational Memory**: Remembers your chat history within each session
- **🎯 Accurate Answers**: Powered by Google's Gemini AI with RAG architecture
- **⚡ Easy to Use**: Beautiful Streamlit interface - no technical knowledge needed!

## 🏗️ How It Works 

```mermaid
graph LR
A[PDF Upload] --> B[Text Extraction & Chunking]
B --> C[Vector Embeddings]
C --> D[ChromaDB Storage]
E[User Question] --> F[Semantic Search]
F --> G[Context Building]
G --> H[Gemini AI Processing]
H --> I[Answer + Citations]
I --> J[Streamlit Display]
```
## Performance Evaluation

Built-in RAGAS evaluation ensures quality answers:

**Faithfulness Score:** 1.0000 (Answers stay true to source material)

**Answer Relevancy:** 0.6533 (Continuously improving!)

<img width="1918" height="1020" alt="chatbot1" src="https://github.com/user-attachments/assets/e150cf55-0440-484b-8237-1c4388c4c8cb" />

<img width="1918" height="1008" alt="chatbot3" src="https://github.com/user-attachments/assets/bed02604-4ac5-408d-a759-8685b8d3d770" />

<img width="1918" height="1010" alt="chatbot4" src="https://github.com/user-attachments/assets/560ed786-9ba5-460f-bafe-b58648763a4f" />

<img width="1918" height="1012" alt="chatbot5" src="https://github.com/user-attachments/assets/441bb8fa-a4fd-4ac7-b2e3-f26270ac87bd" />

## Project Structure

DocuMentor-RAG/
│

├── app_streamlit.py          -- Main Streamlit application

├── rag_notebook.ipynb        -- Jupyter notebook with RAG development

├── Flowchart.pdf             -- Flow of the project

├── H-046-029216-00-4.0-hybase-v6-user-manual-en  -- PDF that i used

├── README.md                 -- This awesome documentation!


## Thank you for checking out this project! ❤️

    
    




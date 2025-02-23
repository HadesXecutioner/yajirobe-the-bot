import streamlit as st
import ollama
import PyPDF2
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.tokenize import sent_tokenize
import io
import re
import warnings
warnings.filterwarnings('ignore')

nltk.download('punkt', quiet=True)
nltk.download('punkt_tab')

class RAGBot:
    def __init__(self):
        self.documents = []
        self.vectorizer = TfidfVectorizer()
        self.document_vectors = None
        self.threshold = 0.2 
        self.summary = ""

    def process_docs(self):
        if self.documents:
            self.document_vectors = self.vectorizer.fit_transform(self.documents)
        

    def loadpdf(self, pdf):
        """Load and Process a PDF file"""
        try:
            PdfReader = PyPDF2.PdfReader(pdf)
            text = ""
            for page in PdfReader.pages:
                text += page.extract_text() or ""

            sentences = sent_tokenize(text)
            self.documents.extend(sentences)
            self.document_vectors = self.vectorizer.fit_transform(self.documents)


            self.summary = " ".join(sentences[:5] if len(sentences) > 5 else " ".join(sentences))

            return f"Successfully loaded {len(sentences)} sentences from the provied PDF"
        except Exception as e:
            return f"Error loading the PDF: {e}"
        
    def relevantquery(self, query):
        """Check is the query is relevant to the loaded documents."""
        if not self.documents:
            return False
        
        query_vector = self.vectorizer.transform([query])
        similarities = cosine_similarity(query_vector, self.document_vectors)
        maxSimilarity = similarities[0].max()

        return maxSimilarity > self.threshold
    

    def getContext(self, query, num_results=3):
        """Find the most relevant senteces for the given query"""

        query_vector = self.vectorizer.transform([query])
        similarities = cosine_similarity(query_vector, self.document_vectors)

        TopIndices = similarities[0].argsort()[-num_results:][::-1]
        return [self.documents[i] for i in TopIndices]   

    def response_generate(self, query):
        """Generate most appropriate response based on relevant context"""
        
        if not self.documents:
            return "Please upload and process a PDF document."
        
        if not self.relevantquery(query):
            return "I apologize , but I cannot aswer this question as it is not within the provided document"
        
        relevantSentences = self.getContext(query)
        context = "\n\n".join(relevantSentences) # May never Run
        
        response = ollama.chat(
            model = " ", # Model Name (Local Model)
            messages=[
                {
                    "role": "system", 
                    "content": """You are a helpful assistant focused on answering questions about the provided document.
                    - Answer questions accurately based on the given context
                    - Stay strictly within the scope of the provided document
                    - If a question cannot be answered from the context, politely decline
                    - Maintain a professional and friendly tone
                    - Do not make assumptions or add information beyond what's in the context
                    - If the context is insufficient, ask for clarification
                    - If user provides Salutations or Greetings, politely decline by saying the following 'I am Yajirobe, and I work as a RAG chatbot, I answer only when a document is uploaded and my answers are strictly relevant to the document itself.'"""
                 }, # Model Prompt

                {"role": "user", "content": f"content: {context}\n\nQuestion: {query}"} # User Prompt
            ]
        )

        return response["message"]["content"]
# Initialize Session state
if "bot" not in st.session_state:
    st.session_state["bot"] = RAGBot()
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

#UI for Streamlit

st.title("Yajirobe The Bot⚔️")


with st.sidebar:
    st.header("Upload Documents")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    if uploaded_file and st.button("Process PDF"):
        result = st.session_state["bot"].loadpdf(uploaded_file)
        st.success(result)
            
# Display PDF Summary
show_summary = st.checkbox("Show PDF Summary", value=True)

# Display summary only if the checkbox is checked
if show_summary and "bot" in st.session_state and hasattr(st.session_state["bot"], "summary"):
    if st.session_state["bot"].summary:
        st.subheader("📄 PDF Summary:")
        st.write(st.session_state["bot"].summary)


st.caption("Ask Away!")

chat_container = st.container()
with chat_container:
    for message in st.session_state["chat_history"]:
        with st.chat_message(message["role"]):
            st.write(message["content"])

if prompt := st.chat_input("Ask me about the documents..."):
    with st.chat_message("user"):
        st.write(prompt)
    
    st.session_state["chat_history"].append({"role": "user", "content": prompt})
    response = st.session_state["bot"].response_generate(prompt)
    
    with st.chat_message("assistant"):
        st.write(response)
    
    st.session_state["chat_history"].append({"role": "assistant", "content": response})

# Chat history download
if st.sidebar.button("Download Chat History"):
    chat_text = "\n".join([f'{msg["role"]}: {msg["content"]}' for msg in st.session_state["chat_history"]])
    st.sidebar.download_button("Download", chat_text, "chat_history.txt")
    

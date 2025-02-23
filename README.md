# Yajirobe The Bot ⚔️

Yajirobe The Bot is a RAG (Retrieval-Augmented Generation) chatbot built using Streamlit, Ollama, and scikit-learn. It allows users to upload PDF documents, extract text, and ask questions related to the document. The chatbot finds relevant context from the document and generates responses using a locally installed LLM.

## Features

- 📂 Upload and process PDF files
- 🔎 Retrieve relevant sentences from the document
- 🤖 Generate responses based on context using a local LLM
- 📝 Display PDF summary
- 💬 Interactive chat with history
- ⬇️ Download chat history

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/HadesXecutioner/yajirobe-the-bot.git
   cd yajirobe-the-bot
   ```
2. Create a virtual environment (optional but recommended): (I used a conda enviorment :P)
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```
3. Install the dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Run the Streamlit app:
   ```sh
   streamlit run main.py
   ```

## Dependencies

- `streamlit`
- `ollama`
- `PyPDF2`
- `scikit-learn`
- `nltk`

## Usage

1. Open the app in your browser after running the script. [You can do that by typing "streamlit run <filename>.py" in the terminal of your code editor]
2. Upload a PDF file from the sidebar.
3. Ask questions about the document using the chat input.
4. View responses based on the extracted text.
5. Download the chat history if needed.

## To-Do

- [ ] Improve response accuracy by fine-tuning vectorization
- [ ] Add multi-PDF support
- [ ] Implement UI enhancements
- [ ] Optimize memory usage for large documents

## License

This project is licensed under the MIT License. Feel free to modify and use it as needed.

## Author

**Muhammad Ahmad Khan**

Happy coding!

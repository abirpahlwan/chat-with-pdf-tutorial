import os

from dotenv import load_dotenv
import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
from pypdf import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.callbacks import get_openai_callback


# Config
load_dotenv()
st.set_page_config(page_title='Chat PDF', page_icon='🤖', layout='wide')


# Sidebar contents
def sidebar():
    with st.sidebar:
        st.title('Chat PDF')
        st.markdown('''

            ''')
        add_vertical_space(40)
        st.write('Made by [Abir Pahlwan](https://github.com/abirpahlwan/) 🤖')


# Main contents
def main():
    # Header
    st.header('Chat with PDF')

    # Upload a pdf file
    pdf = st.file_uploader('Upload your PDF', type='pdf')

    if pdf is not None:
        pdf_reader = PdfReader(pdf)

        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )

        chunks = text_splitter.split_text(text=text)

        # Create embeddings
        embeddings = OpenAIEmbeddings()

        db_name = pdf.name[:-4]  # remove last 4 chars .pdf
        if os.path.exists(f'store/{db_name}'):
            store = FAISS.load_local(f'store/{db_name}', embeddings)
            st.info('Embeddings loaded from the disk')
        else:
            store = FAISS.from_texts(chunks, embeddings)    # costly OpenAI API Call
            # FAISS.save_local(store, f'/{db_name}')
            store.save_local(f'store/{db_name}')
            st.info('Embeddings saved to the disk')

        # user questions/query
        query = st.text_input("Ask questions about your PDF file:")

        if query:
            docs = store.similarity_search(query=query, k=3)    # k = how many relevant docs to return
            llm = OpenAI(temperature=0, model="gpt-3.5-turbo-instruct")
            chain = load_qa_chain(llm=llm, chain_type="stuff")
            with get_openai_callback() as cb:
                response = chain.run(input_documents=docs, question=query)
                print(cb)   # prints token usage and cost in console
            st.write(response)

    pass


if __name__ == '__main__':
    sidebar()
    main()

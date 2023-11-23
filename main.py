import os
import pickle

from dotenv import load_dotenv
import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
from pypdf import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS


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

        # st.write(text)

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )

        chunks = text_splitter.split_text(text=text)
        # st.write(chunks)

        # embeddings
        db_name = pdf.name[:-4]  # remove last 4 chars .pdf
        # st.write(f'{db_name}')

        embeddings = OpenAIEmbeddings()

        if os.path.exists(f'store/{db_name}'):
            store = FAISS.load_local(f'store/{db_name}', embeddings)
            st.write('Embeddings loaded from the disk')
        else:
            store = FAISS.from_texts(chunks, embeddings)
            # FAISS.save_local(store, f'{db_name}.index')
            store.save_local(f'store/{db_name}')
            st.write('Embeddings saved to the disk')

    pass


if __name__ == '__main__':
    sidebar()
    main()

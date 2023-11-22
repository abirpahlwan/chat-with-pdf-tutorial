import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space

# Config
st.set_page_config(page_title='Chat PDF', page_icon='🤖', layout='wide')

# Sidebar contents
with st.sidebar:
    st.title('Chat with Your PDF')
    st.markdown('''
        
    ''')
    add_vertical_space(5)
    st.write('Made by 🤖[Abir Pahlwan](https://github.com/abirpahlwan/)')


with st.container():
    st.write('uhm...')
    left_column, right_column = st.columns(2)
    with left_column:
        st.header('What is this!?')
        st.write('')


def main():
    # Header
    st.header('Chat with PDF')
    st.subheader('I am Abir')

    # Upload a pdf file
    pdf = st.file_uploader('Upload your PDF', type='pdf')

    pass


if __name__ == '__main__':
    main()

import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space


# Config
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
    st.subheader('Try it out!')

    with st.container():
        left_column, right_column = st.columns(2)
        with left_column:
            st.write('uhm...')

    # Upload a pdf file
    pdf = st.file_uploader('Upload your PDF', type='pdf')

    pass


if __name__ == '__main__':
    sidebar()
    main()

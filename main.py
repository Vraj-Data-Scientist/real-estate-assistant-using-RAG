import streamlit as st
from rag import process_urls, generate_answer

# Add Open Graph metadata
st.markdown(
    """
    <meta property="og:title" content="Real Estate Research Tool">
    <meta property="og:description" content="A tool to answer real estate questions using provided URLs.">
    <meta property="og:image" content="https://github.com/Vraj-Data-Scientist/real-estate-assistant-using-RAG/blob/main/image.png?raw=true">
    <meta property="og:url" content="https://real-estate-assistant-using-rag-vraj-dobariya.streamlit.app/">
    """,
    unsafe_allow_html=True
)

st.title("Real Estate Research Tool")



url1 = st.sidebar.text_input("URL 1")
url2 = st.sidebar.text_input("URL 2")
url3 = st.sidebar.text_input("URL 3")

placeholder = st.empty()

with st.expander("How This Tool Supports You 🏠"):
    st.markdown("""
    This application answers your real estate questions using websites you provide.

     It Works Well When ✅
    - The website contains your answer (e.g., mortgage rates 💰), whether current or historical.
      - *Example*: "What’s the current 30-year rate?" or "What was it on March 20, 2025?"—if the site includes that data.

     It May Not Work When 🚫
    - The website doesn’t have the information (e.g., a past rate on a current-only page).
    - Data is in images 🖼️, tables, or requires a login 🔒.
    - Certain sites (e.g., CNBC) restrict access 🌐⛔.

     Helpful Tips 💡
    - Choose websites with clear, text-based data 📝.
    - Avoid pages with logins or restrictions.
    """)



process_url_button = st.sidebar.button("Process URLs")
if process_url_button:
    urls = [url for url in (url1, url2, url3) if url!='']
    if len(urls) == 0:
        placeholder.text("You must provide at least one valid url")
    else:
        for status in process_urls(urls):
            placeholder.text(status)

query = placeholder.text_input("Question")
if query:
    try:
        answer, sources = generate_answer(query)
        st.header("Answer:")
        st.write(answer)

        if sources:
            st.subheader("Sources:")
            for source in sources.split("\n"):
                st.write(source)
    except RuntimeError as e:
        placeholder.text("You must process urls first")

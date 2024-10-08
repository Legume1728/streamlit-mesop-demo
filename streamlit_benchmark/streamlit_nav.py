import streamlit as st

pages = {
    "Pages": [
        st.Page("streamlit_benchmark.py", title="Single benchmark"),
        st.Page("streamlit_compare.py", title="Compare"),
    ]
}
pg = st.navigation(pages)
pg.run()

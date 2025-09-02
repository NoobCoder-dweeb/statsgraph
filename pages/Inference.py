import streamlit as st
from utils.common import scaffold_page

def app():
    """
    Renders the page content.
    """
    scaffold_page(
        title="📐 Inference & Hypothesis Testing",
        description="Conduct statistical inference and hypothesis testing on your data."
    )

    if st.session_state.get("state") == 0:
        st.error("Please complete the Data Cleaning step before proceeding to Inference.")
        st.stop()

if __name__ == "__main__":
    app()
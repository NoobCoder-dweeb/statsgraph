import streamlit as st
from utils.common import scaffold_page

def app():
    """
    Renders the page content.
    """
    scaffold_page(
        title="📊 Exploratory Data Analysis (EDA)",
        description="Perform exploratory data analysis on your cleaned dataset(s)."
    )

    if st.session_state.get("state") == 0:
        st.error("Please complete the Data Cleaning step before proceeding to EDA.")
        st.stop()

if __name__ == "__main__":
    app()
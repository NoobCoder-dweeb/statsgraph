import streamlit as st
import scipy
from utils.common import scaffold_page

"""
Numerical: T-Tests, Dunett's test, Kendell's tau test, kurtosis tests, Spearman correlation coefficient
Categorical: Chi-Squared Test, Fisher's exact test,
"""

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

    # Ensure that there are 2 files uploaded
    if "dataframes" not in st.session_state \
        or len(st.session_state["dataframes"].keys()) < 2 \
        or not st.session_state["dataframes"]:
        st.error("Please ensure that you have uploaded more than 1 datasets.")
        st.stop()

    


if __name__ == "__main__":
    app()
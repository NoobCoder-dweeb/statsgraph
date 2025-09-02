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
        st.toast("Please complete the Data Cleaning step before proceeding to EDA.", 
                 duration="long", 
                 icon="⚠️")
        st.stop()

    if "dataframes" in st.session_state and st.session_state["dataframes"] is not None:
        st.subheader("Loaded DataFrames")
        for key, df in st.session_state["dataframes"].items():
            st.markdown(f"### {key}")
            st.dataframe(
                df,
                width="stretch",
                hide_index=True,
            )
        

if __name__ == "__main__":
    app()
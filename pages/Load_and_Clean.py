import streamlit as st
import pandas as pd
from utils.common import scaffold_page
from typing import Any

def load_dataframe(uploaded_file: Any) -> pd.DataFrame:
    """
    Load dataframes from uploaded files.
    Args:
        uploaded_file (Any): The uploaded file object from Streamlit file_uploader.
    Returns:
        pd.DataFrame: The loaded dataframe.
    """
    return pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
    

def app():
    scaffold_page(
        title="📂 Load and Clean Data",
        description="Upload your dataset(s) and perform initial cleaning."
    )

    uploaded_files = st.file_uploader(
        label="Upload your dataset (CSV, XLSX):",
        type=["csv", "xlsx"],
        accept_multiple_files=True,
    )

    if not uploaded_files:
        st.info("Please upload at least one file to proceed.")
        st.stop()
    
    if len(uploaded_files) > 2:
        st.toast("You can upload multiple files, but at most 2 files.", 
                 icon="⚠️", 
                 duration="short")
        st.stop()
    dataframes = {}
    if len(uploaded_files) > 0:
        st.subheader("Preview of Loaded Data")

    for i, uploaded_file in enumerate(uploaded_files):
        df = load_dataframe(uploaded_file)
        columns = df.columns.tolist()


        dataframes[f"file_{i+1}_{uploaded_file.name}"] = df

    if st.session_state.get("dataframes") is None:
        st.session_state["dataframes"] = dataframes
    else:
        st.session_state["dataframes"].update(dataframes)

    st.session_state["state"] = 1  # Move to next step

    for key, df in dataframes.items():
        st.markdown(f"### Data Preview: {key}")
        edited_df = st.data_editor(
            df,
            num_rows="dynamic",
            hide_index=True,
            key=key,
        )
        dataframes[key] = edited_df

if __name__ == "__main__":
    app()
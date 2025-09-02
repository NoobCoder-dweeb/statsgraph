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

def load_tab(tab, df):
    pass

def app():
    scaffold_page(
        title="📂 Load and Clean Data",
        description="Upload your dataset(s) and perform initial cleaning."
    )

    if "dataframes" not in st.session_state or st.session_state["dataframes"] is None:
        st.session_state["dataframes"] = {}

    uploaded_files = st.file_uploader(
        label="Upload your dataset (CSV, XLSX):",
        type=["csv", "xlsx"],
        accept_multiple_files=True,
    )

    if not uploaded_files:
        st.info("Please upload at least one file to proceed.")
        st.stop()

    if uploaded_files:
        if len(uploaded_files) > 2:
            st.toast("You can upload multiple files, but at most 2 files.", 
                    icon="⚠️", 
                    duration="short")
            st.stop()
    
        for i, uploaded_file in enumerate(uploaded_files):
            key = f"file_{i+1}_{uploaded_file.name}"
            
            if key not in st.session_state["dataframes"]:
                st.session_state["dataframes"][key] = load_dataframe(uploaded_file)

    if not st.session_state["dataframes"]:
        st.warning("No valid dataframes loaded. Please check your files.")
        st.stop()

    # if len(uploaded_files) > 0:
    st.subheader("Preview of Loaded Data")

    if "state" in st.session_state:
        st.session_state["state"] = 1  # Move to next step

    # TODO: Add data cleaning options here
    # df_keys = list(dataframes.keys())

    # if len(dataframes.keys()) == 1:
    #     key = df_keys[0]

    #     st.markdown(f"### Data Preview: {key}")
    #     columns = df.columns.tolist()
    #     edited_df = st.data_editor(
    #         df,
    #         num_rows="dynamic",
    #         hide_index=True,
    #         key=key,
    #     )

    #     dataframes[key] = edited_df
    #     st.session_state["dataframes"].update(edited_df)
    # else:
    #     tab1, tab2 = st.tabs(list(dataframes.keys()))

        
    for key, df in st.session_state["dataframes"].items():
        st.markdown(f"### Data Preview: {key}")
        st.button(
            "Remove Duplicates", 
            key=f"remove_dup_{key}",
            on_click=lambda k=key: st.session_state["dataframes"].update({k: st.session_state["dataframes"][k].drop_duplicates()}),
            )
        columns = df.columns.tolist()
        edited_df = st.data_editor(
            df,
            num_rows="dynamic",
            hide_index=True,
            key=key,
        )

        # Update the dataframe in session state
        st.session_state["dataframes"][key] = edited_df        

if __name__ == "__main__":
    app()
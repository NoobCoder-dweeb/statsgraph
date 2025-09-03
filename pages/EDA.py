import streamlit as st
from utils.common import scaffold_page
import pandas as pd

def initial_check() -> None:
    if st.session_state.get("state") == 0:
        st.toast("Please complete the Data Cleaning step before proceeding to EDA.", 
                 duration="long", 
                 icon="⚠️")
        st.stop()

    if "dataframes" not in st.session_state or st.session_state["dataframes"] is None:
        st.warning("No dataframes found. Please upload and clean your data in the Load and Clean Data step.")
        st.stop()

def descriptive_statistics(df: pd.DataFrame) -> None:
    if st.checkbox("Show Descriptive Statistics"):
        st.subheader("Descriptive Statistics")
        st.write(df.describe(include='all').T)

def store_column_selection(col: str) -> None:
    st.session_state["selected_column"] = col

def column_eda(df: pd.DataFrame) -> None:
    st.subheader("Column-Level Analysis")
    col = st.selectbox("Select a column to analyse:", df.columns.tolist(), on_change=store_column_selection)

    if df[col].dtype in ["int64", "float64"]:
        st.write("📊 Numeric Summary")
        st.write(df[col].describe())
    elif df[col].dtype in ["object", "category"]:
        st.write("🔤 Categorical Summary")
        st.write(df[col].value_counts())
    else:
        st.error("Column type not supported for detailed analysis.")

def visualisations(df: pd.DataFrame)-> None:
    st.subheader("Visualisations")

    if "selected_column" not in st.session_state or st.session_state["selected_column"] is None:
        st.info("Please select a column for visualisation.")
        return
    
    if df.session_state["selected_column"] not in df.columns:
        st.error("Selected column not found in the dataframe.")
        return
    
    if st.button("Generate Visualisations"):
        col = st.sesion_state["selected_column"]

        if df[col].dtype in ["int64", "float64"]:
            pass  # Placeholder for numeric visualisations
        elif df[col].dtype in ["object", "category"]:
            pass  # Placeholder for categorical visualisations
        else:
            st.error("Column type not supported for visualisations.")


def app():
    """
    Renders the page content.
    """
    scaffold_page(
        title="📊 Exploratory Data Analysis (EDA)",
        description="Perform exploratory data analysis on your cleaned dataset(s)."
    )

    initial_check()
        
    df_keys = list(st.session_state["dataframes"].keys())
    data_choice = st.selectbox("Select a dataset for EDA:", df_keys)
    df = st.session_state["dataframes"][data_choice]

    st.markdown(f"### Data Preview: {data_choice}")
    st.write(f"Shape: {df.shape[0]} rows x {df.shape[1]} columns")

    st.info("Displaying 1000 rows for performance reasons.")
    st.dataframe(
        df.sample(min(len(df), 1000), random_state=42), 
        width="stretch",
        hide_index=True
        )
    
    descriptive_statistics(df)

    column_eda(df)
    
    visualisations(df)

if __name__ == "__main__":
    app()
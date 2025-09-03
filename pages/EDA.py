import streamlit as st
from utils.common import scaffold_page
from utils.compute import freedman_draconis_rule, sturges_rule
import pandas as pd
import math
import plotly.express as px

def initial_check() -> None:
    """
    Perform initial checks to ensure prerequisites are met.

    Returns:
        None
    """
    if st.session_state.get("state") == 0:
        st.toast("Please complete the Data Cleaning step before proceeding to EDA.", 
                 duration="long", 
                 icon="⚠️")
        st.stop()

    if "dataframes" not in st.session_state or st.session_state["dataframes"] is None:
        st.warning("No dataframes found. Please upload and clean your data in the Load and Clean Data step.")
        st.stop()

def descriptive_statistics(df: pd.DataFrame) -> None:
    """
    Display descriptive statistics of the dataframe.
    Args:
        df (pd.DataFrame): The dataframe containing the data.
    Returns:
        None
    """
    if st.checkbox("Show Descriptive Statistics"):
        st.subheader("Descriptive Statistics")
        st.write(df.describe(include='all').T)

def store_column_selection(col: str) -> None:
    if "selected_column" not in st.session_state:
        st.session_state["selected_column"] = None
    if col != st.session_state["selected_column"]:
        st.session_state["selected_column"] = col

def column_eda(df: pd.DataFrame) -> None:
    """
    Perform column-level analysis and store the selected column in session state.
    
    Args:
        df (pd.DataFrame): The dataframe containing the data.
    Returns:
        None
    """
    st.subheader("Column-Level Analysis")
    col = st.selectbox("Select a column to analyse:", df.columns.tolist())
    store_column_selection(col)

    if df[col].dtype in ["int64", "float64"]:
        st.write("📊 Numeric Summary")
        st.write(df[col].describe())
    elif df[col].dtype in ["object", "category"]:
        st.write("🔤 Categorical Summary")
        st.write(df[col].value_counts())
    else:
        st.error("Column type not supported for detailed analysis.")

def compute_nbins(series: pd.Series) -> int:
    """
    Compute optimal number of bins for historgram
    
    Args:
        series (pd.Series): The data series for which to compute the number of bins.
    Returns:
        int: The computed number of bins.
    """
    nbins = freedman_draconis_rule(series) if series.shape[0] > 200 else sturges_rule(series)
    nbins = max(5, min(nbins, int(math.sqrt(series.shape[0]))))  # Clamp between
    return nbins

def visualisations(df: pd.DataFrame)-> None:
    """
    Generate visualisations based on the selected column.

    Args:
        df (pd.DataFrame): The dataframe containing the data.

    Returns:
        None
    """
    st.subheader("Visualisations")

    if "selected_column" not in st.session_state or st.session_state["selected_column"] is None:
        st.info("Please select a column for visualisation.")
        return
    
    if st.session_state["selected_column"] not in df.columns:
        st.error("Selected column not found in the dataframe.")
        return
    
    if st.button("Generate Visualisations"):
        col = st.session_state["selected_column"]
        column_data = df[col]

        if column_data.dtype in ["int64", "float64"]:
            # Histogram
            fig = px.histogram(df.dropna(), x=col, nbins=compute_nbins(column_data), title=f"Histogram of {col}")
            st.plotly_chart(fig, width="stretch")

            # Box plot
            fig2 = px.box(df.dropna(), y=col, title=f"Box Plot of {col}")
            st.plotly_chart(fig2, width="stretch")

        elif column_data.dtype in ["object", "category"]:
            # Bar chart for value counts
            fig = px.bar(column_data.index,
                            y=column_data.values, 
                            title=f"Value Counts of {col}", 
                            labels={'x': "Counts", 'y': col})
            st.plotly_chart(fig, width="stretch")

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
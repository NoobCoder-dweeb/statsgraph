import streamlit as st
from utils.common import scaffold_page
from ydata_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report

@st.cache_resource (show_spinner="Generating profile report...")
def get_profile_report(df):
    if len(df) > 10000:
        df = df.sample(10000, random_state=42)
    return ProfileReport(df=df, minimal=True)

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

            pr = get_profile_report(df)
            st_profile_report(pr)
        

if __name__ == "__main__":
    app()
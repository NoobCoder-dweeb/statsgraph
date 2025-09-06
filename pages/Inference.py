import streamlit as st
import numpy as np
import scipy
from utils.common import scaffold_page
from typing import Callable, Tuple

"""
Numerical: T-Tests, Dunett's test, Kendell's tau test, kurtosis tests, Spearman correlation coefficient
Categorical: Chi-Squared Test, Fisher's exact test,
"""

HypothesisTest =  Callable[[np.ndarray, np.ndarray, str], Tuple[float, float]]

num_test = {
    "ttest" : (0,1),
}

cat_test = {
    "chi2": (0,1),
}

available_tests: dict = {
    "numerical": num_test,
    "categorical": cat_test,
}

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

    df_keys = list(st.session_state["dataframes"].keys())
    df1, df2 = st.session_state["dataframes"][df_keys[0]], st.session_state["dataframes"][df_keys[1]]

    df1_cols = list(df1.columns)
    df2_cols = list(df2.columns)

    # define 3 columns: set 1, set 2 and test
    col1, col2, col3 = st.columns(3)

    # have selectbox for users to choose the attributes to test for first 2 sets
    df1_col = col1.selectbox(
        label="Dataset 1",
        options=df1_cols,
        index=1,
    )

    df2_col = col2.selectbox(
        label="Dataset 2",
        options=df2_cols,
        index=2,
    )

    if df1[df1_col].dtype != df2[df2_col]:
        st.error("Error!! Both columns must have the same data type")
        st.stop()
    
    dtype = df1[df1_col].dtype
    d_test = available_tests["numerical"] if dtype in ["int64", "float64"] else available_tests["categorical"]
    
    test_options = list(d_test.keys())
    test_select = st.selectbox(
        label="Statistical Test",
        options=test_options,
        index=0,
    )
    
    # TODO: Apply test
    if test_select:
        pass
        # msg = st.toast(f"{test_select} selected")
        # msg.toast(f"{d_test[test_select]}")
if __name__ == "__main__":
    app()
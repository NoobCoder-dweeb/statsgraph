import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from utils.compute import (t_test, 
                           kendall_tau, 
                           kurtosis_test, 
                           spearman_corr,
                           chi2_test,
                           fisher_exact_test
                           )
from utils.common import scaffold_page
from typing import Callable, Dict, Any, Optional

HypothesisTest =  Callable[[pd.Series, pd.Series], Any]

num_test: Dict[str, HypothesisTest] = {
    "T-Test" : t_test,
    "Kendall's Tau": kendall_tau,
    "Kurtosis Test": kurtosis_test,
    "Spearman Correlation": spearman_corr,
}

cat_test = {
    "Chi-Squared Test": chi2_test,
    "Fisher's Exact Test": fisher_exact_test,
}

available_tests: dict = {
    "numerical": num_test,
    "categorical": cat_test,
}

def plot_overlapping_histograms(x: pd.Series, y: pd.Series, x_label: Optional[str], y_label: Optional[str], title:str):
    fig = go.Figure()
    fig.add_trace(go.Histogram(
        x=x,
        name=x_label,
        opacity=0.6,
        marker_color="blue",
        histnorm="probability density",
    ))
    fig.add_trace(go.Histogram(
        x=y,
        name=y_label,
        opacity=0.6,
        marker_color="red",
        histnorm="probability density",
    ))
    fig.update_layout(
        barmode="overlay",
        title=title,
        xaxis_title="Value",
        yaxis_title="Density",
    )

    return fig

def plot(df1_col, df2_col, test_type, test_select, x, y):
    if test_type == "numerical":
        if test_select in ["T-Test", "Kurtosis Test"]:
            fig = plot_overlapping_histograms(x=x, y=y, x_label=df1_col, y_label=df2_col,
                                                  title=f"{test_select}: Distribution Comparisons"
                                                  )
        else:
            fig = px.scatter(x=x, y=y, labels={"x": df1_col, "y": df2_col},
                                title=f"{test_select}: {df1_col} vs {df2_col}",
                                )
    else:
        table = pd.crosstab(x, y)
        fig = px.imshow(table, text_auto=True, aspect="auto",
                            title=f"{test_select}: Crosstab",
                            )
            
    st.plotly_chart(fig, width="stretch")

def display_metrics(test_select, result):
    if test_select == "Kurtosis Test":
        st.metric(label="Kurtosis (Dataset 1)", value=f"{result[0]: .4f}")
        st.metric(label="Kurtosis (Dataset 2)", value=f"{result[1]: .4f}")
    else:
        st.metric(label="Statistic", value=f"{result[0]: .4f}")
        st.metric(label="p-value", value=f"{result[1]: .4g}")

        if test_select in ["Kendall's Tau", "Spearman Correlation"]:
            st.metric(label="R²", value=f"{result[0]**2: .4f}")

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
    test_type = "numerical" if dtype in ["int64", "float64"] else "categorical"
    d_test = available_tests[test_type]
    
    test_options = list(d_test.keys())
    test_select = st.selectbox(
        label="Statistical Test",
        options=test_options,
        index=0,
    )
    
    x = df1[df1_col]
    y = df2[df2_col]

    if st.button("Run Test"):
        test_func: HypothesisTest = d_test[test_select]
        result = test_func(x, y)

        # Display metrics            
        display_metrics(test_select, result)

        # Plot 
        plot(df1_col, df2_col, test_type, test_select, x, y)


if __name__ == "__main__":
    app()
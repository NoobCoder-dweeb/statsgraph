import streamlit as st
import numpy as np
import plotly.graph_objects as go
from utils.common import scaffold_page
from utils.compute import (linear_regression, 
                           logistic_regression, 
                           polynomial_regression)
from sklearn.model_selection import train_test_split
from sklearn.metrics import (accuracy_score, 
                             f1_score, 
                             roc_curve,
                             roc_auc_score,
                             mean_absolute_error, 
                             mean_squared_log_error)
from sklearn.preprocessing import LabelEncoder

model_types = {
    "Linear Regression" : linear_regression,
    # "Polynomial Regression" : polynomial_regression,
    "Logistic Regression" : logistic_regression,
}

def plot_auc(model, X_test, y_test):
    """
    Function to plot ROC/AUC Curve

    Args:
        model: ML classification model
        X_test (np.array): Test data
        y_test (np.array): Test output

    Return:
        None
    """
    # get predicted probabilities
    if hasattr(model, "predict_proba"):
        y_proba = model.predict_proba(X_test)[:, 1]
    else:
        y_proba = model.predict(X_test)

    fpr, tpr, _ = roc_curve(y_true=y_test, y_score=y_proba)
    auc_score = roc_auc_score(y_true=y_test, y_score=y_proba)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=fpr, y=tpr, mode="lines", name=f"ROC Curve (AUC = {auc_score: .2f})"
    ))
    fig.add_trace(go.Scatter(
        x=[0,1], y=[0,1], mode="lines", name="Random", line={"dash":"dash"}
    ))
    fig.update_layout(
        title="Receiver Operating Characteristic (ROC)",
        xaxis_title="False Positive Rate",
        yaxis_title="True Positive Rate",
        legend={"x":0.6, "y":0.05}
    )

    st.plotly_chart(fig)

def plot_scatter(X_train, y_train, X_test, y_test):
    """
    Create Scatter plot

    Args:
        X_train (np.array) : Contains train data
        y_train (np.array) : Contains train output
        X_test (np.array) : Contains test data
        y_test (np.array) : Test Output
    Return:
        None
    """
    # 2D scatter plot
    if X_train.shape[1] == 1:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=X_train[:,0], y=y_train, mode="markers", name="Train"
        ))
        fig.add_trace(go.Scatter(
            x=X_test[:,0], y=y_test, mode="markers", name="Test", marker={"color":"red"}
        ))
        fig.update_layout(
            title="2D Scatter Plot",
            xaxis_title="Feature",
            yaxis_title="Target"
        )
        st.plotly_chart(fig)
    # 3D Scatter Plot
    elif X_train.shape[1] == 2:
        fig = go.Figure()
        fig.add_trace(go.Scatter3d(
            x=X_train[:,0], y=X_train[:,1], z=y_train, mode="markers", name="Train"
        ))
        fig.add_trace(go.Scatter3d(
            x=X_test[:,0], y=X_test[:,1], z=y_test, mode="markers", name="Test", marker={"color":"red"}
        ))
        fig.update_layout(
            title="3D Scatter Plot",
            scene={
                "xaxis_title":"Feature 1",
                "yaxis_title":"Feature 2",
                "zaxis_title":"Target",
        })
        st.plotly_chart(fig)
    else:
        st.warning("Scatter plot only supported for 1 or 2 features.")
        

def evaluate(model, X_train, X_test, y_train, y_test, pred_type):
    predictions = model.predict(X_test)
    
    col1, col2 = st.columns(2)
    evaluations = []
    if pred_type == "lr":
        evaluations.append(mean_absolute_error(y_true=y_test, y_pred=predictions))
        evaluations.append(np.sqrt(mean_squared_log_error(y_true=y_test, y_pred=predictions)))

        col1.metric(label="Mean Absolute Error", value=f"{evaluations[0]: .4f}")
        col2.metric(label="Root Mean Squared Log Error", value=f"{evaluations[1]: .4f}")
    else:
        evaluations.append(accuracy_score(y_true=y_test, y_pred=predictions))
        if len(np.unique(y_test)) == 2:
            f1 = f1_score(y_true=y_test, y_pred=predictions)
        else:
            f1 = f1_score(y_true=y_test, y_pred=predictions, average="macro")
            
        evaluations.append(f1)
        col1.metric(label="Accuracy", value=f"{evaluations[0]: .4f}")
        col2.metric(label="F1 Score", value=f"{evaluations[1]: .4f}")

    # Scatter plot
    plot_scatter(X_train, y_train, X_test, y_test)

    # Plot ROC/AUC for binary classification
    if len(np.unique(y_test)) == 2:
        plot_auc(model=model, X_test=X_test, y_test=y_test)

def app():
    """
    Renders the page content.
    """
    scaffold_page(
        title="📈 Modeling",
        description="Build and evaluate statistical or machine learning models on your data."
    )

    if st.session_state.get("state") == 0:
        st.error("Please complete the Data Cleaning step before proceeding to Inference.")
        st.stop()

    if "dataframes" not in st.session_state \
        or st.session_state["dataframes"] is None:
        st.error("Please upload at least a dataset.")
    
    dataframes_dict = st.session_state["dataframes"]

    # selectbox to select one dataframe
    df_select = st.selectbox(
        label="Dataframe",
        options=[key for key in dataframes_dict.keys()]
    )

    df = dataframes_dict[df_select]
    model_col, var_col = st.columns(2)

    technique = model_col.selectbox(
        label="Modelling technique",
        options=[key for key in model_types.keys()]
    )

    model_tech = model_types[technique]
    num_cols = df.select_dtypes(include=["int64", "float64"]).columns
    cat_cols = df.select_dtypes(include=["object", "category"]).columns
    pred_type = "lr"

    if technique == "Linear Regression":
        var_col.info("Select two independent variables and one dependent variable.")

        x_1 = var_col.selectbox(
            label="X_1",
            options=num_cols
        )
        
        x_2 = var_col.selectbox(
            label="X_2",
            options=num_cols
        )

        # if x_1 == x_2:
        #     st.error("X_1 must not be the same as X_2")
        #     st.stop()
        
        y = var_col.selectbox(
            label="Y",
            options=list(num_cols)
        )

        if x_1 == y or x_2 == y:
            st.error("There must not be same columns")
            st.stop()
        
        if x_2 == x_1:
            X = df[x_1].values.reshape(-1, 1)
        else:
            X = df[[x_1, x_2]].values

        Y = df[y].values

    elif technique == "Logistic Regression":
        var_col.info("Select an independent variable and one dependent variable.")
        pred_type="logit"

        x = var_col.selectbox(
            label="X",
            options=num_cols
        )
        
        y = var_col.selectbox(
            label="Y",
            options=list(cat_cols)
        )

        if x == y:
            st.error("There must not be same columns")
            st.stop()
        
        X = df[x].values.reshape(-1,1)
        Y = df[y].values
        Y = LabelEncoder().fit_transform(y=Y)
    # TODO: Polynomial Regression
    # else:
    #     var_col.info("Select an independent variable and one dependent variable.")

    #     x = var_col.selectbox(
    #         label="X",
    #         options=num_cols
    #     )
        
    #     y = var_col.selectbox(
    #         label="Y",
    #         options=list(num_cols)
    #     )

    #     if x == y:
    #         st.error("There must not be same columns")
    #         st.stop()
        
    #     X = df[x].values.reshape(-1,1)
    #     Y = df[y].values

    if st.button("Model Dataset"):
        X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)
        model = model_tech(df=df, x=X_train, y=y_train)

        evaluate(model=model, X_train=X_train, X_test=X_test, y_train=y_train, y_test=y_test, pred_type=pred_type)

if __name__ == "__main__":
    app()
import streamlit as st
import pandas as pd

st.title("📂 Load and Clean Data")
st.write("Upload your dataset(s) and perform initial cleaning.")

uploaded_files = st.file_uploader(
    label="Upload your dataset (CSV, XLSX):",
    type=["csv", "xlsx"],
    accept_multiple_files=True,
)
if not uploaded_files:
    st.info("Please upload at least one file to proceed.")
    st.stop()

dataframes = {}
if len(uploaded_files) > 0:
    st.subheader("Preview of Loaded Data")

for i, uploaded_file in enumerate(uploaded_files):
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    dataframes[f"data_editor_{i}"] = df

for key, df in dataframes.items():
    st.write(f"### Data Preview: {key}")
    edited_df = st.data_editor(
        df,
        num_rows="dynamic",
        hide_index=True,
        key=key,
    )
    dataframes[key] = edited_df
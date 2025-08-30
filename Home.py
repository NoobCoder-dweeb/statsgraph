import streamlit as st

def set_st_page_config():
    st.set_page_config(
        page_title="StatsGraph",
        page_icon="📊",
        layout="wide",
    )

    st.title("StatsGraph")
    st.write(
        """
        Welcome! This toolkit helps you perform statistical analysis step by step:

        1. **Load & Clean Data**  
        2. **Explore Data (EDA)**  
        3. **Inference & Hypothesis Testing**  
        4. **Modeling**  
        5. **Visualisation**  
        6. **Save Results**

        👉 Use the sidebar to navigate.
        """
    )

if __name__ == "__main__":
    set_st_page_config()
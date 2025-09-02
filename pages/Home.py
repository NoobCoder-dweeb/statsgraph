import streamlit as st
from utils.common import scaffold_page

def app():
    """
    Renders the page content.
    """
    scaffold_page(
        title="🏠 Home",
        description="""
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
    app()
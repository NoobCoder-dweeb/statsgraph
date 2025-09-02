import streamlit as st
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class MultiPager(BaseModel):
    """A class to manage multiple pages in a Streamlit app."""
    pages: List[Dict[str, Any]] = Field(..., description="List of pages with their titles and content.")

    def __init__(self) -> None:
        """Initializes the MultiPager with an empty list of pages."""
        super().__init__(pages=[])
    
    def add_page(self, title: str, func: Any) -> None:
        """Adds a new page to the MultiPager.
        
        Args:
            title (str): The title of the page.
            func (Any): The function that renders the page content.
        """
        self.pages.append({"title": title, "func": func})
    
    def run(self) -> None:
        """Runs the MultiPager, allowing users to navigate between pages."""
        page = st.sidebar.selectbox(
            label= "App Navigation",
            options=self.pages,
            format_func=lambda page: page["title"]
        )

        # add a button in sidebar to clear session state
        sidebar = st.sidebar
        if sidebar.button("Clear Session State"):
            st.session_state.state = 0
            st.session_state.dataframes = None
            st.rerun()

        # run page
        page["func"]()
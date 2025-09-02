import streamlit as st


def scaffold_page(title: str = f"", description: str = f"") -> None:
    """
    Scaffold a Streamlit page with a title and description.

    Args:
        title (str): The title of the page.
        description (str): A brief description of the page.
    Returns:
        None
    """
    st.title(title)
    st.write(description)

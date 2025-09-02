import streamlit as st
from multipager import MultiPager
from pages import Load_and_Clean, EDA, Inference, Modeling, Home
from typing import Dict, Callable

AppFunc = Callable[[], None]

st.set_page_config(
    page_title="StatsGraph",
    page_icon="📊",
    layout="wide",
)

st.markdown("# StatsGraph")


def add_pages(pages: MultiPager, page_info: Dict[str, AppFunc]) -> MultiPager:
    """ 
    Adds pages to the MultiPager instance.
    Args:
        pages (MultiPager): The MultiPager instance to which pages will be added.
        page_info (Dict[str, AppFunc]): A dictionary mapping page names to their corresponding functions.
    Returns:
        MultiPager: The updated MultiPager instance with added pages.
    """

    for page, func in page_info.items():
        pages.add_page(page, func)

    return pages

if __name__ == "__main__":
    pages = MultiPager()
    # initialise the initial dict
    page_info: Dict[str, AppFunc] = {
        "🏠 Home": Home.app,
        "📂 Load & Clean Data": Load_and_Clean.app,
        "📊 EDA": EDA.app,
        "🤖 Modeling": Modeling.app,
        "🔍 Inference": Inference.app,
    }
    
    pages = add_pages(pages, page_info=page_info)

    st.session_state.setdefault("dataframes", {})
    st.session_state.setdefault("state", 0)  # 0: Initial, 1: Data Loaded

    pages.run()

    # Conditional pages based on state
    # if st.session_state.get("state", 0) >= 1:
    #     conditional_page_info: Dict[str, AppFunc] = {
    #         "📊 EDA": EDA.app,
    #         "🤖 Modeling": Modeling.app,
    #         "🔍 Inference": Inference.app,
    #     }
    #     pages = add_pages(pages, page_info=conditional_page_info)

    #     st.rerun()
 
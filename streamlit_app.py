import streamlit as st
from multipager import MultiPager
from pages import Load_and_Clean, EDA, Inference, Modeling, Home

st.set_page_config(
    page_title="StatsGraph",
    page_icon="📊",
    layout="wide",
)

st.markdown("# StatsGraph")


def add_pages(pages: MultiPager) -> MultiPager:
    pages.add_page("🏠 Home", Home.app)
    pages.add_page("📂 Load & Clean Data", Load_and_Clean.app)
    pages.add_page("📊 EDA", EDA.app)
    pages.add_page("📐 Inference & Hypothesis Testing", Inference.app)
    pages.add_page("📈 Modeling", Modeling.app)

    return pages

if __name__ == "__main__":
    pages = MultiPager()
    pages = add_pages(pages)

    st.session_state.setdefault("dataframes", None)
    st.session_state.setdefault("state", 0)  # 0: Initial, 1: Data Loaded

    pages.run()
 
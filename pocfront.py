import streamlit as st


class multipageCreator:

    wealth_predictor = st.Page("Frontend/wealthpredictor.py", title = "Prediction of Wealth")
    stock_recommender = st.Page("Frontend/stockrecommender.py", title = "Recommendation from the stocks")


    pg = st.navigation(
        {
            "Market Analysis" : [wealth_predictor, stock_recommender]
        }
        )
    pg.run()


    
class StockDashboardApp:
    # 1. Page Configuration & Modern UI Styling
    def __init__(self): 

        st.set_page_config(
            page_title="ProTrade | Advanced Stock Market Intelligence",
            page_icon="⚡",
            layout="wide",
            initial_sidebar_state="expanded",
            )

        # Custom CSS for Sleek Financial Dashboard UI
        st.markdown(
            """
            <style>
            .main {
                background-color: #0e1117;
            }
            .stTextInput input, .stSelectbox select, .stDateInput input {
                background-color: #1a202c !important;
                color: #ffffff !important;
                border-radius: 8px !important;
            }
            </style>
        """,
            unsafe_allow_html=True,
        )

        multipageCreator()

if __name__ == "__main__":
    app = StockDashboardApp()




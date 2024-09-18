from pathlib import Path
import pandas as pd
import streamlit as st
from plot_team import create_plot, create_value_plot
from utils import setup_logger
from connector import DBManager
from About import NEXT_GW, dbm


# Config
logger = setup_logger(__name__)
logger.debug("Running from top")  # just useful to undserstand the order of execution


@st.cache_data(ttl=600, show_spinner="Pulling data...")
def get_df_sel():
    return pd.DataFrame(
        dbm.query(f"SELECT * FROM selections WHERE gameweek = {NEXT_GW}").fetchall()
    )


def main():
    st.title("lionel FPL Selector 🦁")
    df_sel = get_df_sel()

    tab1, tab2 = st.tabs(["🤖 Team Selection", ":chart: Team Forecasts and Values"])
    with tab1:
        st.subheader(f"Team Selections for Gameweek {NEXT_GW}")
        st.plotly_chart(create_plot(df_sel))

    with tab2:
        st.subheader(f"Team Forecasts and Values for Gameweek {NEXT_GW}")
        st.plotly_chart(create_value_plot(df_sel))


if __name__ == "__main__":
    st.set_page_config(
        page_title="lionel - Selections",
    )
    # sidebar()
    main()

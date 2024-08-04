import streamlit as st
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

from plot_players import show_player_fig

from utils import setup_logger

# Config
st.set_page_config(
    page_title="lionel - Forecasts",
)
logger = setup_logger(__name__)
logger.debug("Running from top")  # just useful to undserstand the order of execution

DATA = Path(__file__).parents[2] / "data"
df = pd.read_csv(DATA / "charts_1_25.csv")
players = list(df["name"].unique())
teams = list(df["team_name"].unique())
positions = list(df["position"].unique())


# Set up a callback for the prediction variable
def initialise_session_vars():
    if "pred_var" not in st.session_state:
        # logger.debug("Initialising messages")
        st.session_state.pred_var = "LSTMWithReLU"
    if "player_names" not in st.session_state:
        st.session_state.player_names = ["Bukayo Saka", "Martin Ødegaard"]
    if "teams" not in st.session_state:
        st.session_state.teams = []
    if "positions" not in st.session_state:
        st.session_state.positions = []


def main():
    st.title("lionel FPL Selector 🦁")

    st.plotly_chart(
        show_player_fig(
            df,
            st.session_state.player_names,
            st.session_state.teams,
            st.session_state.positions,
        ),
        # use_container_width=True,
        # height=1000,
        width=2000,
    )


def sidebar():
    with st.sidebar:
        st.title("Filter the forecasts")
        st.multiselect(
            "Player",
            players,
            key="player_names",
        )
        st.multiselect("Team", teams, key="teams")
        st.multiselect("Position", positions, key="positions")


if __name__ == "__main__":
    initialise_session_vars()
    main()
    sidebar()

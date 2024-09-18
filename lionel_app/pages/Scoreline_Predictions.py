import streamlit as st


from About import dbm, NEXT_GW
import pandas as pd
from utils import setup_logger
from plot_team import build_scoreline_plot

logger = setup_logger(__name__)
logger.debug("Running from top")  # just useful to undserstand the order of execution


# Set up a callback for the prediction variable
def initialise_session_vars():
    if "home_team" not in st.session_state:
        st.session_state.home_team = "Arsenal"
    if "away_team" not in st.session_state:
        st.session_state.away_team = "Tottenham"
    if "match" not in st.session_state:
        st.session_state.match = get_next_matches()[2]


@st.cache_data(ttl=600, show_spinner="Pulling data...")
def get_df_scoreline():
    return pd.DataFrame(dbm.query("SELECT * from scorelines").fetchall())


@st.cache_data(ttl=600, show_spinner="Pulling data...")
def get_next_matches():
    df = pd.DataFrame(dbm.query("SELECT * from next_games").fetchall())
    matches = (df["home_team"] + " vs " + df["away_team"]).to_list()
    return matches


@st.cache_data(ttl=600, show_spinner="Pulling data...")
def get_teams():
    return sorted(
        [_[0] for _ in dbm.query("SELECT DISTINCT home from scorelines").fetchall()]
    )


def main():

    st.title("lionel FPL Selector 🦁")

    # Not great to reload this on each run...
    df_scoreline = get_df_scoreline()
    home_team, away_team = st.session_state.match.split(" vs ")
    st.plotly_chart(
        build_scoreline_plot(df_scoreline, home_team, away_team),
        # use_container_width=True,
        height=2000,
        width=2000,
    )


def sidebar():
    with st.sidebar:
        st.title("Filter the forecasts")
        st.selectbox("Match", get_next_matches(), key="match", index=0)


if __name__ == "__main__":
    st.set_page_config(
        page_title="lionel - Scoreline Predictions",
    )
    initialise_session_vars()
    main()
    sidebar()

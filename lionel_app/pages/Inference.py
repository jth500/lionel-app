import streamlit as st
from About import dbm
import pandas as pd
from utils import setup_logger
from plot_players import build_player_inf_plot
from plot_team import build_team_inf_plot

logger = setup_logger(__name__)
logger.debug("Running from top")  # just useful to undserstand the order of execution


# Set up a callback for the prediction variable
def initialise_session_vars():

    if "min_mins" not in st.session_state:
        st.session_state.min_mins = 45


@st.cache_data(ttl=600, show_spinner="Pulling data...")
def get_df_player_inf():
    df = pd.DataFrame(dbm.query("SELECT * FROM player_inference").all())
    df["mean_minutes"] = df["mean_minutes"].round(0)
    return df


@st.cache_data(ttl=600, show_spinner="Pulling data...")
def get_df_team_inf():
    df_team_inf = pd.DataFrame(dbm.query("SELECT * FROM team_inference").all())
    df_team_inf[["attack", "defence"]] = df_team_inf[["attack", "defence"]]
    return df_team_inf


def main():
    st.title("lionel FPL Selector 🦁")

    # Not great to reload this on each run...
    df_player_inf = get_df_player_inf()
    df_team_inf = get_df_team_inf()

    tab1, tab2 = st.tabs(["🤖 Player Inference", ":chart: Team Inference"])
    with tab1:
        st.subheader("Player Goal and Assist Probability")
        st.plotly_chart(
            build_player_inf_plot(df_player_inf, st.session_state.min_mins),
            # use_container_width=True,
            height=2000,
            width=2000,
        )

    with tab2:
        st.subheader("Team Attack and Defence Strength")
        st.plotly_chart(build_team_inf_plot(df_team_inf))


def sidebar():
    with st.sidebar:
        # teams = get_teams()
        st.title("Filter the player inference values")
        st.slider("Minimum Average Minutes", 0, 90, key="min_mins", value=45)


if __name__ == "__main__":
    st.set_page_config(
        page_title="lionel - Forecasts",
    )
    initialise_session_vars()
    main()
    sidebar()

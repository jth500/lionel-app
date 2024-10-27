import pandas as pd
import streamlit as st
from About import NEXT_GW, dbm
from plot_team import build_scoreline_plot
from utils import setup_logger

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
    q = f"""
    SELECT home.name as home, away.name as away
    FROM fixtures
    INNER JOIN teams as away
    ON fixtures.home_id = away.id

    INNER JOIN teams as home
    ON fixtures.away_id = home.id

    WHERE season = 25 AND gameweek = {NEXT_GW}
    """
    df = pd.DataFrame(dbm.query(q).fetchall())

    matches = (df["home"] + " vs " + df["away"]).to_list()
    print(matches)
    return matches


@st.cache_data(ttl=600, show_spinner="Pulling data...")
def get_teams():
    return sorted(
        [_[0] for _ in dbm.query("SELECT DISTINCT home from scorelines").fetchall()]
    )


def main():

    st.title("🦁 Scoreline Predictions")
    with st.expander("More about scoreline predictions"):

        st.write(
            "The following plot shows the posterior distribution of goals for the selected home and away team. "
            "These values show the posterior distribution of the number of goals scored, for given home and away strengths, in the following statistical model:"
        )

        st.latex(
            r"""\text{goals}_{\text{home}} \sim \text{Poisson}(\lambda_{\text{home}})"""
        )
        st.latex(
            r"""\text{goals}_{\text{away}} \sim \text{Poisson}(\lambda_{\text{away}})"""
        )

        st.write("Where:")
        # latex aligned
        st.latex(
            r"""
            \begin{align*}
                \text{log}(\lambda_{\text{home}}) &= \beta_0 + \beta_{\text{home advantage}} + \beta_{\text{attack, home team}} + \beta_{\text{defence, away team}} \\ 
                \text{log}(\lambda_{\text{away}}) &= \beta_0 + \beta_{\text{defence, home team}} + \beta_{\text{attack, away team}}

            \end{align*}
            """
        )

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

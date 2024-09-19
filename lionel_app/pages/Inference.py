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
    st.title("🦁 Player & Team Inference")

    # Not great to reload this on each run...
    df_player_inf = get_df_player_inf()
    df_team_inf = get_df_team_inf()

    tab1, tab2 = st.tabs(["🤖 Player Inference", ":chart: Team Inference"])

    with tab1:
        st.subheader("Player Goal and Assist Probability")
        with st.expander("More about player inference"):
            st.write(
                "This plot shows the posterior mean of the probabilities of a player scoring or assisting "
                "a goal given that the player was on the pitch when their team scored the goal. Players who played few "
                "minutes are pulled towards the mean probability for that position. Each probability is that inferred from "
                "a multinomial distribution where the number of trials is the number of goals scored by the player's team in a given match."
            )
            st.write("I.e.:")
            st.latex(
                r"""
                \text{n}_{\text{goals}}, \text{n}_{\text{assists}}, \text{n}_\text{neither} \sim 
                \text{Multinomial}(\text{N}_\text{team goals}, \text{p}_{\text{score}}, \text{p}_{\text{assist}}, \text{p}_{\text{neither}})
                """
            )
        st.plotly_chart(
            build_player_inf_plot(df_player_inf, st.session_state.min_mins),
            # use_container_width=True,
            height=2000,
            width=2000,
        )

    with tab2:
        st.subheader("Team Attack and Defence Strength")
        with st.expander("More about team inference"):
            st.write(
                "The following plot shows the posterior mean of attack and defence strengths for each team. "
                "These values are the home and away team coefficients in the following statistical model. The values are manipulated to show the expected percentage change in the expected number of goals scored/conceded "
                "per game relative to an intercept."
            )

            st.latex(
                r"""\text{goals}_{\text{home}} \sim \text{Poisson}(\lambda_{\text{home}})"""
            )
            st.latex(
                r"""\text{goals}_{\text{away}} \sim \text{Poisson}(\lambda_{\text{away}})"""
            )

            # latex aligned
            st.latex(
                r"""
                \begin{align*}
                    \text{log}(\lambda_{\text{home}}) &= \beta_0 + \beta_{\text{home advantage}} + \beta_{\text{attack, home team}} + \beta_{\text{defence, away team}} \\ 
                    \text{log}(\lambda_{\text{away}}) &= \beta_0 + \beta_{\text{defence, home team}} + \beta_{\text{attack, away team}}

                \end{align*}
            """
            )
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

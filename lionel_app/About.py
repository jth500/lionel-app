import streamlit as st
from utils import setup_logger, get_gameweek
from connector import DBManager
import pandas as pd
import plotly
from plot_team import build_scoreline_plot
from pathlib import Path

# GLOBALS TO BE IMPORTED ELSEWHERE
DATA = Path(__file__).parents[1] / "data"
print(DATA)
dbm = DBManager(DATA / "fpl.db")
NEXT_GW = get_gameweek(dbm)


# Config
logger = setup_logger(__name__)
logger.debug("Running from top")  # just useful to undserstand the order of execution


@st.cache_data(ttl=600, show_spinner="Pulling data...")
def get_ars_city():
    return pd.read_csv(DATA / "city_arsenal.csv")


def body_model():

    st.title("About lionel")
    st.subheader("A Fantasy Premier League Team Optimisation Tool")
    st.write(
        "lionel is a Fantasy Premier League (FPL) team optimisation tool that "
        "uses a **Bayesian hierarchical model** to predict player performance and "
        "**linear programming** to maximise the selected team's points subject to the "
        "constraints of the FPL game. It is heavily inspired by work from the "
        "[Alan Turing Institute](https://www.turing.ac.uk/news/airsenal) and "
        "[Baio and Blangiardo (2010)](https://discovery.ucl.ac.uk/id/eprint/16040/1/16040.pdf)."
    )
    st.subheader("Bayesian Hierarchical Modelling")
    st.write(
        "lionel uses a Bayesian hierarchical model, implemented with a No-U-Turn Sampler in "
        "[PyMC](https://www.pymc.io/welcome.html), to simultaneously estimate match "
        "scorelines and, conditional on that, player points."
    )
    st.write("The model splits into two levels: match and player.")
    st.write("**Match Level**")
    st.write(
        "The model estimates the number of goals scored by the home and away teams using "
        "a Poisson regression (à la Baio and Blangiardo). The Poisson rate parameter is modelled as"
        "a function of an intercept, the teams' attack and defence strengths, and a "
        "dummy for home advantage."
    )
    st.write("**Player Level**")
    st.write(
        "Player points are modelled as a function of the player's goal contributions, clean sheets, and a player-"
        "level random effect to account for the propensity for yellow cards, bonus points, etc."
    )
    st.write(
        "The model estimates player contributions using a Multinomial regression model (à la Alan"
        " Turing Institute). The number of events is the number of goals estimated at the match level. "
        "For each goal, the possible involvements for each player are: goal, assist, or neither. "
        "For each player, the model estimates the probability of each involvement type using goals scored "
        "whilst that player was on the pitch."
    )
    st.write("Clean sheets are estimated directly from the match-level model.")
    st.write(
        "Expected points is then modelled as conditional on the sum of the player's goal contributions, "
        "clean sheets, and the random effect, after accounting for the different points for each event by position."
    )
    st.write("A stylised DAG for the model is shown below.")

    st.image("/Users/toby/Dev/lionel-app/data/Flowchart.png")
    st.subheader("Predictions")

    st.write(
        "After building the model, it is used simulate team and player outcomes. For example, the plot below shows the "
        "distribution of scores for Man City v Arsenal on Sunday 22nd September 2024. The results seem intuitive: both "
        "are strong defensive teams, and the model predicts a low-scoring game."
        ""
    )
    # st.image("/Users/toby/Dev/lionel-app/data/Screenshot 2024-09-18 at 14.02.26.png")
    st.write("**Man City v Arsenal: Posterior Predictive Distribution of Scorelines**")
    st.plotly_chart(build_scoreline_plot(get_ars_city(), "Manchester City", "Arsenal"))

    # st.write("**Posterior Predictive Distribution of FPL Points**")
    st.write(
        "Conditional on these scorelines, player points are simulated. The plot below shows the "
        "posterior predictive distribution of points for four key players for Arsenal and Man City in their upcoming game. "
        "The predictions seem reasonable: Saka and Haaland are predicted to score a good number of points, but "
        "the game is expected to be low scoring. The defenders have a double-peaked distribution of points, reflecting "
        "that their main source of points is clean sheets, which is a binary outcome for the match."
    )
    st.write("**Man City v Arsenal: Posterior Predictive Distribution of Points**")
    st.image("/Users/toby/Dev/lionel-app/data/plot_posterior.png")

    st.write(
        "Predictions for scorelines from the match-level model for the next gameweek can be seen on the [Scoreline Predictions](/Scoreline_Predictions) page. "
        "Inference on player goal/assist probabilities and team strengths can be seen on the [Inference](/Inference) page."
    )


def body_optimisation():
    st.subheader("Team Selection")
    st.write(
        "The team selection problem is formulated as a linear programming problem. The objective is to maximise "
        "expected points subject the various team, position, and cost constraints of the FPL game. "
    )
    st.write(
        "This is solved using the [PuLP](https://coin-or.github.io/pulp/) Python library."
    )


def body_notes():
    st.subheader("Reproducibility")
    st.write(
        "The code for lionel is openly available at [jth500/lionel](https://github.com/jth500)."
        " FPL data prior to 2024-25 is sourced from [Vaastav](https://github.com/vaastav/Fantasy-Premier-League)."
    )


if __name__ == "__main__":
    st.set_page_config(
        page_title="lionel - About",
    )
    body_model()
    body_optimisation()
    body_notes()

from pathlib import Path
import pandas as pd
import streamlit as st
from plot_team import create_plot, create_value_plot
from utils import setup_logger


# Config
logger = setup_logger(__name__)
logger.debug("Running from top")  # just useful to undserstand the order of execution
st.set_page_config(
    page_title="lionel-app",
)


# Set up a callback for the prediction variable
def initialise_session_vars():
    if "pred_var" not in st.session_state:
        # logger.debug("Initialising messages")
        st.session_state.pred_var = "Naive"


def main():
    st.title("lionel FPL Selector 🦁")

    with st.expander("More about lionel"):
        st.write(
            "lionel is a [Fantasy Premier League](https://github.com/jth500/maet-pln) team"
            " optimisation tool that uses machine learning to predict player performance."
        )
        st.write(
            "It is built using four models: 1) a naive model, 2) a LightGBM"
            "regressor without exogenous variables, 3) a LightGBM regressor "
            "with exogenous variables, and 4) an LSTM model with ReLU activation."
        )

    tab1, tab2 = st.tabs(["🤖 Team Selection", ":chart: Team Forecasts and Values"])
    with tab1:
        st.subheader("Team Selections for Gameweek 1")
        st.plotly_chart(create_plot(25, 1, pred_var=str(st.session_state.pred_var)))

    with tab2:
        st.subheader("Team Forecasts and Values for Gameweek 1")
        st.plotly_chart(
            create_value_plot(25, 1, pred_var=str(st.session_state.pred_var))
        )


def sidebar():
    pred_vars = [
        "Naive",
        "LGBMRegressor_no_exog",
        # "LGBMRegressor_with_exog",
        "LSTMWithReLU",
    ]
    with st.sidebar:
        st.title("Choose a Model")
        st.session_state.pred_var = st.radio(
            "Prediction variable",
            pred_vars,
        )
        st.write(
            "Naive Model: Predicts a player's future "
            "performance by assuming it will be equal to their most "
            "recent performance data."
        )
        st.write(
            "Light Gradient-Boosting Machine Model: Uses"
            " multiple decision trees to iteratively improve predictions "
            "of a player's performance based on historical data and relevant features."
        )
        st.write(
            "LSTM Model: Uses a recurrent neural "
            "network architecture to capture long-term "
            "patterns in time-series data for predicting a "
            "player's future performance."
        )


## TODO: Use old team chart code to get the new one working.. ideally include a filter for team selection methods

if __name__ == "__main__":
    initialise_session_vars()
    sidebar()
    main()

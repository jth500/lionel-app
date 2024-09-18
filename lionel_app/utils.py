import logging
import pandas as pd
import datetime as dt

# from lionel_app import dbm


def setup_logger(name):
    logging.basicConfig()
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    return logger


def get_gameweek(dbm, season=25):
    today = dt.datetime.today().date()
    df = pd.DataFrame(
        dbm.query(f"SELECT * FROM fixtures WHERE season = {season}").fetchall()
    )
    df = (
        df.groupby("gameweek")
        .agg(
            first_kickoff=("kickoff_time", "min"), last_kickoff=("kickoff_time", "max")
        )
        .reset_index()
    )
    df[["first_kickoff", "last_kickoff"]] = df[["first_kickoff", "last_kickoff"]].apply(
        pd.to_datetime
    )
    next_gameweek = df[df.last_kickoff.dt.date < today].iloc[-1, 0] + 1
    return next_gameweek

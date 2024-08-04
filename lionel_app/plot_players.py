import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from pathlib import Path


def show_player_fig(data, names=[], teams=[], positions=[]):
    df_1 = data.copy()
    if names:
        df_1 = df_1[df_1["name"].isin(names)]
    if teams:
        df_1 = df_1[df_1["team_name"].isin(teams)]
    if positions:
        df_1 = df_1[df_1["position"].isin(positions)]

    l = []
    fig = go.Figure()
    for pred_type in ["y", "y_Naive", "y_LGBMRegressor_no_exog", "y_LSTMWithReLU"]:
        l.append(
            go.Scatter(
                x=[df_1["season"], df_1["gameweek"]],
                y=df_1[pred_type],
                mode="lines",
                line=dict(width=2),
                name=pred_type,
                customdata=df_1[
                    ["name", "team_name", "position", "opponent_team_name"]
                ],
                hovertemplate="<b>%{customdata[0]}</b>"
                + "<br><br><b>Team:</b> %{customdata[1]}"
                + "<br><b>Position:</b> %{customdata[2]}"
                + "<br><b>Opponent:</b> %{customdata[3]}"
                + "<extra></extra>",
            )
        )
    layout = go.Layout(
        legend=dict(orientation="h", x=0, y=1),
        xaxis_title="Season | Gameweek",
        yaxis_title="Points",
    )

    fig = go.Figure(data=l, layout=layout)
    return fig

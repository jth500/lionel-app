import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from pathlib import Path

DATA = Path(__file__).parents[1] / "data"


def _create_pitch():
    line_width = 3
    fig = go.Figure()

    fig.add_vrect(x0=-350, x1=350, line=dict(color="black", width=4))  # width=3

    fig.add_trace(
        go.Scatter(
            x=[-350, 350],
            y=[0, 0],
            marker=dict(size=25, color="black"),
            mode="lines",
            line=dict(color="black", width=line_width),
        )
    )

    fig.add_shape(
        type="circle",
        xref="x",
        yref="y",
        x0=-100,
        y0=-100,
        x1=100,
        y1=100,
        line=dict(color="black", width=line_width - 1),
    )

    fig.add_trace(
        go.Scatter(
            x=[-180, -180, 180, 180],
            y=[
                -550,
                -400,
                -400,
                -550,
            ],
            mode="lines",
            line_color="black",
            showlegend=False,
            line=dict(color="black", width=line_width),
        )
    )

    fig.add_trace(
        go.Scatter(
            x=[-180, -180, 180, 180],
            y=[
                550,
                400,
                400,
                550,
            ],
            mode="lines",
            line_color="black",
            showlegend=False,
            line=dict(color="black", width=line_width),
        )
    )

    fig.update_layout(
        font_family="sans-serif",
        autosize=False,
        width=600,
        height=800,
        yaxis_range=[-550, 550],
        xaxis_range=[-400, 400],
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )

    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)
    return fig


def _plot_players(first_xi, position, fig):
    df = first_xi.loc[first_xi.position == position]

    Y = {"FWD": 350, "MID": 75, "DEF": -250, "GK": -475}

    dims = [-250, 250]
    width = dims[1] - dims[0]

    if len(df) > 1:
        divisor = len(df) - 1
        jump = int(width / divisor)
        X = list(range(dims[0], dims[1] + 1, jump))
    else:
        X = [0]

    fig.add_trace(
        go.Scatter(
            x=X,
            y=[Y[position]] * len(df),
            mode="markers+text",
            marker=dict(size=25, color="black"),
            text=df["name"].str.split().str[-1],
            textposition="bottom center",
            textfont=dict(color="black"),
            textfont_size=10,
            customdata=df[
                [
                    "name",
                    "team_name",
                ]
            ],
            hovertemplate="<b>%{customdata[0]}</b>"
            + "<br><br><b>Team:</b> %{customdata[1]}"
            + "<extra></extra>",
        )
    )

    return fig


def _plot_subs(team, fig, pred_var):

    df = team.loc[team[f"first_xi_{pred_var}"] == 0]

    X = [375] * 4
    Y = [-90, -30, 30, 90]

    fig.add_trace(
        go.Scatter(
            x=X,
            y=Y,
            mode="markers",
            marker=dict(size=25, color="black"),
            text=df["name"].str.split().str[-1],
            textposition="bottom left",
            textfont=dict(color="black"),
            textfont_size=10,
            customdata=df[
                [
                    "name",
                    "team_name",
                ]
            ],
            hovertemplate="<b>%{customdata[0]}</b>"
            + "<br><br><b>Team:</b> %{customdata[1]}"
            + "<extra></extra>",
        )
    )
    return fig


def create_plot(season, next_gw, pred_var="LSTMWithReLU"):

    players = pd.read_csv(DATA / f"team_selection_{next_gw}_{season}.csv")
    players = players.rename(columns={"unique_id": "name"})
    team = players[players[f"picked_{pred_var}"] == 1]
    first_xi = team.loc[team[f"first_xi_{pred_var}"] == 1]

    fig = _create_pitch()
    for pos in ["FWD", "MID", "DEF", "GK"]:
        _plot_players(first_xi, pos, fig)

    fig = _plot_subs(team, fig, pred_var)
    fig.update_layout(
        height=725,
        width=500,
        margin={"t": 10, "b": 0},
    )

    return fig

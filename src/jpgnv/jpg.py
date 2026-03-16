from pathlib import Path
import altair as alt
import polars as pl
from plyze.jpg.interfaces import JPGMetricsRegistry as JR

from jpgnv.plots.components import strip


def plot_jpg_metrics(path: Path):
    # TODO: may be good to verify schema here..
    df = pl.read_csv(path)
    charts = [strip(df, f) for f in JR.feature_nicknames]

    chart = alt.vconcat(*charts)

    return chart


def plot_zone_qois(path: Path):
    # TODO: may be good to verify schema here..
    df = pl.read_csv(path)
    charts = [strip(df, f) for f in JR.feature_nicknames]

    chart = alt.vconcat(*charts)

    return chart


# BOX_MULLER_TRANSFORM = "sqrt(-2*log(random()))*cos(2*PI*random())"
# UNIFORM_TRANSFORM = "random()"
#
#
# def point(df: pl.DataFrame, feature: str):
#     chart = (
#         alt.Chart(df)
#         .mark_point()
#         .encode(x=alt.X(f"{feature}:Q").scale(zero=False))
#         .properties(width=500, height=250)
#     )
#     return chart
#
# def jitter(df: pl.DataFrame, feature: str):
#     chart = (
#         point(df, feature)
#         .encode(yOffset="jitter:Q")
#         .transform_calculate(jitter=UNIFORM_TRANSFORM)
#     )
#     return chart
#
# def strip(df: pl.DataFrame, feature: str):
#     chart = (
#         alt.Chart(df)
#         .mark_tick()
#         .encode(x=alt.X(f"{feature}:Q").scale(zero=False))
#         .properties(width=500, height=80)
#     )
#     return chart
#
#
#
#
# def read_csv(path: Path):
#     return pl.read_csv(path)
#
#
def read_parquet(path: Path):
    return pl.read_parquet(path)

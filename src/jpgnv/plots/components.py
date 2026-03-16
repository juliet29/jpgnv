from dataclasses import dataclass
from pathlib import Path
import altair as alt
import polars as pl
from typing import Callable

BOX_MULLER_TRANSFORM = "sqrt(-2*log(random()))*cos(2*PI*random())"
UNIFORM_TRANSFORM = "random()"
HEIGHT = 80
TALL_HEIGHT = 250
WIDTH = 500


def point(df: pl.DataFrame, feature: str):
    chart = (
        alt.Chart(df)
        .mark_point()
        .encode(x=alt.X(f"{feature}:Q").scale(zero=False))
        .properties(width=WIDTH, height=HEIGHT)
    )
    return chart


def jitter(df: pl.DataFrame, feature: str):
    chart = (
        point(df, feature)
        .encode(yOffset="jitter:Q")
        .transform_calculate(jitter=UNIFORM_TRANSFORM)
    )
    return chart


def strip(df: pl.DataFrame, feature: str):
    chart = (
        alt.Chart(df)
        .mark_tick()
        .encode(x=alt.X(f"{feature}:Q").scale(zero=False))
        .properties(width=WIDTH, height=HEIGHT)
    )
    return chart


def histogram(df: pl.DataFrame, feature: str):
    chart = (
        alt.Chart(df)
        .mark_bar()
        .encode(
            x=alt.X(f"{feature}:Q").bin().scale(zero=False),
            y=alt.Y("count()").title("Count"),
        )
        .properties(width=WIDTH, height=HEIGHT)
    )
    return chart


PLOT1D = Callable[[pl.DataFrame, str], alt.Chart]


@dataclass
class FacetFeature:
    path: Path
    features: list[str]

    def get_df(self):
        if self.path.suffix == ".csv":
            self.df = pl.read_csv(self.path)
        else:
            self.df = pl.read_parquet(self.path)

    def vplot(self, plotfx: PLOT1D = strip):
        charts = [plotfx(self.df, f) for f in self.features]
        return alt.vconcat(*charts)

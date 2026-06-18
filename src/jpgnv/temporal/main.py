from pathlib import Path
import altair as alt
from loguru import logger
from jpgnv.plots.corr import simple_corr, simple_line
from jpgnv.plots.components import histogram_nom
import polars as pl


# import pandera as pa
#
# def polars_to_pandera(schema: pl.Schema) -> pa.DataFrameSchema:
#     # Map Polars types to Pandera/Python types
#     type_map = {
#         pl.String: str,
#         pl.Int64: int,
#         pl.Int32: int,
#         pl.Float64: float,
#         pl.Boolean: bool,
#         pl.Date: pl.Date,
#         pl.Datetime: pl.Datetime,
#     }
#
#     columns = {
#         name: pa.Column(type_map.get(type(dtype), dtype))
#         for name, dtype in schema.items()
#     }
#
#     return pa.DataFrameSchema(columns)
#
# PASchema = polars_to_pandera(schema)
#

DRN = "DRN of max unique_wind_pressure"


def max_pressure_plots(path: Path):
    # df = pl.read_csv(path).filter(pl.col("case_name").cast(pl.Int32))
    df = pl.read_csv(path).filter(pl.col("wind_direction") > 353)

    logger.debug(df.height)

    c1 = simple_corr(df, "t_out", "temp")
    c2 = simple_corr(df, "t_out", "mix_vol")
    c3 = simple_corr(df, "wind_speed", "mix_vol")
    c4 = simple_corr(df, "hours(datetimes)", "temp")

    charts = alt.HConcatChart()
    for c in [c1, c2, c3, c4]:
        charts |= c.encode(color=alt.Color(DRN, type="nominal"))

    return charts


def plot_over_day(path: Path):

    df = pl.read_csv(path).filter(pl.col("case_name").cast(pl.Int32) < 6000)
    f1 = "hours(datetimes)"
    f2 = "mean(temp)"
    chart = (
        alt.Chart(df)
        .mark_line()
        .encode(
            x=alt.X(f1, type="quantitative").scale(zero=False),
            y=alt.Y(f2, type="quantitative").scale(zero=False),
            color=alt.Color("case_name", type="nominal"),
        )
        .properties(width=150, height=150)
        .interactive()
    )
    return chart


def calculate_case_dominant_wind_pressure(arr: pl.Series):
    return (arr.value_counts(sort=True).select(pl.col(DRN).max_by("count").first()))[
        DRN
    ].to_list()[0]


def case_max_wind_pressure_drn(path: Path):
    SEED = 12345

    df = pl.read_csv(path)
    cases = df["case_name"].sample(16, seed=SEED)
    dff = df.filter(pl.col("case_name").is_in(cases)).sort(by=pl.col("case_name"))

    c = histogram_nom(dff, DRN, "Drn of Max Pressure").facet(
        facet="case_name", columns=4
    )
    return c


def dom_plot(df: pl.DataFrame):
    logger.debug(df.height)

    # c1 = simple_line(df, "t_out", "temp")
    # c2 = simple_line(df, "t_out", "mix_vol")
    # c3 = simple_line(df, "wind_speed", "mix_vol")
    c4 = simple_line(df, "hours(datetimes)", "mean(temp)")
    c3 = simple_line(df, "hours(datetimes)", "mean(mix_vol)")
    c2 = simple_line(df, "hours(datetimes)", "mean(vent_vol)")

    charts = alt.HConcatChart()
    for c in [c2, c3, c4]:
        charts |= c.encode(
            color=alt.Color("main_drn", type="nominal"),
            strokeDash=alt.StrokeDash("case_name", type="nominal").legend(None),
            row=alt.Row("monthdate(datetimes)"),
        )

    return charts


def calc_maxes(path):
    SEED = 12345

    df = pl.read_csv(path)
    cases = df["case_name"].sample(32, seed=SEED)
    dff = df.filter(pl.col("case_name").is_in(cases)).sort(by=pl.col("case_name"))

    ndict = {}
    for case_row, data in dff.group_by("case_name"):
        case = case_row[0]

        res = calculate_case_dominant_wind_pressure(data.get_column(DRN))
        logger.debug(res)
        ndict[case] = res

    logger.debug(ndict)
    ndf = pl.from_dict(
        data={"case_name": ndict.keys(), "main_drn": ndict.values()}
    )  # pyright: ignore[reportArgumentType]

    logger.debug(ndf)

    fdf = dff.join(ndf, on="case_name")
    logger.debug(fdf)
    return dom_plot(fdf)

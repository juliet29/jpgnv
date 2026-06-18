import polars as pl
import altair as alt


def scatter_matrix(df: pl.DataFrame, features: list[str]):
    return (
        alt.Chart(df)
        .mark_circle()
        .encode(
            alt.X(alt.repeat("column"), type="quantitative").scale(zero=False),
            alt.Y(alt.repeat("row"), type="quantitative").scale(zero=False),
        )
        .properties(width=150, height=150)
        .repeat(
            row=features,
            column=features,
        )
        # .transform_filter(
        #     # Filter: only show row index > column index
        #     f"indexof({features}, datum['row']) > indexof({features}, datum['column'])"
        # )
    )


def simple_corr(df, f1: str, f2: str):
    return (
        alt.Chart(df)
        .mark_circle()
        .encode(
            x=alt.X(f1, type="quantitative").scale(zero=False),
            y=alt.Y(f2, type="quantitative").scale(zero=False),
        )
        .properties(width=150, height=150)
        .interactive()
    )


def simple_line(df, f1: str, f2: str):
    return (
        alt.Chart(df)
        .mark_line()
        .encode(
            x=alt.X(f1, type="quantitative").scale(zero=False),
            y=alt.Y(f2, type="quantitative").scale(zero=False),
        )
        .properties(width=250, height=250)
        .interactive()
    )


def simple_line_with_error(df, f1: str, f2: str):

    x = alt.X(f1, type="quantitative").scale(zero=False)
    y_mean = alt.Y(f"mean({f2})", type="quantitative").scale(zero=False)
    y = alt.Y(f2, type="quantitative").scale(zero=False)

    line = alt.Chart(df).mark_line().encode(x, y_mean)

    band = alt.Chart(df).mark_errorband(extent="ci").encode(x, y)
    c = (band + line).properties(width=250, height=250)
    return c

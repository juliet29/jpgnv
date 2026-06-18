from datetime import datetime
import matplotlib.pyplot as plt
import polars as pl
from cyclopts import App
from loguru import logger
from jpgnv.cluster.main import apply_kmeans
from jpgnv.jpg import read_parquet, strip
from jpgnv.paths import ProjectPaths
from utils4plans.logconfig import logset

from plyze.plots.altair_helpers import AltairRenderers
from plyze.plots.theme import default_theme
from plyze.qoi.registries.main import QOIRegistry as QR
from plyze.jpg.interfaces import JPGMetricsRegistry as JR
import altair as alt

from jpgnv.plots.components import FacetFeature, strip, jitter, point, histogram
from jpgnv.plots.corr import scatter_matrix, simple_corr
from jpgnv.temporal.main import (
    calc_maxes,
    max_pressure_plots,
)

app = App()


def keep():
    default_theme()
    logger.debug("")
    strip, jitter, point, histogram  # pyright: ignore[reportUnusedExpression]
    plt.plot()


### ----- DATA --------
@app.command()
def j():
    ff = FacetFeature(ProjectPaths.jpg_metrics, JR.feature_nicknames)
    ff.get_df()
    c = ff.vplot(histogram)
    c.show()


@app.command()
def q():

    df = (
        read_parquet(ProjectPaths.zonal_qoi)
        .group_by("case_name")
        .agg(pl.col(i).mean() for i in QR.zonal_feature_nicknames)
    )

    ff = FacetFeature(ProjectPaths.zonal_qoi, QR.zonal_feature_nicknames)
    ff.df = df
    c = ff.vplot(histogram) | ff.vplot(strip)
    c.show()


@app.command()
def qc():

    dt = datetime(2017, 7, 1, 12, 0)
    df = (
        read_parquet(ProjectPaths.zonal_qoi)
        .filter(pl.col("datetimes") == dt)
        .group_by("case_name")
        .agg(pl.col(i).mean() for i in QR.zonal_feature_nicknames)
    )
    c = scatter_matrix(df, QR.zonal_feature_nicknames)
    c.show()


@app.command()
def qj():
    dt = datetime(2017, 7, 1, 12, 0)
    df = (
        read_parquet(ProjectPaths.zonal_qoi)
        .filter(pl.col("datetimes") == dt)
        .group_by("case_name")
        .agg(pl.col(i).mean() for i in QR.zonal_feature_nicknames)
    )
    dfj = pl.read_csv(ProjectPaths.jpg_metrics)
    dfj2 = dfj.rename(mapping={"graph_name": "case_name"}).cast(
        {"case_name": pl.String}
    )
    jdf = dfj2.join(df, on="case_name")
    c1 = simple_corr(jdf, JR.mean_depth.nickname, QR.mix_heat_loss.nickname)
    c1a = simple_corr(jdf, JR.mean_depth.nickname, QR.mix_vol.nickname)
    c2 = simple_corr(jdf, JR.mean_depth.nickname, QR.vent_heat_loss.nickname)
    c3 = simple_corr(jdf, JR.mean_depth.nickname, QR.vent_vol.nickname)
    c4 = simple_corr(jdf, JR.mean_depth.nickname, QR.custom.net_vent_heat_gain.nickname)
    c5 = simple_corr(jdf, JR.mean_depth.nickname, QR.temp.nickname)
    c = c1 | c1a | c2 | c3 | c4 | c5
    c.show()


### ----- CLUSTERING --------


@app.command()
def meanshift():

    dt = datetime(2017, 7, 1, 12, 0)
    # X = (
    #     read_parquet(ProjectPaths.zonal_qoi)
    #     .filter(pl.col("datetimes") == dt)
    #     .group_by("case_name")
    #     .agg(pl.col(i).mean() for i in QR.zonal_feature_nicknames)
    #     .drop("case_name")
    #     .with_columns(pl.all().round(4))
    #     .to_numpy()
    # )
    # logger.debug(X)
    # return
    X = (
        pl.read_csv(ProjectPaths.jpg_metrics)
        .select(
            JR.mean_depth.nickname,
            # JR.relative_asymmetry.nickname,
            # JR.total_depth.nickname,
        )
        .with_columns(pl.all().round(4))
        .to_numpy()
    )
    data_path = ProjectPaths.cluster.mean_shift / "init" / "data.csv"
    centers_path = ProjectPaths.cluster.mean_shift / "init" / "center.csv"

    apply_kmeans(X, data_path, centers_path)


### ------- Pressure collapse ---------


@app.command()
def pr():
    c = max_pressure_plots(ProjectPaths.temporal.data)
    c.show()


@app.command()
def dt():
    c = calc_maxes(ProjectPaths.temporal.data)
    c.show()


@app.command()
def ca():
    return calc_maxes(ProjectPaths.temporal.data)


### ------- END COMMANDS ---------


def main():
    AltairRenderers.set_renderer()
    alt.theme.enable("default_theme")
    logset(to_stderr=True)
    app()


if __name__ == "__main__":
    main()

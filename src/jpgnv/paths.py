from pathlib import Path
import pyprojroot


BASE_PATH = pyprojroot.find_root(pyprojroot.has_dir(".git"))


class StaticPaths:
    base = Path(BASE_PATH) / "static"
    inputs = base / "1_inputs"
    temp = base / "4_temp"


class Cluster:
    cluster_results = StaticPaths.temp / "cluster"
    mean_shift = cluster_results / "mean_shift"


class ProjectPaths:
    smk_shared_results = StaticPaths.temp / "smk/shared"
    jpg_metrics = smk_shared_results / "metrics/out.csv"
    zonal_qoi = smk_shared_results / "qois/zonal/out.parquet"
    surface_qoi = smk_shared_results / "qois/surface/out.parquet"

    cluster = Cluster

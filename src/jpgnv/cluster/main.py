from pathlib import Path
from sklearn import preprocessing
from loguru import logger
from sklearn.cluster import KMeans, MeanShift, estimate_bandwidth
import numpy as np
import polars as pl


def preprocess(X: np.ndarray):
    scaler = preprocessing.StandardScaler().fit(X)
    logger.info([scaler.mean_, scaler.scale_])
    Xs = scaler.transform(X)
    return Xs


def finish_cluster(model, data_path: Path, clusters_path: Path):
    logger.info(f"Labels unique: {np.unique(model.labels_)}")
    logger.info(model.labels_.shape)

    if len(np.unique(model.labels_)) == 1:
        raise Exception("Failed to distinguish data => only one label")

    df = pl.DataFrame(data={"labels": model.labels_})
    logger.debug(df)

    df.write_csv(data_path)

    try:
        cf = pl.DataFrame(data=model.cluster_centers_)
        logger.debug(cf)
        cf.write_csv(clusters_path)
    except AttributeError:
        pass

    # logger.info(f"Cluster centers: {model.cluster_centers_}")

    # save a csv with the labels


def apply_meanshift(X_: np.ndarray, data_path: Path, clusters_path: Path):
    # use fewer samples than the data to estimate the bandwidth
    X = preprocess(X_)
    bandwidth = estimate_bandwidth(X)
    logger.info(f"Bandwidth estimated: {bandwidth}")

    ms = MeanShift(bandwidth=bandwidth, bin_seeding=False)
    ms.fit(X)

    finish_cluster(ms, data_path, clusters_path)


def apply_kmeans(X_: np.ndarray, data_path: Path, clusters_path: Path):
    X = preprocess(X_)
    kmeans = KMeans(n_clusters=5).fit(X)
    finish_cluster(kmeans, data_path, clusters_path)

    pass

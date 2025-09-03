import numpy as np
import pandas as pd

def freedman_draconis_rule(series: pd.Series) -> int:
    return int((series.max() - series.min()) // \
        (2 * (series.quantile(0.75) - series.quantile(0.25)) * series.shape[0] ** (-1/3)))

def sturges_rule(series: pd.Series) -> int:
    return int(np.ceil(np.log2(series.shape[0]) + 1))
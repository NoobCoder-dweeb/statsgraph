import numpy as np
import pandas as pd
from scipy import stats
from typing import Tuple

def freedman_draconis_rule(series: pd.Series) -> int:
    return int((series.max() - series.min()) // \
        (2 * (series.quantile(0.75) - series.quantile(0.25)) * series.shape[0] ** (-1/3)))

def sturges_rule(series: pd.Series) -> int:
    return int(np.ceil(np.log2(series.shape[0]) + 1))

#---------------------- Statistical Tests ---------------------------------

def t_test(x: pd.Series, y: pd.Series):
    stat, p = stats.ttest_ind(x.dropna(), y.dropna())
    return stat, p

def kendall_tau(x: pd.Series, y: pd.Series):
    tau, p = stats.kendalltau(x.dropna(), y.dropna())
    return tau, p

def kurtosis_test(x: pd.Series, y: pd.Series):
    kurt_1 = stats.kurtosis(x.dropna())
    kurt_2 = stats.kurtosis(y.dropna())
    return kurt_1, kurt_2

def spearman_corr(x: pd.Series, y: pd.Series):
    corr, p = stats.spearmanr(x.dropna(), y.dropna())
    return corr, p

def chi2_test(x: pd.Series, y: pd.Series):
    table = pd.crosstab(x, y)
    chi2, p, _, _ = stats.chi2_contingency(table)
    return chi2, p

def fisher_exact_test(x: pd.Series, y: pd.Series):
    table = pd.crosstab(x, y)
    if table.shape == (2, 2):
        odds, p = stats.fisher_exact(table)
        return odds, p
    else:
        return np.nan, np.nan

#---------------------- End of Statistical Tests --------------------------

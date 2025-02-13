import pandas as pd
import numpy as np
import quantstats as qs

def test_factor_performance(df, q = 10, factor = 'close/vwap', returns = 'TmrReturn', reverse = False):

    # Rank stocks by factor value within each date
    df.loc[:, 'Rank'] = df.groupby('Date')[factor].rank(ascending=reverse)

    # Divide stocks into 5 quantiles (e.g., top 20% to bottom 20%)
    df.loc[:, 'Quantile'] = pd.qcut(df['Rank'], q=q, labels=[i for i in range(1, q+1)])

    # Calculate average return for each quantile on each date
    quantile_returns = df.groupby(['Date', 'Quantile'])[returns].mean().unstack()
    #quantile_returns['avg'] = df.groupby('Date')[returns].mean()
    quantile_returns['long-short'] = quantile_returns[1] - quantile_returns[q]
    quantile_returns.cumsum().plot()

    qs.reports.metrics(quantile_returns)
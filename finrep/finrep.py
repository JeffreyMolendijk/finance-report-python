import os
from sre_compile import isstring
import pandas as pd
import yfinance as yf
from itertools import product
import plotly.express as px


def read_File(file_path: str):
    """Flexible file reader for .csv or .xlsx

    Args:
        file_path (str): path to file

    Returns:
        _type_: pandas Dataframe
    """
    if isstring(file_path):
        try:
            if file_path.endswith('.csv'):
                return pd.read_csv(file_path)
            if file_path.endswith('.xlsx'):
                return pd.read_excel(file_path)
        except ValueError:
            return None
    return None


class finance:
    """Finance class containing savings, stock and super subclasses"""

    def __init__(self, savings: str, stocks: str, superannuation: str):
        df_savings = read_File(savings)
        df_savings['type'] = 'savings'
        self.savings = df_savings

        df_superannuation = read_File(superannuation)
        df_superannuation['type'] = 'superannuation'
        self.superannuation = df_superannuation

        df_stocks = read_File(stocks)
        mindate = min(df_savings['date'].min(), df_superannuation['date'].min())
        maxdate = max(df_savings['date'].max(), df_superannuation['date'].max())
        idx = pd.date_range(mindate, maxdate, freq='MS')
        idx_df = pd.DataFrame({'date': idx})
        stocks_range = idx_df.merge(df_stocks, how='left')
        stocks_range = stocks_range[['date', 'stock', 'units']]
        tickers = stocks_range['stock'].dropna().unique()
        outlist = list(product(stocks_range['date'].unique(), tickers))
        stocks_range = pd.DataFrame(data=outlist, columns=['date', 'stock']).merge(
            stocks_range, on=['date', 'stock'], how='left')
        stocks_range['units'] = stocks_range['units'].fillna(0)
        stocks_range['unitsum'] = stocks_range.groupby(['stock']).cumsum()
        stocks_range = stocks_range.drop('units', axis=1)
        hist = yf.download(list(tickers), start=mindate, end=maxdate, interval='1mo')

        res = []
        for ticker in tickers:
            res.append(pd.DataFrame({'date': hist.index,
                                    'price': hist['Open'][ticker].values,
                                    'stock': ticker}).reset_index(drop=True))
        stocks_range = stocks_range.merge(pd.concat(res), on=['date', 'stock'], 
                                            how='left')
        stocks_range['value'] = stocks_range['unitsum'] * stocks_range['price']
        self.stocks = stocks_range

    def __validate_pandas(self):
        """Validate whether loaded data is valid

        Returns:
            _type_: boolean
        """
        if len(self.savings) == 2 and \
            len(self.superannuation) == 2 and \
            len(self.stocks) == 4:
            return True 
        return False

    def get_portfolio(self):
        """Generates portfolio summary with monthly values

        Returns:
            _type_: pandas DataFrame
        """
        stockval = self.stocks[['date', 'value', 'stock']].rename(columns={
            'value': 'amount', 'stock': 'type'})
        portfolio_total = pd.concat([self.savings, self.superannuation, stockval])
        return portfolio_total

    def show_portfolio(self):
        """Generates a plotly object showing portfolio distribution

        Returns:
            _type_: plotly object
        """
        fig = px.bar(self.get_portfolio(), x="date", y="amount", color="type", 
                        title="Portfolio distribution")
        return fig

    def forecast(self, months_predict: int):
        print(f'In {months_predict} months you will have infinite money!')

    def optimize_portfolio():
        pass  # tweak contribution parameters to determine optimum


def main():
    """Contains example analysis code"""
    portfolio = finance(savings=os.path.join('data', 'savings.xlsx'),
                        stocks=os.path.join('data', 'stocks.xlsx'),
                        superannuation=os.path.join('data', 'super.xlsx'))

    print(portfolio.get_portfolio())
    print(type(portfolio.show_portfolio()))
    portfolio.show_portfolio().show()


if __name__ == "__main__":
    main()

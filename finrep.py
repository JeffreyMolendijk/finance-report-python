from lib2to3.pgen2.pgen import DFAState
import os
from sqlite3 import Timestamp
from sre_compile import isstring
import pandas as pd
from datetime import date, datetime
import yfinance as yf
from itertools import product



def read_File(input: str):
    """Flexible file reader for .csv or .xlsx

    Args:
        input (str): path to file

    Returns:
        _type_: pandas Dataframe
    """
    if isstring(input):
        try:
            if input.endswith('.csv'): return pd.read_csv(input)
            if input.endswith('.xlsx'): return pd.read_excel(input)
        except:
            print('failed to load file from string')    



class finance:
    """Finance class containing savings, stock and super subclasses
    """
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
        stocks_range = idx_df.join(df_stocks, rsuffix='original')
        stocks_range = stocks_range[['date', 'stock', 'units']]
        tickers = stocks_range['stock'].dropna().unique()
        outlist = list(product(stocks_range['date'], tickers))
        stocks_range = pd.DataFrame(data=outlist, columns=['date','stock']).merge(stocks_range, how='left')
        stocks_range['units'] = stocks_range['units'].fillna(0)
        stocks_range['unitsum'] = stocks_range.groupby(['stock']).cumsum()
        stocks_range = stocks_range.drop('units', axis=1)
        hist = yf.download(list(tickers), start=mindate, end=maxdate, interval='1mo')
        res = []
        for ticker in tickers:
            res.append(pd.DataFrame({'date': hist.index, 'price': hist['Open'][ticker].values, 'stock': ticker}).reset_index(drop=True))
        stocks_range = stocks_range.merge(pd.concat(res), on=['date','stock'], how = 'left')
        stocks_range['value'] = stocks_range['unitsum'] * stocks_range['price']
        self.stocks = stocks_range
        
    def __validate_pandas(unvalidated_pandas, type: str):
        if type == 'savings': return True 
        
    def show_portfolio(self):
        return self.savings.merge(self.superannuation, on = 'date')
        
    def forecast(self, months_predict: int):
        print(f'In {months_predict} months you will have infinite money!')
    
    def optimize_portfolio():
        pass # tweak contribution parameters to determine optimum
    
    def percentage_portfolio():
        pass # calculate distribution of portfolio



def main():
    portfolio = finance(savings=os.path.join('data', 'savings.xlsx'), 
                    stocks=os.path.join('data', 'stocks.xlsx'), 
                    superannuation=os.path.join('data', 'super.xlsx'))
                    
    portfolio.forecast(10)
    print(portfolio.show_portfolio())
    print(portfolio.stocks)


if __name__ == "__main__":
    main()

# TODO: integrate results with Preset (Apache superset) or another dashboard
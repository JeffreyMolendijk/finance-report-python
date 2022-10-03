from finrep.finrep import read_File, finance
import pandas as pd
import plotly
import os

def test_read_File():
    assert isinstance(read_File(os.path.join('data', 'savings.xlsx')), pd.DataFrame), 'Is not a dataframe'

def test_finance():
    portfolio = finance(savings=os.path.join('data', 'savings.xlsx'),
                        stocks=os.path.join('data', 'stocks.xlsx'),
                        superannuation=os.path.join('data', 'super.xlsx'))
    assert isinstance(portfolio.savings, pd.DataFrame), 'savings is not a dataframe'
    assert isinstance(portfolio.stocks, pd.DataFrame), 'stocks is not a dataframe'
    assert isinstance(portfolio.superannuation, pd.DataFrame), 'savings is not a dataframe'

def test_get_portfolio():
    portfolio = finance(savings=os.path.join('data', 'savings.xlsx'),
                        stocks=os.path.join('data', 'stocks.xlsx'),
                        superannuation=os.path.join('data', 'super.xlsx'))
    assert isinstance(portfolio.get_portfolio(), pd.DataFrame), 'get_portfolio() should return a dataframe'

def test_show_portfolio():
    portfolio = finance(savings=os.path.join('data', 'savings.xlsx'),
                        stocks=os.path.join('data', 'stocks.xlsx'),
                        superannuation=os.path.join('data', 'super.xlsx'))
    assert isinstance(portfolio.show_portfolio(), plotly.graph_objs._figure.Figure), 'show_portfolio() should return a plotly object'

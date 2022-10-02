from finrep.finrep import read_File, finance
import pandas as pd
import os

def test_sum():
    assert sum([1, 2, 3]) == 6, 'Should be 6'

def test_read_File():
    assert isinstance(read_File(os.path.join('data', 'savings.xlsx')), pd.DataFrame), 'Is not a dataframe'

def test_finance():
    portfolio = finance(savings=os.path.join('data', 'savings.xlsx'), 
                stocks=os.path.join('data', 'stocks.xlsx'), 
                superannuation=os.path.join('data', 'super.xlsx'))
    assert isinstance(portfolio.savings, pd.DataFrame), 'savings is not a dataframe'
    assert isinstance(portfolio.stocks, pd.DataFrame), 'stocks is not a dataframe'
    assert isinstance(portfolio.superannuation, pd.DataFrame), 'savings is not a dataframe'

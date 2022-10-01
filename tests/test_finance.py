from finrep.finrep import read_File
import pandas as pd
import os

def test_sum():
    assert sum([1, 2, 3]) == 6, 'Should be 6'

def test_read_File():
    assert isinstance(read_File(os.path.join('data', 'savings.xlsx')), pd.DataFrame), 'Is not a dataframe'
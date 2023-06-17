import pandas as pd
import csv
import mysql.connector
from CRmatcher import ColMatcher, RowMatcher

class CSVMatcher:
    def __init__(self):
        self.RowMatcher = RowMatcher()
        self.ColMatcher = ColMatcher()

    def Row_Matcher(self, output_csv, primary_column, foreign_column, primary_file, foreign_file):
        primary = pd.read_csv(primary_file)
        foreign = pd.read_csv(foreign_file)
        result = self.RowMatcher.find(output_csv, primary_column, foreign_column, primary, foreign)
        return result
    # def Col_Matcher()
        
        
# class DBMatcher:
#     def __init__(self, config):
#         self.host = config['host']
#         self.user = config['user']
#         self.passwd = config['passwd']
    
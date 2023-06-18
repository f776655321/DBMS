import pandas as pd
import csv
import mysql.connector
from utili import ColMatcher, RowMatcher

class CSVMatcher:
    def __init__(self):
        self.RowMatcher = RowMatcher()
        self.ColMatcher = ColMatcher()

    def Match(self, output_csv, primary_file, foreign_file, primary_column, flag, foreign_column = None, find_col = 1):
        primary = pd.read_csv(primary_file)
        foreign = pd.read_csv(foreign_file)
        # Need ColMatcher
        if(foreign_column == None):
            foreign_column = self.ColMatcher.get_column_matching(primary, foreign, primary_column, find_col)
            result = self.RowMatcher.find(output_csv, primary_column, foreign_column, primary, foreign, flag)
        # Not Need ColMatcher
        else:
            result = self.RowMatcher.find(output_csv, primary_column, foreign_column, primary, foreign, flag)
        result = result.drop('concat', axis=1)
        return result
    
class DBMatcher:
    def __init__(self, config):
        self.host = config['host']
        self.user = config['user']
        self.passwd = config['passwd']
        self.RowMatcher = RowMatcher()
        self.ColMatcher = ColMatcher()

    def Match(self, output_csv, primary_db, foreign_db, primary_table, foreign_table,  primary_column, foreign_column = None, find_col = 1):
        
        connector = mysql.connector.connect(host = self.host, user = self.user, passwd = self.passwd)
        cursor = connector.cursor()
        cursor.execute(f'USE {primary_db}')
        cursor.execute(f'SELECT * FROM {primary_table}')
        column_names = [desc[0] for desc in cursor.description]
        data = cursor.fetchall()
        primary =  pd.DataFrame(data, columns=column_names)

        cursor.execute(f'USE {foreign_db}')
        cursor.execute(f'SELECT * FROM {foreign_table}')
        column_names = [desc[0] for desc in cursor.description]
        data = cursor.fetchall()
        foreign =  pd.DataFrame(data, columns=column_names)

        cursor.close()
        connector.close()

        # Need ColMatcher
        if(foreign_column == None):
            foreign_column = self.ColMatcher.get_column_matching(primary, foreign, primary_column, find_col)
            result = self.RowMatcher.find(output_csv, primary_column, foreign_column, primary, foreign)
        # Not Need ColMatcher
        else:
            result = self.RowMatcher.find(output_csv, primary_column, foreign_column, primary, foreign)
        result = result.drop('concat', axis=1)
        return result

    
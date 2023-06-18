from CRmatcher import CSVMatcher
import os
import statistics
import pandas as pd

def get_data(input_data_dir, benchmark, case):
    with open(os.path.join(input_data_dir,benchmark,case,'rows.txt'), 'r') as file:
        i = 0
        
        for line in file:
            if( i == 0):
                line = line.strip('\n').split(':')
                src_col = line[0]
                target_col = line[1]

                i += 1

            else:
                
                direction = line

    if(direction == 'source'):
        foreign_file = os.path.join(input_data_dir,benchmark,case,'source.csv')
        foreign_key = src_col
        primary_key = target_col
        primary_file = os.path.join(input_data_dir,benchmark,case,'target.csv')
        flag = 1
    else:
        foreign_file = os.path.join(input_data_dir,benchmark,case,'target.csv')
        foreign_key = target_col
        primary_key = src_col
        primary_file = os.path.join(input_data_dir,benchmark,case,'source.csv')
        flag = 2

    return foreign_file, foreign_key, primary_key, primary_file, flag

benchmark = 'autojoin-Benchmark'
folder = f'./data/{benchmark}'
CSV = CSVMatcher()

P = []
R = []
F1 = []
for topic in os.listdir(folder):
  foreign_file, foreign_column, primary_column, primary_file, flag = get_data('./data', benchmark, topic)
  
  predict = CSV.Match(True, primary_file, foreign_file, primary_column, flag, foreign_column)
  golden = pd.read_csv(f'./data/{benchmark}/{topic}/ground truth.csv')
  print(predict.columns)
  
  _P = matched/len(predict_rows)
  _R = matched/len(golden_rows)
  _F1 = 2 * _P * _R / (_P + _R)
  print(_P, _R, _F1)
  P.append(_P)
  R.append(_R)
  F1.append(_F1)

print("average P: ", statistics.mean(P))
print("average Q: ", statistics.mean(Q))
print("average F1: ", statistics.mean(F1))
  
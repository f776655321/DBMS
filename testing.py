from column_matcher import column_matcher

import DataLoader as dl
import Matcher as matcher
import pathlib
import math
import sys


BASE_PATH = str(pathlib.Path(__file__).absolute().parent.parent.absolute())
DS_PATH = './data/autojoin-Benchmark/'

def get_qgrams(q,s):
    res = set()
    assert q > 0
    if q > len(s):
        return res
    if q == len(s):
        res.add(s)
        return res

    end = len(s) - q + 1

    for i in range(end):
        res.add(s[i:i+q])

    return res

def get_count_matching_q_grams(q, src_set, target_set):
    cnt = 0
    for src in src_set:
        src_qgrams = get_qgrams(q, src)
        for t in target_set:
            t_qgrams = get_qgrams(q, t)
            if not src_qgrams.isdisjoint(t_qgrams):
                cnt += 1
                break

    return cnt


def get_column_matching(src_table, target_table, src_specified_column, src_keys_ratio=0.05, tgt_keys_ratio=0.05, q=5, matching_ratio=0.5):
    res = []
    print(src_table['titles'])
    if src_specified_column in src_table['titles']:
        index = src_table['titles'].index(src_specified_column)
    
    col_src = [src_table['items'][j][index].lower() for j in range(len(src_table['items']))]
    # print(col_src)
    dup_src = len(col_src) - len(set(col_src))
    if dup_src > math.ceil(src_keys_ratio * len(col_src)):
        return "I don't know"
    num_tgt_cols = len(target_table['titles'])
    for k in range(num_tgt_cols):
        col_tgt = [target_table['items'][j][k].lower() for j in range(len(target_table['items']))]
        dup_tgt = len(col_tgt) - len(set(col_tgt))
        if dup_tgt > math.ceil(tgt_keys_ratio * len(col_tgt)):
            continue

        cnt = get_count_matching_q_grams(q, col_src, col_tgt)
        # print(cnt)
        if cnt > len(col_src) * matching_ratio:
            res.append({
                'src_table': src_table['name'],
                'src_row': src_table['titles'][index],
                'src_row_id': index,
                'target_table': target_table['name'],
                'target_row': target_table['titles'][k],
                'target_row_id': k,
            })

    return {
        'items': res,
        'bidi': True,
    }

def files_to_tables(file):
    res = {
        'src': {'name': 'src_'+file, 'titles': None, 'items': []},
        'target': {'name': 'target_'+file, 'titles': None, 'items': []},
        'name': file
    }
    with open(file, encoding='UTF8') as f:
        res['src']['titles'] = f.readline().strip().split(',')
        res['src']['items'] = [line.strip().split(',') for line in f.readlines()]
    
    return res['src']
    
args = sys.argv[:]
primary_file = args[1]
foreign_file = args[2]

fileA = files_to_tables(primary_file)
fileB = files_to_tables(foreign_file)
# print()
# lst = []
# tables, all_tables = dl.get_tables_from_dir(DS_PATH, lst, make_lower=True, verbose=False)
# print("Reading Done!")
# a = get_column_matching(all_tables[2], all_tables[3], 'Time in Office')
# print(a)
# print(all_tables[4])
my_col_matcher = column_matcher()
target_column = my_col_matcher.get_column_matching(fileA, fileB, "Governor")
print(target_column)
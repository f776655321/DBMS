import pathlib
import math
import sys

class column_matcher():
    def __init__(self, q_start=5, q_end=10, src_keys_ratio=0.5, matching_ratio=0.5):
        self.q_start = q_start
        self.q_end = q_end
        self.src_keys_ratio = src_keys_ratio
        self.matching_ratio = matching_ratio
        
        return

    def get_qgrams(self, q, s):
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
    
    def files_to_tables(self, fileA, fileB):
        tables = []
        files = [fileA, fileB]
        for file in files:
            res = {
            'src': {'name': 'src_'+file, 'titles': None, 'items': []},
            'target': {'name': 'target_'+file, 'titles': None, 'items': []},
            'name': file
            }
            with open(file, encoding='UTF8') as f:
                res['src']['titles'] = f.readline().strip().split(',')
                res['src']['items'] = [line.strip().split(',') for line in f.readlines()]
            tables.append(res['src'])
        return tables
    
    def get_count_matching_q_grams(self, q, src_set, target_set):
        cnt = 0
        for src in src_set:
            src_qgrams = self.get_qgrams(q, src)
            for t in target_set:
                t_qgrams = self.get_qgrams(q, t)
                if not src_qgrams.isdisjoint(t_qgrams):
                    cnt += 1
                    break

        return cnt
    
    def get_column_matching(self, src_table, target_table, src_specified_column, ):
        res = []
        print(f'Column matching!\nsrc_table: {src_table["name"]}\nsrc_column: {src_specified_column}\ntgt_table: {target_table["name"]}\ntgt_columns: {target_table["titles"]}\n')
        if src_specified_column in src_table['titles']:
            index = src_table['titles'].index(src_specified_column)
        else:
            return "The src_specified_column not in the src_table"
    
        col_src = [src_table['items'][j][index].lower() for j in range(len(src_table['items']))]
        dup_src = len(col_src) - len(set(col_src))
        if dup_src > math.ceil(self.src_keys_ratio * len(col_src)):
            print("Caution: There are a few duplicate rows in the source table, the assigned column might not be the primary key.")
        
        column_cnt = list()
        num_tgt_cols = len(target_table['titles'])
        for k in range(num_tgt_cols):
            col_tgt = [target_table['items'][j][k].lower() for j in range(len(target_table['items']))]
            dup_tgt = len(col_tgt) - len(set(col_tgt))
            print(f'Column "{target_table["titles"][k]}":\nratio of duplicate rows = {dup_tgt/len(col_tgt):.3f}')

            cnt_list = list()
            for q in range(self.q_start, self.q_end):
                cnt = self.get_count_matching_q_grams(q, col_src, col_tgt)
                cnt_list.append((cnt, q))
                print(f'    q={q}: {cnt/len(col_src)*self.matching_ratio}')
        
            max_cnt, max_q = max(cnt_list)
            column_cnt.append((max_cnt, max_q))

        idx = column_cnt.index(max(column_cnt))
        print(f'Find the best target column: {target_table["titles"][idx]} with q={column_cnt[idx][1]}')
        res.append({
            'src_table': src_table['name'],
            'src_row': src_table['titles'][index],
            'src_row_id': index,
            'target_table': target_table['name'],
            'target_row': target_table['titles'][idx],
            'target_row_id': idx,
        })
        
        return src_specified_column, res[0]['target_row']
    
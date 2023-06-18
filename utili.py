import pandas as pd
import torch
from sentence_transformers import SentenceTransformer
from tqdm import tqdm
import numpy as np
import time

class RowMatcher:
    def __init__(self):

        cuda_available = torch.cuda.is_available()

        self.device = torch.device("cuda" if cuda_available else "cpu")

        self.model = SentenceTransformer('sentence-transformers/gtr-t5-large').to(self.device)

    def find(self, output_file, primary_column, foreign_column, primary, foreign, flag, thershold = 0.6, difference = 0.24):

        if(type(foreign_column) == type('')):
            foreign_column = [foreign_column]
        if(type(primary_column) == type('')):
            primary_column = [primary_column]

        foreign['concat'] = foreign[foreign_column].apply(lambda row: ' '.join(row.values.astype(str)), axis=1)
        primary['concat'] = primary[primary_column].apply(lambda row: ' '.join(row.values.astype(str)), axis=1)

        f_column_data = foreign['concat'].values
        p_column_data = primary['concat'].values

        temp_predict = []
        store = []

        for index,f_column in tqdm(enumerate(f_column_data),total = len(f_column_data)):
            
            sentences = []

            for p_column in p_column_data:
                sentences.append(str(p_column))
                sentences.append(str(f_column))
            
            embeddings = self.model.encode(sentences)
            embeddings = torch.tensor(embeddings).to(self.device)

            reshaped_embeddings = embeddings.view(-1, 2, embeddings.size(1))
            
            dot_product = torch.diagonal(torch.matmul(reshaped_embeddings[:, 0, :],reshaped_embeddings[:, 1, :].t()))

            max_index = torch.argmax(dot_product)

            temp_predict.append((index,max_index))

            store.append(dot_product[max_index])

        store = torch.tensor(store).to(self.device)
        
        representation = torch.argmax(store)

        if(store[representation] > thershold):
            indices = torch.nonzero(store > (store[representation] - difference))

        if(flag == 1):

            f_column_names = foreign.columns.tolist()
            p_column_names = primary.columns.tolist()
            f_column_names = ['source-' + f_column_name for f_column_name in f_column_names]
            p_column_names = ['target-' + p_column_name for p_column_name in p_column_names]
            total_names = f_column_names + p_column_names
        else:
            f_column_names = foreign.columns.tolist()
            p_column_names = primary.columns.tolist()
            f_column_names = ['target-' + f_column_name for f_column_name in f_column_names]
            p_column_names = ['source-' + p_column_name for p_column_name in p_column_names]
            total_names =  p_column_names + f_column_names

        output = dict()

        for name in total_names:
            output[name] = []

        foreign_data = foreign.to_dict('records')
        primary_data = primary.to_dict('records')

        for indice in indices:
            f_indice = temp_predict[indice][0]
            p_indice = temp_predict[indice][1]
            
            # push_yet = set()
            for key, value in foreign_data[f_indice].items():
                output[key].append(value)
                # push_yet.add(key)
            for key, value in primary_data[p_indice].items():
                # if(key not in push_yet):
                output[key].append(value)

        df = pd.DataFrame(output)
        if(output_file):
            df.to_csv('./output.csv', index=False)
        return df

class ColMatcher:
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
    
    def df_to_tables(self, df1, df2, src_specified_column):
        df1 = df1.astype(str)
        df2 = df2.astype(str)
        df1.fillna('', inplace=True)
        df2.fillna('', inplace=True)
        
        if type(src_specified_column) == type([]):
            df1['concat'] = df1[src_specified_column].apply(lambda row: ' '.join(row.values.astype(str)), axis=1)
        
        tables = []
        dfs = [df1, df2]
        for df1 in dfs:
            res = {
            'titles': None, 
            'items': []
            }

            res['titles'] = df1.columns.tolist()
            res['items'] = [row.tolist() for _, row in df1.iterrows()] 

            tables.append(res)
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
    
    def get_column_matching(self, src_df, target_df, src_specified_column, n_col_out=1):
        tables = self.df_to_tables(src_df, target_df, src_specified_column)
        src_table = tables[0]
        target_table = tables[1]
        
        res = []
        print(f'Column matching...')
        if type(src_specified_column) == type([]):
            index = src_table['titles'].index('concat')
        else:
            if src_specified_column in src_table['titles']:
                index = src_table['titles'].index(src_specified_column)
            else:
                return "The src_specified_column not in the src_table"
    
        col_src = [src_table['items'][j][index].lower() for j in range(len(src_table['items']))]
        dup_src = len(col_src) - len(set(col_src))
        # if dup_src > math.ceil(self.src_keys_ratio * len(col_src)):
            # print("Caution: There are a few duplicate rows in the source table, the assigned column might not be the primary key.")
        
        column_cnt = list()
        num_tgt_cols = len(target_table['titles'])
        for k in range(num_tgt_cols):
            col_tgt = [target_table['items'][j][k].lower() for j in range(len(target_table['items']))]
            dup_tgt = len(col_tgt) - len(set(col_tgt))
            # print(f'Column "{target_table["titles"][k]}":\nratio of duplicate rows = {dup_tgt/len(col_tgt):.3f}')

            cnt_list = list()
            for q in range(self.q_start, self.q_end):
                cnt = self.get_count_matching_q_grams(q, col_src, col_tgt)
                cnt_list.append((cnt, q))
                # print(f'    q={q}: {cnt/len(col_src)*self.matching_ratio}')
        
            max_cnt, max_q = max(cnt_list)
            column_cnt.append((max_cnt, max_q))

        sort_idx = np.argsort(column_cnt, axis=0)
        sort_idx = np.flip(sort_idx[:, 0])
        # print(sort_idx)
        # print(np.array(target_table['titles'])[sort_idx])
        tgt_rows = np.array(target_table['titles'])[sort_idx][:n_col_out]
        # print(tgt_rows)
        tgt_rows = tgt_rows.tolist()
        sort_idx = sort_idx[:n_col_out].tolist()
        
        # print(f'Find the best target column: {target_table["titles"][idx]} with q={column_cnt[idx][1]}')
        res.append({
            'src_row': src_table['titles'][index],
            'src_row_id': index,
            'target_row': tgt_rows,
            'target_row_id': sort_idx,
        })
        # print(res)
        return res[0]['target_row']
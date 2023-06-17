import pandas as pd
import torch
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

class RowMatcher:
    def __init__(self):

        self.model = SentenceTransformer('sentence-transformers/gtr-t5-large')

        cuda_available = torch.cuda.is_available()

        self.device = torch.device("cuda" if cuda_available else "cpu")

        self.model = SentenceTransformer('sentence-transformers/gtr-t5-large').to(self.device)

    def find(self,output_file,primary_coloum,foreign_coloum,primary_file,foreign_file,thershold = 0.6,difference = 0.24):
        foreign = pd.read_csv(foreign_file)
        primary = pd.read_csv(primary_file)

        f_coloum_data = foreign[foreign_coloum].values
        p_coloum_data = primary[primary_coloum].values

        temp_predict = []
        store = []

        for index,f_coloum in tqdm(enumerate(f_coloum_data),total = len(f_coloum_data)):
            
            sentences = []

            for p_coloum in p_coloum_data:
                sentences.append(str(p_coloum))
                sentences.append(str(f_coloum))
            
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

        f_column_names = foreign.columns.tolist()
        p_column_names = primary.columns.tolist()

        total_names = f_column_names + p_column_names
        output = dict()

        for name in total_names:
            output[name] = []

        foreign_data = foreign.to_dict('records')
        primary_data = primary.to_dict('records')

        for indice in indices:
            f_indice = temp_predict[indice][0]
            p_indice = temp_predict[indice][1]
            
            for key, value in foreign_data[f_indice].items():
                output[key].append(value)
            
            for key, value in primary_data[p_indice].items():
                output[key].append(value)

        df = pd.DataFrame(output)
        if(output_file):
            df.to_csv(output_file, index=False)
            return
        else:
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
        # print(f'Column matching!\nsrc_table: {src_table["name"]}\nsrc_column: {src_specified_column}\ntgt_table: {target_table["name"]}\ntgt_columns: {target_table["titles"]}\n')
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

        idx = column_cnt.index(max(column_cnt))
        # print(f'Find the best target column: {target_table["titles"][idx]} with q={column_cnt[idx][1]}')
        res.append({
            'src_table': src_table['name'],
            'src_row': src_table['titles'][index],
            'src_row_id': index,
            'target_table': target_table['name'],
            'target_row': target_table['titles'][idx],
            'target_row_id': idx,
        })
        
        return res[0]['target_row']
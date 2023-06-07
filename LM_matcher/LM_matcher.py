import pandas as pd
from argparse import ArgumentParser
from sentence_transformers import SentenceTransformer
import torch
from tqdm import tqdm
import numpy as np
import os

class FileRowMatcher:
    def __init__(self):

        self.model = SentenceTransformer('sentence-transformers/gtr-t5-large').cuda()

        cuda_available = torch.cuda.is_available()

        self.device = torch.device("cuda" if cuda_available else "cpu")

    def find(self,input_data_dir,output_file,foreign_coloum,primary_coloum,foreign_file,primary_file,thershold = 0.6,difference = 0.24):
        foreign = pd.read_csv(os.path.join(input_data_dir,foreign_file))
        primary = pd.read_csv(os.path.join(input_data_dir,primary_file))

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

        df.to_csv(output_file, index=False)

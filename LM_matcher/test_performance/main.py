import pandas as pd
from argparse import ArgumentParser
from transformers import AutoTokenizer, AutoModel
from sentence_transformers import SentenceTransformer
import torch
from tqdm import tqdm
import numpy as np
import os

def parse_arguments():
    parser = ArgumentParser()

    parser.add_argument('--data_dir', type=str,
                        default='../data')
    parser.add_argument('--benchmark', type=str,
                        default='autojoin-Benchmark')
    args = parser.parse_args()
    return args

def match(data_dir,case):

    src = pd.read_csv(os.path.join(data_dir,case,'source.csv'))
    target = pd.read_csv(os.path.join(data_dir,case,'target.csv'))
    gt = pd.read_csv(os.path.join(data_dir,case,'ground truth.csv'))

    with open(os.path.join(data_dir,case,'rows.txt'), 'r') as file:
    # Iterate over each line in the file
        i = 0
        
        for line in file:
            if( i == 0):
                line = line.strip('\n').split(':')
                src_col = line[0]
                target_col = line[1]

                i += 1

            else:
                
                direction = line

    source_values = src[src_col].values
    target_values = target[target_col].values

    if(direction == 'source'):
        foreign_keys = source_values
        primary_keys = target_values
    else:
        foreign_keys = target_values
        primary_keys = source_values

    model = SentenceTransformer('sentence-transformers/gtr-t5-large').cuda()

    device = torch.device('cuda')

    temp_predict = []
    store = []
    predict = []
    
    for foreign_key in foreign_keys:
        
        sentences = []
        
        for primary_key in primary_keys:
            sentences.append(str(primary_key))
            sentences.append(str(foreign_key))

        embeddings = model.encode(sentences)
        embeddings = torch.tensor(embeddings).to(device)

        reshaped_embeddings = embeddings.view(-1, 2, embeddings.size(1))
        
        dot_product = torch.diagonal(torch.matmul(reshaped_embeddings[:, 0, :],reshaped_embeddings[:, 1, :].t()))

        max_index = torch.argmax(dot_product)
            
        if(direction == 'source'):
            temp_predict.append((foreign_key,primary_keys[max_index]))

        else:
            temp_predict.append((primary_keys[max_index],foreign_key))

        store.append(dot_product[max_index])

    store = torch.tensor(store).to(device)
    
    representation = torch.argmax(store)

    thershold = 0.6
    difference = 0.24

    if(store[representation] > thershold):
        indices = torch.nonzero(store > (store[representation] - difference))

    for indice in indices:
        predict.append(temp_predict[indice])
        
    src_gt = gt['source-' + src_col].values
    target_gt = gt['target-' + target_col].values
    
    correct = 0

    for answer in zip(src_gt,target_gt):
        if answer in predict:
            correct += 1

    precision = correct / len(predict)
    
    recall = correct / len(src_gt)
    
    f1 = 2 * precision * recall / (precision + recall)
    
    return f1

def main(args):
    data_dir = args.data_dir
    benchmark = args.benchmark

    files = os.listdir(os.path.join(data_dir,benchmark))
    f1s = []

    for file in tqdm(files):
        f1s.append(match(os.path.join(data_dir,benchmark),file))
    
    total = 0
    not_good = []

    for index,f1 in  enumerate(f1s):
        total += f1

        if(f1 < 0.85):
            not_good.append(files[index])

    print(total/len(files))
    print(not_good)

if __name__ == '__main__':
    main(parse_arguments())
    
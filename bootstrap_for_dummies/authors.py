import os

import pandas as pd
import numpy as np
import pickle

input_dir = r'F:\study\MADE\MADE22\project\dataset\normalized'

aa_inter = pd.read_csv(os.path.join(input_dir, 'aa_inter.csv'))

df = aa_inter[['_id', 'author__id']].merge(aa_inter[['_id', 'author__id']], left_on='_id', right_on='_id', suffixes=['_1', '_2'])

df = df[df['author__id_1'] < df['author__id_2']]



if __name__ == '__main__':
    print()
import os
from sqlalchemy import create_engine
import pandas as pd
import numpy as np
import pickle
input_dir = r'F:\study\MADE\MADE22\project\dataset\normalized'

with open(os.path.join(input_dir, "articles_lbl.csv"), 'rb') as file:
    df = pd.read_csv(file)  ##, index=False)

    df.abstract.map(len).max()
    print(df.head())
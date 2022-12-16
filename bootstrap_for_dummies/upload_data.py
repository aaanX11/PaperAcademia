import os
from sqlalchemy import create_engine
import pandas as pd
import numpy as np
import pickle


input_dir = r'F:\study\MADE\MADE22\project\dataset\normalized'
input_dir2 = r'F:\study\MADE\MADE22\project\dataset\connec_compont'


def upload():
    engine = create_engine('postgresql://flaskdbusr:flaskdbpw@127.0.0.1:5432/flaskdb')
    engine.connect()

    articles_less1 = pd.read_csv(os.path.join(input_dir2, 'small_components_ids.csv'))
    articles_less2 = pd.read_csv(os.path.join(input_dir2, '100k_articles.csv'))

    articles_less = pd.concat((articles_less2, articles_less1))
    articles_less.drop_duplicates(inplace=True)

    articles = pd.DataFrame()
    authors = pd.DataFrame()
    venues = pd.DataFrame()
    aa_inter = pd.read_csv(os.path.join(input_dir, 'aa_inter.csv'))
    aa_inter = articles_less.merge(aa_inter, left_on='_id', right_on='_id')
    authors_less = aa_inter[['author__id']].rename(columns={'author__id': '_id'}).drop_duplicates()

    for chunk in pd.read_csv(os.path.join(input_dir, 'authors.csv'),
                             chunksize=10000,
                             usecols=['_id', 'name', 'org', 'orgid'],
                             dtype={'_id': str, 'name': str, 'org': str, 'orgid': str}):
        authors = authors.append(chunk)
    authors = authors_less.merge(authors, left_on='_id', right_on='_id')
    # for chunk in pd.read_csv(os.path.join(input_dir, 'articles.csv'),
    #                          chunksize=10000,
    #                          usecols=['_id', 'title', 'venue', 'year', 'keywords', 'fos', 'n_citation', 'abstract', 'references'],
    #                          dtype={'_id': str, 'title': str, 'venue': str, 'year': np.float, 'keywords': str, 'fos': str, 'n_citation': np.float, 'abstract': str, 'references': str}
    #                          ):
    #     articles = articles.append(chunk)
    #
    # articles = articles.set_index('_id')
    # articles['n_citation'] = articles['n_citation'].map(lambda x: int(x) if isinstance(x, float) and not np.isnan(x) else x)

    for chunk in pd.read_csv(os.path.join(input_dir, 'venues.csv'),
                             chunksize=10000,
                             usecols=['_id', 'name_d', 'raw'],
                             dtype={'_id': str, 'name_d': str, 'raw': str}):
        chunk['name'] = chunk['name_d'].fillna(chunk['raw'])
        venues = venues.append(chunk[['_id', 'name']])

    #with open(os.path.join(input_dir, 'data_labels.pkl'), 'rb') as file:
    #    articles_w_lbl = pickle.load(file)

    #df = articles.merge(articles_w_lbl['topics'], left_index=True, right_index=True, how='left')
    #with open(os.path.join(input_dir, "articles_lbl.csv"), 'wb') as file:
    #    df.to_csv(file)  ##, index=False)
    #    # pickle.dump(all_articles, file)

    #df.to_sql('articles', engine, if_exists='append')
    with open(os.path.join(input_dir, "articles_lbl.csv"), 'rb') as file:
         df = pd.read_csv(file)  ##, index=False)

    df = articles_less.merge(df, left_on='_id', right_on='_id')
    #df.to_sql('articles', engine, if_exists='append')
    #----------------------------------------------------------------------------------------------------

    authors.to_sql('authors', engine, if_exists='append')
    #venues.to_sql('venues', engine)
    aa_inter.to_sql('aa_inter', engine, if_exists='append')
    engine.dispose()


# '_id', 'title', 'venue', 'year', 'keywords', 'fos', 'n_citation', 'abstract', 'references', 'topic'
# 53e9a751b7602d9703087637', '53e9a751b7602d970308763e',
#        '53e9a751b7602d9703087640', '53e9a751b7602d9703087646',
#        '53e9a751b7602d9703087649', '53e9a751b7602d970308764b',
#        '53e9a751b7602d9703087659', '53e9a751b7602d970308766d',
#        '53e9a751b7602d9703087677', '53e9a751b7602d9703087690',


if __name__ == '__main__':
    upload()
    # upload_interactions()

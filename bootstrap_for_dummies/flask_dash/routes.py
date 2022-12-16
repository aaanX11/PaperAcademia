import functools
import os
from flask import Blueprint
from flask import flash
from flask import request
from flask import Flask, url_for, render_template, redirect
from jinja2 import Template
from .db import get_engine
from .auth import login_required
from .forms import SearchForm
from  . import queries
import pandas as pd
from flask import g

bp = Blueprint("routes", __name__)


@bp.route("/bye")
def bye():
    tm = Template(""" Bye!""")
    return tm.render()


@bp.route("/")
def hello():

    return render_template('iframe_test.html')



@bp.route("/search", methods=['GET', 'POST'])
@login_required
def search():
    form = SearchForm(request.form)
    if request.method == "POST" and form.validate():
        if not form.author.data and not form.year.data and not form.topic.data:
            flash("Some fields must be filled.")
        else:
            return redirect(url_for('routes.articles', year=form.year.data, author=form.author.data, topic=form.topic.data))

    return render_template("search/search.html")



@bp.route("/articles")
@login_required
def articles():
    d = request.args.to_dict()
    year = d.get('year', None)
    author = d.get('author', None)
    topic = d.get('topic', None)

    db = get_engine()
    if author:
        df1 = pd.read_sql_query(
            queries.q_authors_articles,
            con=db,
            params={'authorname': '%' + author + '%'},
            index_col='_id'
        )

        if year:
            df1 = df1[df1.year == int(year)]
        if topic:
            df1 = df1[df1.topics.str.contains(topic)]
    else:
        if year:
            df1 = pd.read_sql_query(
                queries.q_year_articles,
                con=db,
                params={'year': year},
                index_col='_id'
            )
            if topic:
                df1 = df1[df1.topics.str.contains(topic)]
        else:
            df1 = pd.read_sql_query(
                queries.q_topic_articles,
                con=db,
                params={'topic': '%' + topic + '%'},
                index_col='_id'
            )

    df1['author_names'] = df1['author_names'].map(lambda x: x.split('; '))
    df1['topics'] = df1['topics'].map(
        lambda x: x.strip('{}').split(',') if isinstance(x, str) else [])

    df_likes = pd.read_sql_query(
        queries.q_user_likes,
        con=db,
        params={'userid': g.user["id"]}
    )

    df1['liked'] = 0
    articles_ = set(df1.index.to_list())

    df1.loc[[x for x in df_likes.article_id.to_list() if x in articles_], 'liked'] = 1

    return render_template("search/sometable_view.html", user_id=g.user["id"], article_list=df1.reset_index(names=['_id']).to_dict('records'))



@bp.route("/one_article")
@login_required
def one_article():
    d = request.args.to_dict()
    _id = d.get('art_id', None)

    db = get_engine()

    df1 = pd.read_sql_query(
        queries.q_1article,
        con=db,
        params={'article_id': _id},
        index_col='_id'
    )
    if len(df1) == 0:
        return render_template("search/article_not_found.html")

    df1['author_names'] = df1['author_names'].map(lambda x: x.split('; '))
    df1['references'] = df1['references'].map(lambda x: x.split('; '))
    df1['topics'] = df1['topics'].map(lambda x: x.strip('{}').split(','))

    df_likes = pd.read_sql_query(
        queries.q_user_article_like,
        con=db,
        params={'userid': g.user["id"], 'article_id': _id}
    )
    if len(df_likes):
        df1['liked'] = 1
    else:
        df1['liked'] = 0

    return render_template("search/article_view.html", user_id=g.user["id"], article_obj=df1.reset_index(names=['_id']).to_dict('records')[0])


@bp.route("/top_authors")
def top_authors():

    db = get_engine()

    df1 = pd.read_sql_query(
        queries.q_top_authors,
        con=db,
    )
    df1['years'] = df1['min_year'] + '-' + df1['max_year']
    df1.loc[df1[df1.min_year == df1.max_year].index, 'years'] = df1.loc[df1[df1.min_year == df1.max_year].index, 'min_year']
    return render_template("search/authors.html", authors_list=df1.to_dict('records'))


@bp.route("/cytoscape")
@login_required
def cytoscape():
    # d = request.args.to_dict()
    # topic = d.get('topic', None)
    # if not topic:
    #     flash("No topic specified.")
    #     redirect(url_for('top_authors'))
    #
    db = get_engine()
    # db.execute(queries.q_cytograph1)
    # df1 = pd.read_sql_query(
    #     queries.q_cytograph2,
    #     con=db,
    #     params={'topic': '%' + topic + '%'},
    # )
    #
    # return render_template(
    #     "/graph/graph.html",
    #     elmnt_list=df1.a1.map(lambda x: {'data': {'id': x}}).to_list()
    #                + df1[['_id', 'a1', 'a2']].apply(lambda row: {'data': {'id': row._id, 'source': row.a1, 'target': row.a2}}, axis=1).to_list()
    # )
    #
    # input_dir = r'F:\study\MADE\MADE22\project\dataset\normalized'
    # input_dir2 = r'F:\study\MADE\MADE22\project\dataset\connec_compont'
    #
    # aa_inter = pd.read_csv(os.path.join(input_dir, 'aa_inter.csv'))
    #
    #
    # articles_less = pd.read_csv(os.path.join(input_dir2, 'small_components_ids.csv'))
    #
    # df = aa_inter[['_id', 'author__id']].merge(aa_inter[['_id', 'author__id']], left_on='_id', right_on='_id',
    #                                            suffixes=['_1', '_2'])
    #
    # df = articles_less.merge(df, left_on='_id', right_on='_id')
                                               #                                            suffixes=['_1', '_2'])
    # df = df[df['author__id_1'] < df['author__id_2']]
    # df = df[df['author__id_1'].notna() & df['author__id_2'].notna()]
    # df.drop_duplicates(inplace=True)

    # return render_template(
    #     "/graph/graph.html",
    #     elmnt_list=list(
    #         map(lambda x: {'data': {'id': x}}, (set(df.author__id_1.to_list() + df.author__id_2.to_list()))))
    #                + df[['_id', 'author__id_1', 'author__id_2']].apply(
    #         lambda row: {'data': {'id': row._id, 'source': row.author__id_1, 'target': row.author__id_2}},
    #         axis=1).to_list()
    # )
    #------------------------------------------------------------------------------
    # aa_inter = pd.read_sql_query(
    #     queries.q_cytograph5,
    #     con=db
    # )
    # df = aa_inter[['_id', 'aa']].merge(aa_inter[['_id', 'aa']], left_on='_id', right_on='_id',suffixes=['_1', '_2'])
    # df = df[df['aa_1'] < df['aa_2']]
    # df = df[df['aa_1'].notna() & df['aa_2'].notna()]
    # df.drop_duplicates(inplace=True)
    #
    # return render_template(
    #            "/graph/graph.html",
    #            elmnt_list=list(map(lambda x: {'data': {'id': x}}, (set(df.aa_1.to_list() + df.aa_2.to_list()))))
    #                       + df[['_id', 'aa_1', 'aa_2']].apply(lambda row: {'data': {'id': row._id, 'source': row.aa_1, 'target': row.aa_2}}, axis=1).to_list()
    #        )
    # ------------------------------------------------------------------------------
    db.execute(queries.q_cytograph6)
    df = pd.read_sql_query(
        queries.q_cytograph7,
        con=db
    )
    input_dir2 = r'F:\study\MADE\MADE22\project\dataset\connec_compont'
    articles_less = pd.read_csv(os.path.join(input_dir2, 'small_components_ids.csv'))
    df = articles_less.merge(df, left_on='_id', right_on='_id')
    df = df[df['aa_1'].notna() & df['aa_2'].notna()]
    df.drop_duplicates(inplace=True)

    return render_template(
        "/graph/graph.html",
        elmnt_list=list(map(lambda x: {'data': {'id': x}}, (set(df.aa_1.to_list() + df.aa_2.to_list()))))
                   + df[['_id', 'aa_1', 'aa_2']].apply(
            lambda row: {'data': {'id': row._id, 'source': row.aa_1, 'target': row.aa_2}}, axis=1).to_list()
    )

@bp.route("/ldavis")
@login_required
def ldavis():
    return render_template('vis.html')
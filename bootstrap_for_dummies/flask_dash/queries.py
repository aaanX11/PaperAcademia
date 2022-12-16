q_authors_articles = """select * from (
	select articles._id, title, topics, string_agg(name, '; ') author_names, year   from articles  
	inner join (
		select name, author__id, aa_inter._id from aa_inter inner join authors on aa_inter.author__id = authors._id 
	) aa_inter_ on articles._id = aa_inter_._id 
	group by articles._id, title, topics, year
	) t 
where author_names like %(authorname)s and _id IS NOT NULL;"""

q_user_likes = '''select article_id from ua_inter where id = %(userid)s ;'''

q_insert_like = '''insert into ua_inter (id, article_id) values( %(userid)s, %(articleid)s ) ; '''

q_remove_like = '''delete from ua_inter where id = %(userid)s and article_id = %(articleid)s; '''


q_year_articles = '''select * from (
	select articles._id, title, topics, string_agg(name, '; ') author_names, year   from articles   
	inner join (
		select name, author__id, aa_inter._id from aa_inter inner join authors on aa_inter.author__id = authors._id 
	) aa_inter_ on articles._id = aa_inter_._id 
	group by articles._id, title, topics, year
	) t 
where year = %(year)s and _id IS NOT NULL; '''

q_topic_articles = '''select * from (
	select articles._id, title, topics, string_agg(name, '; ') author_names, year   from articles   
	inner join (
		select name, author__id, aa_inter._id from aa_inter inner join authors on aa_inter.author__id = authors._id 
	) aa_inter_ on articles._id = aa_inter_._id 
	group by articles._id, title, topics, year
	) t 
where topics like %(topic)s and _id IS NOT NULL 
LIMIT 200 ; '''

q_1article = '''select abstract, fos, keywords, venues.name venue, t2._id, title, topics, author_names, year, t2.references from (
 select abstract, fos, keywords, venue, t1._id _id, title, topics, author_names, year, articles.references from 
 (
	select string_agg(name, '; ') author_names, aa_inter._id _id from aa_inter inner join authors on aa_inter.author__id = authors._id 
	where aa_inter._id = %(article_id)s
	group by aa_inter._id
) t1  inner join articles on t1._id = articles._id 
	) t2 inner join venues on t2.venue = venues._id  '''

q_user_article_like = '''select article_id from ua_inter where id = %(userid)s and article_id = %(article_id)s ;'''


q_top_authors = '''select author_id, author_articles_cit.name, cast(sum(n_citation) as INTEGER) citations, cast(min(author_articles_cit.year) as varchar) min_year, cast(max(author_articles_cit.year) as varchar) max_year from 
	(select distinct articles._id _id, name, author_id, n_citation, year from 
	(select * from 
		(SELECT _id author_id, name, org FROM authors ) author 
		inner join aa_inter on author.author_id = aa_inter.author__id ) author_articles 
	inner join articles on author_articles._id = articles._id 
 ) author_articles_cit 
group by author_id, author_articles_cit.name 
order by citations desc NULLS LAST 
LIMIT 200 ;'''


q_cytograph1 = '''CREATE TEMPORARY TABLE IF NOT EXISTS aa_inter_tmp AS (
	select distinct _id, t.author__id from 
		(select distinct author__id from aa_inter 
			group by author__id 
			having count(*) > 1 ) t 
		left join aa_inter on t.author__id = aa_inter.author__id 
	);'''


q_cytograph2 = '''select t1._id, t1.author__id a1, t2.author__id a2 from 
articles inner join
aa_inter_tmp t1 on articles._id = t1._id
inner join aa_inter_tmp t2 on t1._id = t2._id 
where articles.topics like %(topic)s and 
not t1.author__id = t2.author__id 
and t1._id in ('53e9a767b7602d97030a19e2', '53e9a774b7602d97030aad59', '53e9a774b7602d97030acc8d') 
; '''


q_cytograph3 = '''select t1._id, t1.author__id a1, t2.author__id a2 from 
articles inner join
aa_inter_tmp t1 on articles._id = t1._id
inner join aa_inter_tmp t2 on t1._id = t2._id 
where articles.topics like %(topic)s 
and t1._id in ('53e9a767b7602d97030a19e2', '53e9a774b7602d97030aad59', '53e9a774b7602d97030acc8d') 
; '''

q_cytograph5 = '''select aa_inter._id _id, authors.name aa from aa_inter 
left join authors on aa_inter.author__id = authors._id'''

q_cytograph6 = '''CREATE TEMPORARY TABLE IF NOT EXISTS aa_inter_tmp
    AS (
select aa_inter._id _id, authors.name aa from aa_inter 
left join authors on aa_inter.author__id = authors._id
		) ; '''

q_cytograph7 = '''select t1._id, t1.aa aa_1, t2.aa aa_2 from aa_inter_tmp t1 
inner join 
aa_inter_tmp t2 on t1._id = t2._id 
where t1.aa < t2.aa;'''
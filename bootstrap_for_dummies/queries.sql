CREATE INDEX article_id_index ON aa_inter (_id);
CREATE INDEX author_id_index ON aa_inter (author__id);
--33sec

select articles._id _id, title, abstract, name, year from 
(select * from 
	(SELECT _id author__id, name, org FROM authors WHERE name = 'Raghunathan Rengaswamy' ) author 
	inner join aa_inter on author.author__id = aa_inter.author__id ) author_articles 
left join articles on author_articles._id = articles._id 
WHERE articles._id IS NOT NULL ;
--2sec
	
select * from 
	aa_inter where author__id in (SELECT _id FROM authors WHERE name = 'Maryam Biazaran' ) ;
-- 2sec	


select title, abstract, name, year from 
(select * from 
	(SELECT _id author__id, name, org FROM authors WHERE name = 'Maryam Biazaran' ) author 
	inner join aa_inter on author.author__id = aa_inter.author__id ) author_articles 
left join articles on author_articles._id = articles._id ;
--2sec

--select * from articles where _id is NULL;
ALTER TABLE articles 
ADD CONSTRAINT articles__id_pkey PRIMARY KEY (_id);


select _id, topics from articles where topics like '%math%' ;
--0.2sec


select articles._id _id, title, abstract, name, year from 
(select * from 
	(SELECT _id author__id, name, org FROM authors ) author 
	inner join aa_inter on author.author__id = aa_inter.author__id ) author_articles 
left join articles on author_articles._id = articles._id ;
--16sec <-----------------<-----------------<---------------<------------------<-------------------<----------------???

select distinct articles._id _id, title, abstract, name, year, n_citation from 
(select * from 
	(SELECT _id author__id, name, org FROM authors ) author 
	inner join aa_inter on author.author__id = aa_inter.author__id ) author_articles 
inner join articles on author_articles._id = articles._id ;
--2sec

select distinct articles._id _id, title, abstract, name, author_id, year, n_citation from 
(select * from 
	(SELECT _id author_id, name, org FROM authors ) author 
	inner join aa_inter on author.author_id = aa_inter.author__id ) author_articles 
inner join articles on author_articles._id = articles._id ;
 --2sec


 select name, sum(n_citation) citations from 
	(select distinct articles._id _id, name, author_id, n_citation from 
	(select * from 
		(SELECT _id author_id, name, org FROM authors ) author 
		inner join aa_inter on author.author_id = aa_inter.author__id ) author_articles 
	inner join articles on author_articles._id = articles._id 
 ) author_articles_cit 
group by author_id, name 
order by citations desc ;
--2sec

select name, sum(n_citation) citations from 
	(select distinct articles._id _id, name, author_id, n_citation from 
	(select * from 
		(SELECT _id author_id, name, org FROM authors ) author 
		inner join aa_inter on author.author_id = aa_inter.author__id ) author_articles 
	inner join articles on author_articles._id = articles._id 
 ) author_articles_cit 
group by author_id, name 
order by citations desc NULLS LAST;
--2sec

---------------------------------
--Erik Brynjolfsson - 2 articles
--Feng Gao
----------------------------------

select articles._id, title, string_agg(name, '; ') from articles 
inner join (
	select name, author__id, aa_inter._id from aa_inter inner join authors on aa_inter.author__id = authors._id
) aa_inter_ on articles._id = aa_inter_._id 
group by articles._id, title 
--4sec


select articles._id, title, string_agg(name, '; ') from articles 
inner join (
	select name, author__id, aa_inter._id from aa_inter inner join authors on aa_inter.author__id = authors._id 
	where name like '%Erik Brynjolfsson%'
) aa_inter_ on articles._id = aa_inter_._id 
group by articles._id, title 
--0.3sec

select * from (
	select articles._id, title, topics, string_agg(name, '; ') author_names, year   from articles 
	inner join (
		select name, author__id, aa_inter._id from aa_inter inner join authors on aa_inter.author__id = authors._id 
	) aa_inter_ on articles._id = aa_inter_._id 
	group by articles._id, title, topics, year
	) t 
where author_names like '%Feng Gao%' and _id IS NOT NULL;
--0.5sec


select * from (
	select articles._id, title, topics, string_agg(name, '; ') author_names, year   from articles 
	inner join (
		select name, author__id, aa_inter._id from aa_inter inner join authors on aa_inter.author__id = authors._id 
	) aa_inter_ on articles._id = aa_inter_._id 
	group by articles._id, title, topics, year
	) t 
where year = 2007 and _id IS NOT NULL;
--4sec

select * from (
	select articles._id, title, topics, string_agg(name, '; ') author_names, year   from articles 
	inner join (
		select name, author__id, aa_inter._id from aa_inter inner join authors on aa_inter.author__id = authors._id 
	) aa_inter_ on articles._id = aa_inter_._id 
	group by articles._id, title, topics, year
	) t 
where topics like '%compsci%' and _id IS NOT NULL 
LIMIT 200 ;
--0.5sec

select abstract, fos, keywords, venues.name venue, tt._id, title, topics, author_names, year from (
select * from (
select abstract, fos, keywords, venue, articles._id _id, title, topics, string_agg(name, '; ') author_names, year   from articles 
	inner join (
		select name, author__id, aa_inter._id from aa_inter inner join authors on aa_inter.author__id = authors._id 
	) aa_inter_ on articles._id = aa_inter_._id 
	group by articles._id, title, topics, year 
	) t where _id = '53e9a751b7602d9703087690' 
	) tt inner join venues on tt.venue = venues._id ;
--0.4sec


select abstract, n_citation, tt.references, fos, keywords, venues.name venue, tt._id, title, topics, author_names, year from (
select * from (
select abstract, n_citation, articles.references, fos, keywords, venue, articles._id _id, title, topics, string_agg(name, '; ') author_names, year   from articles 
	inner join (
		select name, author__id, aa_inter._id from aa_inter inner join authors on aa_inter.author__id = authors._id 
	) aa_inter_ on articles._id = aa_inter_._id 
	group by articles._id, title, topics, year 
	) t where _id = %(article_id)s  
	) tt inner join venues on tt.venue = venues._id ;


select author_id, author_articles_cit.name, sum(n_citation) citations, min(author_articles_cit.year) min_year, max(author_articles_cit.year) max_year from 
	(select distinct articles._id _id, name, author_id, n_citation, year from 
	(select * from 
		(SELECT _id author_id, name, org FROM authors ) author 
		inner join aa_inter on author.author_id = aa_inter.author__id ) author_articles 
	inner join articles on author_articles._id = articles._id 
 ) author_articles_cit 
group by author_id, author_articles_cit.name 
order by citations desc NULLS LAST ;
--3sec

select author_id, author_articles_cit.name, sum(n_citation) citations, cast(min(author_articles_cit.year) as varchar) min_year, cast(max(author_articles_cit.year) as varchar) max_year from 
	(select distinct articles._id _id, name, author_id, n_citation, year from 
	(select * from 
		(SELECT _id author_id, name, org FROM authors ) author 
		inner join aa_inter on author.author_id = aa_inter.author__id ) author_articles 
	inner join articles on author_articles._id = articles._id 
 ) author_articles_cit 
group by author_id, author_articles_cit.name 
order by citations desc NULLS LAST ;

select author_id, author_articles_cit.name, sum(n_citation) citations, cast(min(author_articles_cit.year) as varchar) min_year, cast(max(author_articles_cit.year) as varchar) max_year from 
	(select distinct articles._id _id, name, author_id, n_citation, year from 
	(select * from 
		(SELECT _id author_id, name, org FROM authors ) author 
		inner join aa_inter on author.author_id = aa_inter.author__id ) author_articles 
	inner join articles on author_articles._id = articles._id 
 ) author_articles_cit 
group by author_id, author_articles_cit.name 
order by citations desc NULLS LAST ;

select * from 
(
	select distinct t1._id, t1.author__id a1, t2.author__id a2 from aa_inter t1 
	inner join aa_inter t2 on t1._id = t2._id 
	--where t1._id in ('53e9a767b7602d97030a19e2', '53e9a774b7602d97030aad59', '53e9a774b7602d97030acc8d') 
) t 
where not a1 = a2 
order by 1 ;
--34sec

select _id, filtered.author__id from 
(
	select distinct author__id from aa_inter 
	group by author__id 
	having count(*) > 1 
) filtered 
inner join aa_inter on aa_inter.author__id = filtered.author__id
--12sec

CREATE TEMPORARY TABLE IF NOT EXISTS aa_inter_tmp
    AS (
	select distinct author__id from aa_inter 
	group by author__id 
	having count(*) > 1 
	);
--1sec

select _id, t1.author__id author1, t2.author__id author2 from aa_inter_tmp t1
inner join aa_inter_tmp t2 on t1.author__id = t2.author__id 
left join aa_inter on t1.author__id = aa_inter.author__id ;
--18sec

select distinct _id, t.author__id from 
(select distinct author__id from aa_inter 
	group by author__id 
	having count(*) > 1 ) t 
left join aa_inter on t.author__id = aa_inter.author__id 
--9sec


CREATE TEMPORARY TABLE IF NOT EXISTS aa_inter_tmp AS (
	select distinct _id, t.author__id from 
		(select distinct author__id from aa_inter 
			group by author__id 
			having count(*) > 1 ) t 
		left join aa_inter on t.author__id = aa_inter.author__id 
	);
--19sec

CREATE INDEX article_id_index ON aa_inter_tmp (_id);
CREATE INDEX author_id_index ON aa_inter_tmp (author__id);
--index 

select * from 
(
	select distinct t1._id, t1.author__id a1, t2.author__id a2 from aa_inter_tmp t1 
	inner join aa_inter_tmp t2 on t1._id = t2._id 
	--where t1._id in ('53e9a767b7602d97030a19e2', '53e9a774b7602d97030aad59', '53e9a774b7602d97030acc8d') 
) t 
where not a1 = a2 
order by 1 ;
--cannot

select t1._id, t1.author__id a1, t2.author__id a2 from 
articles inner join
aa_inter_tmp t1 on articles._id = t1._id
inner join aa_inter_tmp t2 on t1._id = t2._id 
where articles.topics like '%tech%'
--6sec


select distinct t1._id, t1.author__id a1, t2.author__id a2 from 
articles inner join
aa_inter_tmp t1 on articles._id = t1._id
inner join aa_inter_tmp t2 on t1._id = t2._id 
where articles.topics like '%compsci%' and 
not t1.author__id = t2.author__id 
and t1._id = '53e9a774b7602d97030aad59'; -- , '53e9a774b7602d97030acc8d') 
; 


DROP TABLE aa_inter_tmp;
CREATE TEMPORARY TABLE IF NOT EXISTS aa_inter_tmp AS (
select distinct _id, t.author__id from 
(select distinct author__id from aa_inter 
	group by author__id 
	having count(*) > 1 ) t  -- authors with more then 1 article
left join aa_inter on t.author__id = aa_inter.author__id  -- and their articles
-- must be filtered aa_inter
);


"53e9a767b7602d97030a19e2"	"53f46293dabfaefedbb79f53"	"545932e7dabfaeb0fe3470f5"
"53e9a767b7602d97030a19e2"	"53f46293dabfaefedbb79f53"	"53f46293dabfaefedbb79f53"
"53e9a767b7602d97030a19e2"	"545932e7dabfaeb0fe3470f5"	"545932e7dabfaeb0fe3470f5"
"53e9a767b7602d97030a19e2"	"545932e7dabfaeb0fe3470f5"	"53f46293dabfaefedbb79f53"
"53e9a774b7602d97030aad59"	"54102310dabfae450f4d4e6b"	"54102310dabfae450f4d4e6b"
"53e9a774b7602d97030aad59"	"54102310dabfae450f4d4e6b"	"53f4376ddabfaeb22f47ac28"
"53e9a774b7602d97030aad59"	"53f4376ddabfaeb22f47ac28"	"54102310dabfae450f4d4e6b"
"53e9a774b7602d97030aad59"	"53f4376ddabfaeb22f47ac28"	"53f4376ddabfaeb22f47ac28"
"53e9a774b7602d97030acc8d"	"56cb18a1c35f4f3c656578ee"	"542be23ddabfae216e61c971"
"53e9a774b7602d97030acc8d"	"56cb18a1c35f4f3c656578ee"	"542e55a1dabfae4b91c40d4d"
"53e9a774b7602d97030acc8d"	"56cb18a1c35f4f3c656578ee"	"5429973adabfaec7081977be"
"53e9a774b7602d97030acc8d"	"56cb18a1c35f4f3c656578ee"	"56cb18a1c35f4f3c656578ee"
"53e9a774b7602d97030acc8d"	"5429973adabfaec7081977be"	"542be23ddabfae216e61c971"
"53e9a774b7602d97030acc8d"	"5429973adabfaec7081977be"	"542e55a1dabfae4b91c40d4d"
"53e9a774b7602d97030acc8d"	"5429973adabfaec7081977be"	"5429973adabfaec7081977be"
"53e9a774b7602d97030acc8d"	"5429973adabfaec7081977be"	"56cb18a1c35f4f3c656578ee"
"53e9a774b7602d97030acc8d"	"542e55a1dabfae4b91c40d4d"	"542be23ddabfae216e61c971"
"53e9a774b7602d97030acc8d"	"542e55a1dabfae4b91c40d4d"	"542e55a1dabfae4b91c40d4d"
"53e9a774b7602d97030acc8d"	"542e55a1dabfae4b91c40d4d"	"5429973adabfaec7081977be"
"53e9a774b7602d97030acc8d"	"542e55a1dabfae4b91c40d4d"	"56cb18a1c35f4f3c656578ee"
"53e9a774b7602d97030acc8d"	"542be23ddabfae216e61c971"	"542be23ddabfae216e61c971"
"53e9a774b7602d97030acc8d"	"542be23ddabfae216e61c971"	"542e55a1dabfae4b91c40d4d"
"53e9a774b7602d97030acc8d"	"542be23ddabfae216e61c971"	"5429973adabfaec7081977be"
"53e9a774b7602d97030acc8d"	"542be23ddabfae216e61c971"	"56cb18a1c35f4f3c656578ee"


CREATE TEMPORARY TABLE IF NOT EXISTS authors_tmp AS (
select distinct aa_inter.author__id from aa_inter  
		group by aa_inter.author__id 
		having count(*) > 1 
	) ;

select distinct _id, t.author__id from 
	() t  -- authors with more then 1 article
	left join aa_inter on t.author__id = aa_inter.author__id 
	---------------------------------------------------------------------------------------------------------------
	---------------------------------------------------------------------------------------------------------------
	---------------------------------------------------------------------------------------------------------------
	---------------------------------------------------------------------------------------------------------------
	---------------------------------------------------------------------------------------------------------------
	---------------------------------------------------------------------------------------------------------------
	---------------------------------------------------------------------------------------------------------------
	---------------------------------------------------------------------------------------------------------------


select abstract, fos, keywords, venues.name venue, t2._id, title, topics, author_names, year from (
 select abstract, fos, keywords, venue, t1._id _id, title, topics, author_names, year from 
 (
	select string_agg(name, '; ') author_names, aa_inter._id _id from aa_inter inner join authors on aa_inter.author__id = authors._id 
	where aa_inter._id = %(article_id)s
	group by aa_inter._id
) t1  inner join articles on t1._id = articles._id 
	) t2 inner join venues on t2.venue = venues._id 
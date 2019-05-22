# Database code for the DB news, full solution!

import psycopg2

DBNAME = "news"

def get_result():
  """Return the top three most viewed articles with their view counts.
    the top three most article author with their view counts,
	 and the top one day whith  more than 1% of requests lead to errors

    Returns:
    A dictionary of 3 elements tuples. 
	the top_three_articles tuple return:
      - the title of the article.
      - the number of views for the article
	 The top_three_authors return :
	  - the name of author.
      - the number of views for his articles
	 The top_day_error tuple return:
	  - the day.
      - the percent of the error

    The list is sorted by number of views in descending order. Only the three
    most viewed articles are returned.
  """
  results={}
  db = psycopg2.connect(database=DBNAME)
  c = db.cursor()
  c.execute("""SELECT articles.title, COUNT(log.path) AS num FROM log, articles 
  WHERE log.path=CONCAT('/article/',articles.slug) 
  GROUP BY articles.title 
  ORDER BY num DESC 
  LIMIT 3
  """)
  results['top_three_articles'] = c.fetchall()
  c.execute("""SELECT authors.name, COUNT(log.path) AS num 
  FROM log, articles, authors 
  WHERE log.path=CONCAT('/article/',articles.slug) 
  AND articles.author=authors.id 
  GROUP BY authors.name 
  ORDER BY num DESC 
  LIMIT 3
  """)
  results['top_three_authors'] = c.fetchall()
  c.execute("""SELECT date_trunc('day', log.time) ,
  CAST(tot.somme2*100 as FLOAT) / COUNT(*) AS pourcentage
  FROM log 
  INNER JOIN (SELECT date_trunc('day', time) as date2,
  COUNT(log.time) as somme2 
  FROM log 
  WHERE  status like '%4%' or status like '%5%' 
  GROUP BY date_trunc('day', time)) AS tot 
  ON (tot.date2 = date_trunc('day', time)) 
  GROUP BY (tot.somme2,date_trunc('day', log.time)) 
  ORDER BY pourcentage DESC 
  LIMIT 1
  """)
  results['top_day_error'] = c.fetchall()
  db.close()
  return results




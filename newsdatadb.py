# Database code for the DB news, full solution!

import psycopg2

DBNAME = "news"

def get_posts():
  """Return the top three most viewed articles with their view counts.

    Returns:
    A list of two element tuples. Each tuple contains:
      - the title of the article.
      - the number of views for the article

    The list is sorted by number of views in descending order. Only the three
    most viewed articles are returned.
  """
  db = psycopg2.connect(database=DBNAME)
  c = db.cursor()
  c.execute("""SELECT articles.title, COUNT(log.path) AS num FROM log, articles 
  WHERE log.path=CONCAT('/article/',articles.slug) 
  GROUP BY articles.title 
  ORDER BY num DESC 
  LIMIT 3
  """)
  posts = c.fetchall()
  db.close()
  return posts

def get_posts_author():
  """Return the top three most article author with their view counts.

    Returns:
    A list of two element tuples. Each tuple contains:
      - the name of author.
      - the number of views for his articles

    The list is sorted by number of views in descending order. Only the three
    most viewed articles are returned.
  """
  db = psycopg2.connect(database=DBNAME)
  c = db.cursor()
  c.execute("""SELECT authors.name, COUNT(log.path) AS num 
  FROM log, articles, authors 
  WHERE log.path=CONCAT('/article/',articles.slug) 
  AND articles.author=authors.id 
  GROUP BY authors.name 
  ORDER BY num DESC 
  LIMIT 3
  """)
  posts = c.fetchall()
  db.close()
  return posts
  
def get_posts_errors_days():
  """Return the top one day whith  more than 1% of requests lead to errors

    Returns:
    A list of two element tuples. Each tuple contains:
      - the day.
      - the percent of the error

    The list is sorted by percent of errors in descending order. Only the first
    most day with errors is returned.
	"""
  db = psycopg2.connect(database=DBNAME)
  c = db.cursor()
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
  posts = c.fetchall()
  db.close()
  return posts




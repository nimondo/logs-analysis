# Database code for the DB news, full solution!

import psycopg2

DBNAME = "news"

def get_posts():
  """Return all posts from the 'database', most recent first."""
  db = psycopg2.connect(database=DBNAME)
  c = db.cursor()
  c.execute("select articles.title, count(log.path) as num from log, articles where log.path=CONCAT('/article/',articles.slug) group by articles.title order by num desc limit 3")
  posts = c.fetchall()
  db.close()
  return posts

def get_posts_author():
  """Return all posts from the 'database', most recent first."""
  db = psycopg2.connect(database=DBNAME)
  c = db.cursor()
  c.execute("select authors.name, count(log.path) as num from log, articles, authors where log.path=CONCAT('/article/',articles.slug) and articles.author=authors.id group by authors.name order by num desc limit 3")
  posts = c.fetchall()
  db.close()
  return posts
  
def get_posts_errors_days():
  """Return all posts from the 'database', most recent first."""
  db = psycopg2.connect(database=DBNAME)
  c = db.cursor()
  c.execute("SELECT date_trunc('day', log.time) , CAST(tot.somme2*100 as FLOAT) / count(*) AS pourcentage FROM log INNER JOIN (SELECT date_trunc('day', time) as date2, count(log.time) as somme2 FROM log WHERE  status like '%4%' or status like '%5%' GROUP BY date_trunc('day', time)) AS tot ON (tot.date2 = date_trunc('day', time)) GROUP BY (tot.somme2,date_trunc('day', log.time)) ORDER BY pourcentage desc limit 1 ;")
  posts = c.fetchall()
  db.close()
  return posts




#!/usr/bin/env python3
# 
# A buggy web service in need of a database.

from flask import Flask, request, redirect, url_for

from newsdatadb import get_posts, get_posts_author, get_posts_errors_days

app = Flask(__name__)

@app.route('/', methods=['GET'])
def main():
    posts = ''.join("<div class=post><em class=date>{}</em>  {} views</div>".format(n,m) for n,m in get_posts())
    authors = ''.join("<div class=post><em class=date>{}</em>   {} views</div>".format(n,m) for n, m in get_posts_author())
    days = ''.join("<div class=post><em class=date>{} </em>  {}% errors</div>".format(n.strftime('%Y-%m-%d'),round(m,2)) for n,m in get_posts_errors_days())
    return """\
	<!DOCTYPE html>
	<html>
	   <head>
		<title>DB Newsdata</title>
		<link rel="stylesheet" href="{{ url_for('static', filename='app.css') }}">
		</head>
	<body>
		<h1>First Project</h1>
		<h2>{title1}</h2>
		{result1}
		<h2>{title2}</h2>
		{result2}
		<h2>{title3}</h2>
		{result3}
	</body>
</html>
		""".format(title1="The most popular three articles of all time", result1=posts,title2="The most popular article authors of all time", result2=authors,title3="The day which  more than 1% of requests lead to errors", result3=days)





if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8000)


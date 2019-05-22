#!/usr/bin/env python3
# 
# A buggy web service in need of a database.
import os
from newsdatadbt import get_result
results=get_result()
print
top_three_articles = ''.join("{} {} views \n".format(n,m) 
for n,m in results['top_three_articles'])
top_three_authors = ''.join("{} {} views \n".format(n,m) 
for n,m in results['top_three_authors'])
top_day_error = ''.join("{} {} views \n".format(n,m) 
for n,m in results['top_day_error'])
with open('results.txt', 'w') as my_results_file:
	my_results_file.write("""The most popular three articles of all time 
	\n{}\nThe most popular article authors of all time\n{}
	\nThe day with more than 1% of requests lead to errors\n{}\n
	""".format(
		top_three_articles,top_three_authors,top_day_error
	))
	my_results_file.close()

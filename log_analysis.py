#!/usr/bin/python2
# Reporting tool based on the data in the database News.

import psycopg2

DBNAME = "news"


def top_articles():
    """
    Prints top 3 most accessed articles with number of views as sorted list
    with most popular article at the top.
    """
    db = psycopg2.connect("dbname=news")
    c = db.cursor()
    c.execute("""select title, num from articles left join tops on tops.path
              like '%'||(articles.slug) order by num desc limit 3""")
    results = c.fetchall()
    print "\nMost popular three articles of all time :\n"
    for part in results:
        print "\t- \"", part[0], "\" -->", part[1], "views"
    db.close()


def top_authors():
    """
    Prints a sorted list of authors and number of views with the most popular
    author at the top
    """
    db = psycopg2.connect("dbname=news")
    c = db.cursor()
    c.execute("""select name, sum(num) as views from (articles join tops on
              tops.path like '%'||(articles.slug)) as arti left join authors
              on authors.id = arti.author group by name order by views desc""")
    results = c.fetchall()
    print "\nMost popular article authors of all time :\n"
    for part in results:
        print "\t-", part[0], "-->", part[1], "views"
    db.close()


def log_errors():
    """
    Prints the date and error percentage of days when more than 1% of requests
    lead to errors.
    """
    db = psycopg2.connect("dbname=news")
    c = db.cursor()
    c.execute("""select to_char(cast(time as date), 'Month DD, YYYY'),
              round((count(case status when '404 NOT FOUND' then 1 else null
              end)*100.0)/count(status),2) as percent from log group by
              cast(time as date) having ((count(case status when
              '404 NOT FOUND' then 1 else null end)*100.0)/count(status))>1""")
    results = c.fetchall()
    print "\nDays when more than 1% of requests lead to errors :\n"
    for part in results:
        print "\t-", part[0], "-->", part[1], "% errors"
    db.close()


top_articles()
top_authors()
log_errors()

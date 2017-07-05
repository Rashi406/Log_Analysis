#!/usr/bin/python2
# Reporting tool based on the data in the database News.

import psycopg2

DBNAME = "news"


def connect(dbname="news"):
    """
    Returns the db and cursor variables.
    """
    try:
        db = psycopg2.connect("dbname=news".format(DBNAME))
        c = db.cursor()
        return db, c
    except psycopg2.Error as e:
        print "Unable to connect to database"
        sys.exit(1)


def fetch_query(query):
    """
    Connect to the database, query, fetch results, close, return results.
    """
    db, c = connect()
    c.execute(query)
    results = c.fetchall()
    db.close()
    return results


def print_top_articles():
    """
    Fetch top articles using helper function, print results, close connection.
    """
    results = fetch_query(
	      """select title, num from articles left join tops on tops.path
              like '%'||(articles.slug) order by num desc limit 3""")
    print "\nMost popular three articles of all time :\n"
    for part in results:
        print "\t- \"", part[0], "\" -->", part[1], "views"


def print_top_authors():
    """
    Fetch top authors using helper function, print results, close connection.
    """
    results = fetch_query(
              """select name, sum(num) as views from (articles join tops on
              tops.path like '%'||(articles.slug)) as arti left join authors
              on authors.id = arti.author group by name order by views desc""")
    print "\nMost popular article authors of all time :\n"
    for part in results:
        print "\t-", part[0], "-->", part[1], "views"


def print_top_error_days():
    """
    Fetch top error days using helper function, print results, close
    connection.
    """
    results = fetch_query(
	      """select to_char(cast(time as date), 'Month DD, YYYY'),
              round((count(case status when '404 NOT FOUND' then 1 else null
              end)*100.0)/count(status),2) as percent from log group by
              cast(time as date) having ((count(case status when
              '404 NOT FOUND' then 1 else null end)*100.0)/count(status))>1""")
    print "\nDays when more than 1% of requests lead to errors :\n"
    for part in results:
        print "\t-", part[0], "-->", part[1], "% errors"


if __name__ == '__main__':
    print_top_articles()
    print_top_authors()
    print_top_error_days()

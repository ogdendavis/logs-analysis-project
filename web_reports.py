#!/usr/bin/env python

import psycopg2

DB = "news"


def report():
    # Run all reports in one easy command!
    top_articles()
    top_authors()
    high_errors()
    return


def top_articles():
    # Connect to database and activate cursor
    try:
        conn = psycopg2.connect(dbname=DB)
    except:
        print("ERROR: Unable to connect to database")
        return
    cur = conn.cursor()
    # SQL query joins articles and log where the log path matches the slug from
    # the article table. It then groups the results by the article title and
    # displays the title and number of views for the top 5 most-viewed articles
    cur.execute("""SELECT articles.title, COUNT(*) AS views
                   FROM log JOIN articles
                   ON log.path = CONCAT('/article/',articles.slug)
                   GROUP BY articles.title
                   ORDER BY views DESC LIMIT 5""")
    result = cur.fetchall()
    # Close connections to database
    cur.close()
    conn.close()
    # Format the output so that it's easy to read, including title and space
    # above and below the result. Minimum title length of 40 is sufficient in
    # this dataset to give the result as a nice readable table. If future
    # articles have longer titles, it's easy to change the '40' below to a
    # larger number.
    print("")
    print("Top articles by page views:")
    for article in result:
        print("{0:.<40} {1:,} views".format(article[0], article[1]))
    return


def top_authors():
    # Connect to database and cursor
    try:
        conn = psycopg2.connect(dbname=DB)
    except:
        print("ERROR: Unable to connect to database")
        return
    cur = conn.cursor()
    # Query joins all 3 tables by linking article slug to path in web log, and
    # linking the article's author field to the author id. The result is
    # limited to the top 5 authors (same as for top_articles), but that's
    # irrelevant in the current data set, as there are only 4 authors!
    cur.execute("""SELECT authors.name, COUNT(*) AS views
                   FROM log JOIN articles
                   ON log.path = CONCAT('/article/',articles.slug)
                       JOIN authors
                       ON articles.author = authors.id
                   GROUP BY authors.id
                   ORDER BY views DESC LIMIT 5""")
    result = cur.fetchall()
    # Close database connections
    cur.close()
    conn.close()
    # Formatting is the same as for top_articles, with shorter min length for
    # author name
    print("")
    print("Top authors by page views:")
    for author in result:
        print("{0:.<30} {1:,} views".format(author[0], author[1]))
    return


def high_errors():
    try:
        conn = psycopg2.connect(dbname=DB)
    except:
        print("ERROR: Unable to connect to database")
        return
    cur = conn.cursor()
    # I split the query into parts, to make it (slightly more) intelligible.
    # This inner query first strips down the timestamps so that they just
    # report day, month, and year, allowing us to group logs by date. Then it
    # creates two counts, one for the total requests in a day, and the other
    # for errors in that day. Finally, it groups the rows by date.
    inner_query = """SELECT
                        date_trunc('day', time) AS date,
                        COUNT(1) AS requests,
                        COUNT(CASE status WHEN '200 OK' THEN null ELSE 1 END)
                            AS errors
                    FROM log GROUP BY date"""
    # The outer query uses the inner query (above) to retrieve dates, total
    # requests, and errors. It then calculates errors as a percentage of total
    # requests and orders the results by that percentage.
    cur.execute("""SELECT
                       date,
                       CAST(errors AS float) / CAST(requests AS float)
                         AS error_rate
                   FROM ({}) AS subquery
                   ORDER BY error_rate DESC""".format(inner_query))
    result = cur.fetchall()
    cur.close()
    conn.close()
    # I failed to find a way to get the queries above to only return dates with
    # an error rate at or above 1%. I feel certain that this is an easy thing
    # to do, and that I have simply failed to figure it out. Be that as it may,
    # I know I've gotten the report down to a manageable size with this data
    # set, so I'm saying, "screw it" and doing the last filter in Python.
    the_one_percent = []
    for day in result:
        if day[1] >= 0.01:
            the_one_percent.append(day)
    print("")
    print("Days with high http error rates:")
    # Format the error rate as a readable percent, and convert the date object
    # to a string, again in a readable format.
    for day in the_one_percent:
        err_rate = day[1] * 100
        date = day[0].strftime('%Y-%m-%d')
        print("{0} - {1:.2f}%".format(date, err_rate))
    return


if __name__ == '__main__':
    report()

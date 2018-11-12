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
    conn = psycopg2.connect(dbname=DB)
    cur = conn.cursor()
    # SQL query joins articles and log where the log path matches the slug from
    # the article table. It then groups the results by the article title and
    # displays the title and number of views for the top 5 most-viewed articles
    cur.execute("select articles.title, count(*) as views from log join articles on log.path = concat('/article/',articles.slug) group by articles.title order by views desc limit 5")
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
    conn = psycopg2.connect(dbname=DB)
    cur = conn.cursor()
    # Query joins all 3 tables by linking article slug to path in web log, and
    # linking the article's author field to the author id. The result is limited
    # to the top 5 authors (same as for top_articles), but that's irrelevant in
    # the current data set, as there are only 4 authors!
    cur.execute("select authors.name, count(*) as views from log join articles on log.path = concat('/article/',articles.slug) join authors on articles.author = authors.id group by authors.id order by views desc limit 5")
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
    conn = psycopg2.connect(dbname=DB)
    cur = conn.cursor()
    # I split the query into parts, to make it (slightly more) intelligible.
    # This inner query first strips down the timestamps so that they just report
    # day, month, and year, allowing us to group logs by date. Then it creates
    # two counts, one for the total requests in a day, and the other for errors
    # in that day. Finally, it groups the rows by date.
    inner_query = "select date_trunc('day', time) as date, count(1) as requests, count(case status when '200 OK' then null else 1 end) as errors from log group by date"
    # The outer query uses the inner query (above) to retrieve dates, total
    # requests, and errors. It then calculates errors as a percentage of total
    # requests and orders the results by that percentage.
    cur.execute("select date, cast(errors as float) / cast(requests as float) as error_rate from ({}) as subquery order by error_rate desc ".format(inner_query))
    result = cur.fetchall()
    cur.close()
    conn.close()
    # I failed to find a way to get the queries above to only return dates with
    # an error rate at or above 1%. I feel certain that this is an easy thing to
    # do, and that I have simply failed to figure it out. Be that as it may, I
    # know I've gotten the report down to a manageable size with this data set,
    # so I'm saying, "screw it" and doing the last filter in Python.
    the_one_percent = []
    for day in result:
        if day[1] >= 0.01:
            the_one_percent.append(day)
    print("")
    print("Days with high http error rate:")
    # Format the error rate as a readable percent, and convert the date object
    # to a string, again in a readable format.
    for day in the_one_percent:
        err_rate = day[1] * 100
        date = day[0].strftime('%Y-%m-%d')
        print("{0} - {1:.2f}%".format(date, err_rate))
    return

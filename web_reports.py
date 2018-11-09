import psycopg2

DB = "news"

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
    print("\n")
    print("Top 5 most-viewed articles:")
    for article in result:
        print("{0:.<40} {1:,} views".format(article[0], article[1]))
    print("\n")
    return

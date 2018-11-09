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
    print("Top articles by page views:")
    for article in result:
        print("{0:.<40} {1:,} views".format(article[0], article[1]))
    print("\n")
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
    print("\n")
    print("Top authors by page views:")
    for author in result:
        print("{0:.<30} {1:,} views".format(author[0], author[1]))
    print("\n")
    return

def top_authors_by_id():
    conn = psycopg2.connect(dbname=DB)
    cur = conn.cursor()
    cur.execute("select articles.author, count(*) as views from log join articles on log.path = concat('/article/',articles.slug) group by articles.author order by views desc limit 5")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def all_authors():
    conn = psycopg2.connect(dbname=DB)
    cur = conn.cursor()
    cur.execute("select id, name from authors")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows





def articles_log_view():
    conn = psycopg2.connect(dbname=DB)
    cur = conn.cursor()
    cur.execute("select articles.title, log.path from log join articles on log.path = concat('/article/',articles.slug)")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def test():
    conn = psycopg2.connect(dbname=DB)
    cur = conn.cursor()
    cur.execute("select * from log where path like '%bad-things-gone%'")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

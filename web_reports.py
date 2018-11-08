import psycopg2

DB = "news"

def list_logs():
    conn = psycopg2.connect(dbname=DB)
    cur = conn.cursor()
    #cur.execute("select articles.slug, log.path from articles, log where log.path like '%candidate%' limit 10")
    cur.execute("select path, id, ip from log where path like '%balloon%' limit 10")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def list_articles():
    conn = psycopg2.connect(dbname=DB)
    cur = conn.cursor()
    cur.execute("select title, slug, id from articles where slug like '%balloon%' limit 10")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def popular_articles():
    conn = psycopg2.connect(dbname=DB)
    cur = conn.cursor()
    cur.execute("select article.title, count(*) from articles, log where log.path =  limit 10")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def art_log_join():
    conn = psycopg2.connect(dbname=DB)
    cur = conn.cursor()
    cur.execute("select articles.title, log.path from log join articles on log.path = concat('/article/',articles.slug) limit 10")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

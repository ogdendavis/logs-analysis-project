#!/usr/bin/env python

# This file holds helper functions I used while creating the main reports in
# web_reports

import psycopg2

DB = "news"


def top_authors_by_id():
    conn = psycopg2.connect(dbname=DB)
    cur = conn.cursor()
    cur.execute("""SELECT articles.author, COUNT(*) AS views
                   FROM log JOIN articles
                   ON log.path = CONCAT('/article/',articles.slug)
                   GROUP BY articles.author
                   ORDER BY views DESC LIMIT 5""")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def all_authors():
    conn = psycopg2.connect(dbname=DB)
    cur = conn.cursor()
    cur.execute("SELECT id, name FROM authors")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def articles_log_view():
    conn = psycopg2.connect(dbname=DB)
    cur = conn.cursor()
    cur.execute("""SELECT articles.title, log.path
                   FROM log JOIN articles
                   ON log.path = CONCAT('/article/',articles.slug)""")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def err_by_date():
    conn = psycopg2.connect(dbname=DB)
    cur = conn.cursor()
    cur.execute("""SELECT date_trunc('day', time) AS date, COUNT(*) AS errs
                   FROM log
                   WHERE status != '200 OK'
                   GROUP BY date
                   ORDER BY errs DESC""")
    result = cur.fetchall()
    cur.close()
    conn.close()
    return result

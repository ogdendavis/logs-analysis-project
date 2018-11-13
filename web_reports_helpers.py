#!/usr/bin/env python

# This file holds helper functions I used while creating the main reports in
# web_reports

import psycopg2

DB = "news"

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

def err_by_date():
    conn = psycopg2.connect(dbname=DB)
    cur = conn.cursor()
    cur.execute("select date_trunc('day', time) as date, count(*) as errs from log where status != '200 OK' group by date order by errs desc")
    result = cur.fetchall()
    cur.close()
    conn.close()
    return result

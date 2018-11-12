# Web Reports

This is a simple reporting tool that uses PostgreSQL and Python to analyze
data from a website's analytics log. The tool is run from the Python
Interpreter, and output is simply printed directly to the terminal.

## Database Structure

This tool assumes information is store in a PostgreSQL database with the
following structure:

List of relations:

Schema  |   Name   | Type  
--------|----------|-------
public  | articles | table
public  | authors  | table
public  | log      | table

Table "public.articles":

Column |           Type          
-------|--------------------------
author | integer                 
title  | text                    
slug   | text                    
lead   | text                    
body   | text                    
time   | timestamp with time zone
id     | integer                  

Table "public.authors":

Column |  Type   
-------|---------
name   | text    
bio    | text    
id     | integer

Table "public.log":

Column |           Type           
-------|--------------------------
path   | text                     
ip     | inet                     
method | text                     
status | text                     
time   | timestamp with time zone
id     | integer                  

## Insallation

To connect Web Reports to your database, execute the following command from the
folder in which you have placed the Web Reports files:

    psql -d [your database]

## Usage

Web Reports uses **PostgreSQL 9.5.14** and **Python 2.7.12**.

To execute all of the reports in Web Reports, open the Python Interpreter in
the command line and run:

```python
import web_reports as wr
wr.reports()
```

You can also run each report by itself:
```python
wr.top_articles() # Shows top 5 most-viewed articles
wr.top_authors() # Shows top 5 authors by total page views
wr.high_errors() # Shows all days with HTTP error rates >= 1% of requests
```

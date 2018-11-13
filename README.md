# Web Reports

This is a simple reporting tool that uses PostgreSQL and Python to analyze
data from a website's analytics log. The tool is run from the Python
Interpreter, and output is simply printed directly to the terminal.

## What does it do?

The main Python module of Web Reports (web_reports.py) runs three reports on a
PostgreSQL database:

* **top_articles**
  * Returns the most popular articles in the database, by total page views
* **top_authors**
  * Returns the authors who have the most total page views over all their
  articles
* **high_errors**
  * Returns all dates in which the error rate for HTTP requests is > 1%
* **report**
  * A shortcut function to run all three reports above and show their output

Comments in web_reports.py explain how each individual report works.

There is an additional module (web_reports_helpers) that contains functions
which were used in the creation of the three main reports, and are preserved
because they could prove helpful to someone who wants to poke around in the
database some more:

*Please note that all of these functions return unformatted output that may be
difficult to parse without some additional Python tweaking.*

* **top_authors_by_id**
  * Same return as top_authors, but listed by author id instead of name
* **all_authors**
  * Returns a list of all authors and their ids
* **articles_log_view**
  * WARNING: VERBOSE
  * Returns the article title and URL path for each HTTP request in the log
* **err_by_date**
  * Returns a timestamp representing a day and a count of the total HTTP errors
  on that day, sorted from most to fewest errors

Additional documents in the project are:

* **db-reference.txt**: A reference showing the database structure
* **output.txt**: Sample output from web_reports.report()
* **newsdata.sql**: SQL instructions to construct the database for this project
* **README.md**: This file. The one you're reading right now. The readme.

## Installation

To install Web Reports, simply copy the files to a folder on your system. A
minimal "install" could consist of only copying web_reports.py, as it is a
standalone module that can be used independently of the other files.

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

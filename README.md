# SQL Alchemy Database Basics Project 1

This repo shows the basics of interacting with a databae using sqlAlchemy and Python.

# Installing

## Create a virtual env and source it (windows instructions)

`python -m venv .venv`

`source .venv/Scripts/activate`

## Install Python requirements

`pip install -r requirements.txt`

## Running at command prompt

`python A_BasicsProj1.py`

## Info on DB and viewing

You can see all the tables using sqllite at terminal by running:

`sqlite3 socialDB.db`

`select * from users`

`.tables`

`.schema`

Other option is to open socialDb.db with:

https://sqlitebrowser.org/dl/

# SQL Alchemy Database Basics Project 2

## SQL Alchemy Crash Course - Master Databases in Python

https://www.youtube.com/watch?v=529LYDgRTgQ

## Run

Run the .py files starting with A_BasicProj1.py like this:

`python A_BasicProj1.py`

## Queries:

Enter sqlite3

`sqlite3 mydatabase.db`

### Seeing a printout of tables

`PRAGMA table_info(people);`

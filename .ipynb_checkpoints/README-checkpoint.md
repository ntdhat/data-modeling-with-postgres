### Date created
05/05/2020

## Analytics Database for Sparkify

### Description

The analytics team at Sparkify is particularly interested in understanding what songs users are listening to. Currently, they don't have an easy way to query their data, which resides in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

This project is for creating a new Postgres database optimized for queries on song play analysis.

### Instructions

1. Run the `create_tables.py` to create a new clean database and tables (this file should be run to reset tables before each time running ETL scripts.)
2. Run the `etl.py` to read and process song data and log data and load the data into the database's tables
3. Run your queries base on the new generated database

### Files in the project

1. `test.ipynb` displays the first few rows of each table for checking the database.
2. `create_tables.py` drops and creates tables (run this file to reset the tables before each time running ETL scripts.)
3. `etl.ipynb` reads and processes a single file from `song_data` and `log_data` and loads the data into tables. This notebook contains detailed instructions on the ETL process for each of the tables.
4. `etl.py` reads and processes files from song_data and log_data and loads them into your tables. This file can be filled out based on works in the ETL notebook.
5. `sql_queries.py` contains all sql queries, and is imported into the last three files above.

### Database schema

**Fact Table**

1. songplays - records in log data associated with song plays i.e. records with page `NextSong`
    - songplay\_id, start\_time, user\_id, level, song\_id, artist\_id, session\_id, location, user\_agent

**Dimension Tables**

2. users - users in the app
    - user\_id, first\_name, last\_name, gender, level
3. songs - songs in music database
    - song\_id, title, artist\_id, year, duration
4. artists - artists in music database
    - artist\_id, name, location, latitude, longitude
5. time - timestamps of records in songplays broken down into specific units
    - start\_time, hour, day, week, month, year, weekday

### The Datasets

The datasets consist of 2 files:

**1. Song dataset**

The first dataset consists of log files in JSON format containing metadata about a song and the artist of that song. The files are partitioned by the first three letters of each song's track ID. For example, here are filepaths to two files in this dataset.

    song_data/A/B/C/TRABCEI128F424C983.json
    song_data/A/A/B/TRAABJL12903CDCF1A.json

**2. Log dataset**

The second dataset consists of log files in JSON format. The log files are partitioned by year and month. For example, here are filepaths to two files in this dataset.

    log_data/2018/11/2018-11-12-events.json
    log_data/2018/11/2018-11-13-events.json

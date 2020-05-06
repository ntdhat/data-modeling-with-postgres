import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    """
    Process the song files and insert returned data into database's tables
    
    Args:
        (cursor)     cur      - the psycopg2 cursor object
        (str)        filepath - absolute path to the data file
    """
    # open song file
    df = pd.read_json(filepath, lines=True)

    for row in df.values:
        # insert song record
        song_data = [row[7], row[8], row[0], row[9], row[5]]
        cur.execute(song_table_insert, song_data)
    
        # insert artist record
        artist_data = [row[0], row[4], row[2], row[1], row[3]]
        cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """
    Process the log files and insert returned data into database's tables
    
    Args:
        (cursor)     cur      - the psycopg2 cursor object
        (str)        filepath - absolute path to the data file
    """
    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df[df['page'] == 'NextSong']

    # convert timestamp column to datetime
    t = pd.to_datetime(df['ts'], unit='ms')
    
    # insert time data records
    time_data = list(zip(df['ts'], t.dt.hour, t.dt.day, t.dt.weekofyear, t.dt.month, t.dt.year, t.dt.weekday))
    column_labels = ['start_time', 'hour', 'day', 'week of year', 'month', 'year', 'weekday']
    time_df = pd.DataFrame(time_data, columns=column_labels)

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[['userId', 'firstName', 'lastName', 'gender', 'level']]

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song.replace("'", "''"), row.artist.replace("'", "''"), row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = [row.ts, row.userId, row.level, songid, artistid, row.sessionId, row.location, row.userAgent]
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """
    Get the absolute path to the data files and apply data processor to the data files
    
    Args:
        (cursor)     cur      - the psycopg2 cursor object
        (connection) conn     - the psycopg2 connection object
        (str)        filepath - the relative path to the data file
        (function)   func     - the data processor
    """
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    # Initialize connection to the Postgres database and generate a cursor
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()
    
    # Process data from the 2 datasets (song data and log data) located in the local storage
    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    # Close the connection to the database
    conn.close()


if __name__ == "__main__":
    main()
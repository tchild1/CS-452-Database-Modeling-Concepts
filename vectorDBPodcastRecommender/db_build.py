## This script is used to create the tables in the database

import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()

CONNECTION = os.getenv('CONNECTION_STRING')

# need to run this to enable vector data type
CREATE_EXTENSION = 'CREATE EXTENSION IF NOT EXISTS vector'

# drop tables if exist
DROP_PODCAST_TABLE = 'DROP TABLE IF EXISTS podcast CASCADE'
DROP_SEGMENT_TABLE = 'DROP TABLE IF EXISTS podcast_segment CASCADE' 


# TODO: Add create table statement
CREATE_PODCAST_TABLE = '''
CREATE TABLE podcast (
    id VARCHAR(50) PRIMARY KEY,
    title VARCHAR(150)
)
'''

# TODO: Add create table statement
CREATE_SEGMENT_TABLE = '''
CREATE TABLE podcast_segment (
    id VARCHAR(10) PRIMARY KEY,
    podcast_id VARCHAR(50),
    start_time float,
    end_time float,
    content VARCHAR(1000),
    embedding  VECTOR(128),
    FOREIGN KEY (podcast_id) REFERENCES podcast(id)
)
'''

# TODO: Create tables with psycopg2 (example: https://www.geeksforgeeks.org/executing-sql-query-with-psycopg2-in-python/)
with psycopg2.connect(CONNECTION) as conn:
    cursor = conn.cursor()
    cursor.execute(CREATE_EXTENSION)

    cursor.execute(DROP_PODCAST_TABLE)
    cursor.execute(DROP_SEGMENT_TABLE)

    cursor.execute(CREATE_PODCAST_TABLE)
    cursor.execute(CREATE_SEGMENT_TABLE)

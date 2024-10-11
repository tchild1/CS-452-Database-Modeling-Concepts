## This script is used to insert data into the database
import os
import json
from dotenv import load_dotenv
from datasets import load_dataset
import pandas as pd
from utils import fast_pg_insert
import psycopg2

load_dotenv()


# TODO: Read the embedding files
embeddingsObjects = {}
EMBEDDINGS_DIR = 'C:/Users/child/Desktop/CS452/vectorDBPodcastRecommender/embedding'
for file in os.listdir(EMBEDDINGS_DIR):
    filePath = os.path.join(EMBEDDINGS_DIR, file)

    if os.path.isfile(filePath):
        with open(filePath, 'r', encoding='utf8') as file:
            rawText = file.read()
            for object in rawText.splitlines():
                if object.strip():
                    jsonObj = json.loads(object)
                    embeddingsObjects[jsonObj['custom_id']] = jsonObj


# TODO: Read documents files
documentsObjects = {}
DOCUMENTS_DIR = 'C:/Users/child/Desktop/CS452/vectorDBPodcastRecommender/documents'
for file in os.listdir(DOCUMENTS_DIR):
    filePath = os.path.join(DOCUMENTS_DIR, file)

    if os.path.isfile(filePath):
        with open(filePath, 'r', encoding='utf8') as file:
            rawText = file.read()
            for object in rawText.splitlines():
                if object.strip():
                    jsonObj = json.loads(object)
                    documentsObjects[jsonObj['custom_id']] = jsonObj


podcastTableData = []
for object in documentsObjects.values():

    found = False
    for podcast in podcastTableData:
        if podcast['id'] == object['body']['metadata']['podcast_id']:
            found = True
            break

    if not found:
        podcastTableData.append({
            'id': object['body']['metadata']['podcast_id'],
            'title': object['body']['metadata']['title']
        })
    
podcastTableDf = pd.DataFrame(podcastTableData)


podcastSegmentData = []
for object in embeddingsObjects.values():
    podcastSegmentData.append({
        'id': object['custom_id'],
        'podcast_id': documentsObjects[object['custom_id']]['body']['metadata']['podcast_id'],
        'start_time': documentsObjects[object['custom_id']]['body']['metadata']['start_time'],
        'end_time': documentsObjects[object['custom_id']]['body']['metadata']['stop_time'],
        'content': documentsObjects[object['custom_id']]['body']['input'],
        'embedding': object['response']['body']['data'][0]['embedding']
    })
    
podcastSegmentDf = pd.DataFrame(podcastSegmentData)


# TODO: Insert into postgres
# HINT: use the recommender.utils.fast_pg_insert function to insert data into the database
# otherwise inserting the 800k documents will take a very, very long time

CONNECTION = os.getenv('CONNECTION_STRING')

# clear tables to avoid conflict if reran
DELETE_PODCAST_TABLE = 'DELETE FROM podcast CASCADE'
DELETE_PODCAST_SEGMENT_TABLE = 'DELETE FROM podcast_segment CASCADE'


with psycopg2.connect(CONNECTION) as conn:
    cursor = conn.cursor()

    cursor.execute(DELETE_PODCAST_SEGMENT_TABLE)
    cursor.execute(DELETE_PODCAST_TABLE)

fast_pg_insert(podcastTableDf, CONNECTION, 'podcast', ['id', 'title'])
fast_pg_insert(podcastSegmentDf, CONNECTION, 'podcast_segment', ['id', 'podcast_id', 'start_time', 'end_time', 'content', 'embedding'])

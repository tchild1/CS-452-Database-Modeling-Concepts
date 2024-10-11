## This script is used to query the database
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

CONNECTION = os.getenv('CONNECTION_STRING')

# question 1
# What are the five most similar segments to segment "267:476"?
questionOneQuery = '''
SELECT P.title, PS.id, PS.content, PS.start_time, PS.end_time, PS.embedding <-> (SELECT embedding
    FROM podcast_segment as PS
    WHERE PS.id = '267:476') AS embedded_distance
FROM podcast as P
INNER JOIN podcast_segment AS PS ON P.id = PS.podcast_id
WHERE PS.id != '267:476'
ORDER BY embedded_distance
LIMIT 5
'''

# question 2
# What are the five most dissimilar segments to segment "267:476"?
questionTwoQuery = '''
SELECT P.title, PS.id, PS.content, PS.start_time, PS.end_time, PS.embedding <-> (SELECT embedding
    FROM podcast_segment as PS
    WHERE PS.id = '267:476') AS embedded_distance
FROM podcast as P
INNER JOIN podcast_segment AS PS ON P.id = PS.podcast_id
WHERE PS.id != '267:476'
ORDER BY embedded_distance DESC
LIMIT 5
'''

# question 3
# What are the five most similar segments to segment '48:511'
questionThreeQuery = '''
SELECT P.title, PS.id, PS.content, PS.start_time, PS.end_time, PS.embedding <-> (SELECT embedding
    FROM podcast_segment as PS
    WHERE PS.id = '48:511') AS embedded_distance
FROM podcast as P
INNER JOIN podcast_segment AS PS ON P.id = PS.podcast_id
WHERE PS.id != '48:511'
ORDER BY embedded_distance
LIMIT 5
'''

# question 4
# What are the five most similar segments to segment '51:56'?
questionFourQuery = '''
SELECT P.title, PS.id, PS.content, PS.start_time, PS.end_time, PS.embedding <-> (SELECT embedding
    FROM podcast_segment as PS
    WHERE PS.id = '51:56') AS embedded_distance
FROM podcast as P
INNER JOIN podcast_segment AS PS ON P.id = PS.podcast_id
WHERE PS.id != '51:56'
ORDER BY embedded_distance
LIMIT 5
'''

# question 5
# For each of the following podcast segments, 
# find the five most similar podcast episodes. 
# Hint: You can do this by averaging over the embedding vectors within a podcast episode.

# A)
questionFiveAQuery = '''
SELECT Pod.title AS title, Seg.embedding <-> Pod.embedding AS embedded_distance
FROM (
    SELECT PS.embedding as embedding
    FROM podcast_segment AS PS
    WHERE PS.id = '267:476'
) AS Seg
CROSS JOIN (
    SELECT P.title as title, AVG(PS.embedding) as embedding
    FROM podcast_segment AS PS
    INNER JOIN podcast as P on PS.podcast_id = P.id
    WHERE PS.podcast_id != (
        SELECT PS.podcast_id
        FROM podcast_segment as PS
        WHERE PS.id = '267:476'
    )
    GROUP BY P.title, PS.podcast_id
) AS Pod
ORDER BY embedded_distance
LIMIT 5
'''

# B)
questionFiveBQuery = '''
SELECT Pod.title AS title, Seg.embedding <-> Pod.embedding AS embedded_distance
FROM (
    SELECT PS.embedding as embedding
    FROM podcast_segment AS PS
    WHERE PS.id = '48:511'
) AS Seg
CROSS JOIN (
    SELECT P.title as title, AVG(PS.embedding) as embedding
    FROM podcast_segment AS PS
    INNER JOIN podcast as P on PS.podcast_id = P.id
    WHERE PS.podcast_id != (
        SELECT PS.podcast_id
        FROM podcast_segment as PS
        WHERE PS.id = '48:511'
    )
    GROUP BY P.title, PS.podcast_id
) AS Pod
ORDER BY embedded_distance
LIMIT 5
'''

# C)
questionFiveCQuery = '''
SELECT Pod.title AS title, Seg.embedding <-> Pod.embedding AS embedded_distance
FROM (
    SELECT PS.embedding as embedding
    FROM podcast_segment AS PS
    WHERE PS.id = '51:56'
) AS Seg
CROSS JOIN (
    SELECT P.title as title, AVG(PS.embedding) as embedding
    FROM podcast_segment AS PS
    INNER JOIN podcast as P on PS.podcast_id = P.id
    WHERE PS.podcast_id != (
        SELECT PS.podcast_id
        FROM podcast_segment as PS
        WHERE PS.id = '51:56'
    )
    GROUP BY P.title, PS.podcast_id
) AS Pod
ORDER BY embedded_distance
LIMIT 5
'''

# question 6
# For podcast episode id = VeH7qKZr0WI, find the five most similar podcast episodes. 
# Hint: you can do a similar averaging procedure as Q5
questionSixQuery = '''
SELECT AllPods.title AS title, Pod.embedding <-> AllPods.embedding AS embedded_distance
FROM (
    SELECT PS.embedding as embedding
    FROM podcast_segment AS PS
    INNER JOIN podcast AS P on P.id = PS.podcast_id
    WHERE P.id = 'VeH7qKZr0WI'
) AS Pod
CROSS JOIN (
    SELECT P.title as title, AVG(PS.embedding) as embedding
    FROM podcast_segment AS PS
    INNER JOIN podcast as P on PS.podcast_id = P.id
    WHERE P.id != 'VeH7qKZr0WI'
    GROUP BY P.title, P.id
) AS AllPods
ORDER BY embedded_distance
LIMIT 5
'''


with psycopg2.connect(CONNECTION) as conn:
    cursor = conn.cursor()

    cursor.execute(questionOneQuery)
    questionOneResults = cursor.fetchall()

    cursor.execute(questionTwoQuery)
    questionTwoResults = cursor.fetchall()

    cursor.execute(questionThreeQuery)
    questionThreeResults = cursor.fetchall()

    cursor.execute(questionFourQuery)
    questionFourResults = cursor.fetchall()

    cursor.execute(questionFiveAQuery)
    questionFiveAResults = cursor.fetchall()

    cursor.execute(questionFiveBQuery)
    questionFiveBResults = cursor.fetchall()

    cursor.execute(questionFiveCQuery)
    questionFiveCResults = cursor.fetchall()

    cursor.execute(questionSixQuery)
    questionSixResults = cursor.fetchall()


print('question 1:')
for row in questionOneResults:
    print(row)

print('\nquestion 2:')
for row in questionTwoResults:
    print(row)

print('\nquestion 3:')
for row in questionThreeResults:
    print(row)

print('\nquestion 4:')
for row in questionFourResults:
    print(row)

print('\nquestion 5A:')
for row in questionFiveAResults:
    print(row)

print('\nquestion 5B:')
for row in questionFiveBResults:
    print(row)

print('\nquestion 5C:')
for row in questionFiveCResults:
    print(row)

print('\nquestion 6:')
for row in questionSixResults:
    print(row)

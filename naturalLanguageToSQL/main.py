from openai import OpenAI
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
connString = os.getenv('CONNECTION_STRING')

question = 'Who spends the most amount of time in class?'

def createTables(connString):
    dropCourseTimeTable = 'DROP TABLE IF EXISTS CourseTime CASCADE'
    dropCourseTable = 'DROP TABLE IF EXISTS Course CASCADE' 
    dropStudentCourseTable = 'DROP TABLE IF EXISTS StudentCourse CASCADE'
    dropStudentTable = 'DROP TABLE IF EXISTS Student CASCADE'


    createStudentTable = '''
    CREATE TABLE Student (
        StudentId CHAR(9) PRIMARY KEY,
        FirstName VARCHAR(20),
        LastName VARCHAR(20)
    )
    '''

    createCourseTable = '''
    CREATE TABLE Course (
        CourseId int PRIMARY KEY,
        CourseName VARCHAR(50),
        CourseNumber CHAR(3),
        SectionNumber CHAR(3) 
    )
    '''

    createStudentCourseTable = '''
    CREATE TABLE StudentCourse (
        CourseId int,
        StudentId CHAR(9),
        StudentGrade VARCHAR(2),
        PRIMARY KEY (CourseId, StudentId),
        FOREIGN KEY (CourseId) REFERENCES Course(CourseId),
        FOREIGN KEY (StudentId) REFERENCES Student(StudentId)
    )
    '''

    createCourseTimeTable = '''
    CREATE TABLE CourseTime (
        CourseId int PRIMARY KEY,
        Days VARCHAR(100),
        StartTime Time,
        EndTime Time,
        FOREIGN KEY (CourseId) REFERENCES Course(CourseId)
    )
    '''



    with psycopg2.connect(connString) as conn:
        cursor = conn.cursor()
        cursor.execute(dropStudentTable)
        cursor.execute(dropCourseTable)
        cursor.execute(dropStudentCourseTable)
        cursor.execute(dropCourseTimeTable)

        cursor.execute(createStudentTable)
        cursor.execute(createCourseTable)
        cursor.execute(createStudentCourseTable)
        cursor.execute(createCourseTimeTable)

    return createStudentTable + createCourseTable + createStudentCourseTable + createCourseTimeTable

def populateTables(connString):

    populateStudentTable = '''
    INSERT INTO Student (StudentId, FirstName, LastName)
    VALUES
        ('123456789', 'John', 'Doe'),
        ('987654321', 'Jane', 'Smith'),
        ('234567890', 'Emily', 'Johnson'),
        ('345678901', 'Michael', 'Williams'),
        ('456789012', 'Sarah', 'Jones')
    '''

    populateStudentCourseTable = '''
    INSERT INTO StudentCourse (CourseId, StudentId, StudentGrade)
    VALUES
        (1, '123456789', 'A'),
        (1, '987654321', 'B'),
        (3, '987654321', 'A'),
        (2, '234567890', 'A-'),
        (3, '345678901', 'C+'),
        (4, '456789012', NULL),
        (5, '123456789', 'A'),
        (5, '234567890', 'B'),
        (2, '345678901', 'A-'),
        (3, '456789012', NULL),
        (4, '987654321', 'C');
    '''

    populateCourseTable = '''
    INSERT INTO Course (CourseId, CourseName, CourseNumber, SectionNumber)
    VALUES
        (1, 'Introduction to Programming', 'CS1', '001'),
        (2, 'Data Structures', 'CS2', '001'),
        (3, 'Database Systems', 'CS3', '001'),
        (4, 'Web Development', 'CS4', '001'),
        (5, 'Operating Systems', 'CS5', '001');
    '''

    populateCourseTimeTable = '''
    INSERT INTO CourseTime (CourseId, Days, StartTime, EndTime)
    VALUES
        (1, 'Monday, Wednesday', '09:00:00', '10:30:00'),
        (2, 'Tuesday, Thursday', '11:00:00', '12:30:00'),
        (3, 'Monday, Wednesday, Friday', '13:00:00', '14:30:00'),
        (4, 'Tuesday', '15:00:00', '16:30:00'),
        (5, 'Thursday', '17:00:00', '18:30:00')
    '''

    with psycopg2.connect(connString) as conn:
        cursor = conn.cursor()
        cursor.execute(populateStudentTable)
        cursor.execute(populateCourseTable)
        cursor.execute(populateStudentCourseTable)
        cursor.execute(populateCourseTimeTable)

        conn.commit()

def askChatGPTForSQL(question, schemaContext, shot=False):
    try:
        if shot:
            prompt = "Given this Database schema: \n" + schemaContext + "\n and this example query which retrieves the names of all students: SELECT FirstName, LastName FROM Student; Please provide me a postgres sql query that will answer my question. Question: " + question + ' Please ONLY return the sql and do not say anything else.'
        else:
            prompt = "Given this Database schema: \n" + schemaContext + "\n please provide me a postgres sql query that will answer my question. Question: " + question + ' Please ONLY return the sql and do not say anything else.'

        client: OpenAI = OpenAI()
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user", 
                    "content": prompt
                }
            ]
        )

        return completion.choices[0].message.content.replace('```', '').replace('sql', '')
    
    except:
        return 'There was an error formulating an squ query, please inform the user of this error'

def getSQLResults(sql):
    try:
        with psycopg2.connect(connString) as conn:
            cursor = conn.cursor()
            cursor.execute(sql)

            rows = cursor.fetchall()
        
        return rows

    except:
        return 'There was an error getting results for this sql query. Please inform the user of this error.'

def askChatGPTForFriendlyResponseToQuestion(question, results):

    prompt = 'A user asked this question of my database: ' + question + 'After querying for the result, this was the result from the database: ' + str(results) + ' will you please provide a friendly response kindly answering their question with the results provided? Please ONLY answer the question, but be very friendly. '
    
    client: OpenAI = OpenAI()
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user", 
                "content": prompt
            }
        ]
    )

    return completion.choices[0].message.content


schemaContext = createTables(connString)

populateTables(connString)

sql = askChatGPTForSQL(question, schemaContext, True)

print('sql:\n', sql)

results = getSQLResults(sql)

friendlyResponse = askChatGPTForFriendlyResponseToQuestion(question, results)

print(friendlyResponse)

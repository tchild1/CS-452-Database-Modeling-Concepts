**Example 1**  
Question: Can you list all students who got an A in their class?  

SQL Generated:  
SELECT S.StudentId, S.FirstName, S.LastName
FROM Student S
JOIN StudentCourse SC ON S.StudentId = SC.StudentId
WHERE SC.StudentGrade = 'A';

Friendly Response:  
Of course! Here are the students who got an A in their class:

- John Doe
- Jane Smith
- John Doe  

My thoughts:  
I think that this worked really well. I understand that the friendly response is just putting the sql response in natural language, but I wish it had recognized that John Doe didn't need to be listed twice on this list.  


**Example 2**  
Question: Can you provide a report of who has taken what classes?

SQL Generated:  
SELECT 
    s.StudentId,
    s.FirstName,
    s.LastName,
    c.CourseId,
    c.CourseName,
    c.CourseNumber,
    c.SectionNumber,
    sc.StudentGrade
FROM 
    Student s
JOIN 
    StudentCourse sc ON s.StudentId = sc.StudentId
JOIN 
    Course c ON sc.CourseId = c.CourseId;

Friendly Response:  
Sure! Here's a list of who has taken what classes:

- **John Doe** (ID: 123456789) has taken:
  - Introduction to Programming 
  - Operating Systems 

- **Jane Smith** (ID: 987654321) has taken:
  - Introduction to Programming
  - Database Systems
  - Web Development

- **Emily Johnson** (ID: 234567890) has taken:
  - Data Structures
  - Operating Systems

- **Michael Williams** (ID: 345678901) has taken:
  - Database Systems
  - Data Structures

- **Sarah Jones** (ID: 456789012) has taken:
  - Web Development
  - Database Systems

I hope this helps! Let me know if there's anything else you need. 😊


My thoughts:  
I think this is a great example. ChatGPT provided me a table with exactly the information I wanted. I also love that it put a smiley face at the end.  


**Example 3 (Single Domain)**  
What student has the best grades?
Question: What student has the best grades?

SQL Generated:  
SELECT s.FirstName, s.LastName
FROM Student s
JOIN StudentCourse sc ON s.StudentId = sc.StudentId
WHERE sc.StudentGrade = (SELECT MIN(StudentGrade) FROM StudentCourse)
LIMIT 1;

Friendly Response:  
Sure thing! The student with the best grades is John Doe. Great job, John! 😊🎓

My thoughts: I think that this question and response did well! This was a quick way to obtain the student with the best grades in a single query
 

**Example 4**  
Question: How did Mike Williams do in Web Dev?

SQL Generated:  
SELECT sc.StudentGrade
FROM StudentCourse sc
JOIN Student s ON sc.StudentId = s.StudentId
JOIN Course c ON sc.CourseId = c.CourseId
WHERE s.FirstName = 'Mike'
AND s.LastName = 'Williams'
AND c.CourseName = 'Web Dev';

Friendly Response:  
Hi there! It looks like there might not be any recorded information on Mike Williams' performance in Web Dev. If there's anything else I can assist you with, please feel free to ask!

My thoughts: In this example I tested ChatGpt's ability to recognize a nickname. I asked for Mike Williams' performance in a certain class, however, there is no 'Mike' Williams, only a Michael Williams. I wanted to see if it would try to figure this out. While it didnt figure it out, I think it made the right decision. It would have taken at least 2 queries to see that there was a Michael Williams and then it would have had to make an inference. Given only one query it is best that it only searched for a literal string


**Example 5: (Single Domain)**  
Question: Please provide the names of everyone who has gotten a B in any class?  

SQL Generated:  
SELECT DISTINCT s.FirstName, s.LastName
FROM Student s
JOIN StudentCourse sc ON s.StudentId = sc.StudentId
WHERE sc.StudentGrade = 'B';  

Friendly Response: Sure thing! The people who have received a B in any class are Emily Johnson and Jane Smith. 😊  

My Thoughts: This was a trial with single domain prompting strategy. Here I provided a basic SQL Query example within this schema to see if that would help. Honestly, I don't think it needed the example to perform well. It has done just as well on more difficult questions without an example. However, perhaps if my database was more complex it would need more of an example.  

**Example 6 (Single Domain)**  
Question: Who spends the most amount of time in class?

SQL Generated:  
SELECT s.FirstName, s.LastName
FROM Student s
JOIN StudentCourse sc ON s.StudentId = sc.StudentId
JOIN CourseTime ct ON sc.CourseId = ct.CourseId
GROUP BY s.StudentId, s.FirstName, s.LastName
ORDER BY SUM(EXTRACT(EPOCH FROM (ct.EndTime - ct.StartTime))) DESC
LIMIT 1;

Friendly Response: Sure! It looks like Jane Smith spends the most amount of time in class. 😊

My Thoughts: I think that again ChatGPT did well getting a response. However, in this case it did fail to take into account the NUMBER of days an individual is in class, it just sumed the length of each class, not considering how many days that class occurs on. My Prompt (as a single domain prompt) didn't have an example super related to calculating time, perhaps if it did it would have done a better job at makeing that distiction.
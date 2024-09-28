CREATE VIEW student_grades AS
SELECT 
    s.name, 
    c.course_name, 
    g.grade
FROM 
    students s
JOIN 
    grades g ON s.student_id = g.student_id
JOIN
    courses c ON g.course_id = c.course_id;   
    
   
CREATE VIEW good_grades AS
SELECT 
    s.name, 
    c.course_name, 
    g.grade
FROM 
    students s
JOIN 
    grades g ON s.student_id = g.student_id
JOIN
    courses c ON g.course_id = c.course_id  
WHERE g.grade > 80;  

CREATE VIEW popular_course AS
SELECT 
    course_name,
    total_num_of_students
FROM
    courses
WHERE
    total_num_of_students = (SELECT MAX(total_num_of_students)
                             FROM courses);  
                            
                            
                            
------ EXE --------------------------------------------
SELECT * FROM student_grades 
SELECT * from good_grades
SELECT * from popular_course  
                            
   
'''

מה עושה פונקציה COALESCE ?
___________________________________________________________________
The COALESCE() function returns the first non-null value in a list.

'''

'''
1.
**************************************************
---- update student number add
CREATE OR REPLACE FUNCTION update_total_students_after_insert()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE courses
    SET total_num_of_students = total_num_of_students + 1
    WHERE course_id = NEW.course_id;

    UPDATE students s
    SET
        course_avg_grades = (
            SELECT ROUND(AVG(grade)::numeric, 2)
            FROM grades g
            WHERE g.student_id = s.student_id
        ),
        num_courses = num_courses + 1
    WHERE s.student_id = NEW.student_id;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_total_students_after_insert_trigger
AFTER INSERT ON grades
FOR EACH ROW
EXECUTE FUNCTION update_total_students_after_insert();

------ EXE --------------------------------------------
INSERT INTO grades(student_id, course_id, grade) VALUES(1, 3, 75)

******************************************************
---- update student number remove
CREATE OR REPLACE FUNCTION update_total_students_after_delete()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE courses
    SET total_num_of_students = total_num_of_students - 1
    WHERE course_id = OLD.course_id;

    UPDATE students s
    SET
        course_avg_grades = (
            SELECT ROUND(AVG(grade)::numeric, 2)
            FROM grades g
            WHERE g.student_id = s.student_id
        ),
        num_courses = num_courses - 1
    WHERE s.student_id = OLD.student_id;

    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_total_students_after_delete_trigger
AFTER DELETE ON grades
FOR EACH ROW
EXECUTE FUNCTION update_total_students_after_delete();

------ EXE --------------------------------------------
DELETE FROM grades WHERE student_id = 1 AND course_id=3;

'''

'''
2.
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
**********************************************************
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
    courses c ON g.course_id = c.course_id;  
WHERE 
    g.grade > 80;          
**********************************************************
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

'''

'''
3.
CREATE OR REPLACE FUNCTION find_valedictorian(
    OUT student_name VARCHAR(100),
    OUT student_email VARCHAR(100),
    OUT student_course_avg_grades REAL,  
    OUT student_num_courses INTEGER)
language plpgsql AS
    $$
        BEGIN
            SELECT s.name, s.email, s.course_avg_grades, s.num_courses
			INTO student_name, student_email, student_course_avg_grades, student_num_courses
            FROM students s
            WHERE course_avg_grades = (SELECT MAX(course_avg_grades)
                                        FROM students);
        end;
    $$;
    
------ EXE --------------------------------------------    
select * from find_valedictorian()   

'''
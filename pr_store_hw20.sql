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
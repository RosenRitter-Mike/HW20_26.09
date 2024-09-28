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
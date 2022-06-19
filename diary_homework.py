from database import *


class DiaryHomeworkCommands(DataBase):
    def __init__(self, connection: CMySQLConnection) -> None:
        """Initialization"""
        super().__init__(connection)

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(DiaryHomeworkQueries.create_table_diary_homework_query)

        except Error as e:
            print(e)
        

class DiaryHomeworkQueries:
    create_table_diary_homework_query = """CREATE TABLE IF NOT EXISTS diaryhomework(
        classroom_id INT,
        FOREIGN KEY (classroom_id) REFERENCES Classroom (classroom_id) ON DELETE CASCADE,
        
        standard_diary_week_current_lesson1 VARCHAR(40),
        standard_diary_week_current_lesson2 VARCHAR(40),
        standard_diary_week_current_lesson3 VARCHAR(40),
        standard_diary_week_current_lesson4 VARCHAR(40),
        standard_diary_week_current_lesson5 VARCHAR(40),
        standard_diary_week_current_lesson6 VARCHAR(40),
        standard_diary_week_current_lesson7 VARCHAR(40),
        standard_diary_week_current_lesson8 VARCHAR(40),
        standard_diary_week_current_lesson9 VARCHAR(40),
        standard_diary_week_current_lesson10 VARCHAR(40),
        standard_diary_week_current_lesson11 VARCHAR(40),
        standard_diary_week_current_lesson12 VARCHAR(40),
        
        standard_diary_week_next_lesson1 VARCHAR(40),
        standard_diary_week_next_lesson2 VARCHAR(40),
        standard_diary_week_next_lesson3 VARCHAR(40),
        standard_diary_week_next_lesson4 VARCHAR(40),
        standard_diary_week_next_lesson5 VARCHAR(40),
        standard_diary_week_next_lesson6 VARCHAR(40),
        standard_diary_week_next_lesson7 VARCHAR(40),
        standard_diary_week_next_lesson8 VARCHAR(40),
        standard_diary_week_next_lesson9 VARCHAR(40),
        standard_diary_week_next_lesson10 VARCHAR(40),
        standard_diary_week_next_lesson11 VARCHAR(40),
        standard_diary_week_next_lesson12 VARCHAR(40),
        
        current_diary_week_current_lesson1 VARCHAR(40),
        current_diary_week_current_lesson2 VARCHAR(40),
        current_diary_week_current_lesson3 VARCHAR(40),
        current_diary_week_current_lesson4 VARCHAR(40),
        current_diary_week_current_lesson5 VARCHAR(40),
        current_diary_week_current_lesson6 VARCHAR(40),
        current_diary_week_current_lesson7 VARCHAR(40),
        current_diary_week_current_lesson8 VARCHAR(40),
        current_diary_week_current_lesson9 VARCHAR(40),
        current_diary_week_current_lesson10 VARCHAR(40),
        current_diary_week_current_lesson11 VARCHAR(40),
        current_diary_week_current_lesson12 VARCHAR(40),
        
        current_diary_week_next_lesson1 VARCHAR(40),
        current_diary_week_next_lesson2 VARCHAR(40),
        current_diary_week_next_lesson3 VARCHAR(40),
        current_diary_week_next_lesson4 VARCHAR(40),
        current_diary_week_next_lesson5 VARCHAR(40),
        current_diary_week_next_lesson6 VARCHAR(40),
        current_diary_week_next_lesson7 VARCHAR(40),
        current_diary_week_next_lesson8 VARCHAR(40),
        current_diary_week_next_lesson9 VARCHAR(40),
        current_diary_week_next_lesson10 VARCHAR(40),
        current_diary_week_next_lesson11 VARCHAR(40),
        current_diary_week_next_lesson12 VARCHAR(40),
        
        next_diary_week_current_lesson1 VARCHAR(40),
        next_diary_week_current_lesson2 VARCHAR(40),
        next_diary_week_current_lesson3 VARCHAR(40),
        next_diary_week_current_lesson4 VARCHAR(40),
        next_diary_week_current_lesson5 VARCHAR(40),
        next_diary_week_current_lesson6 VARCHAR(40),
        next_diary_week_current_lesson7 VARCHAR(40),
        next_diary_week_current_lesson8 VARCHAR(40),
        next_diary_week_current_lesson9 VARCHAR(40),
        next_diary_week_current_lesson10 VARCHAR(40),
        next_diary_week_current_lesson11 VARCHAR(40),
        next_diary_week_current_lesson12 VARCHAR(40),
        
        next_diary_week_next_lesson1 VARCHAR(40),
        next_diary_week_next_lesson2 VARCHAR(40),
        next_diary_week_next_lesson3 VARCHAR(40),
        next_diary_week_next_lesson4 VARCHAR(40),
        next_diary_week_next_lesson5 VARCHAR(40),
        next_diary_week_next_lesson6 VARCHAR(40),
        next_diary_week_next_lesson7 VARCHAR(40),
        next_diary_week_next_lesson8 VARCHAR(40),
        next_diary_week_next_lesson9 VARCHAR(40),
        next_diary_week_next_lesson10 VARCHAR(40),
        next_diary_week_next_lesson11 VARCHAR(40),
        next_diary_week_next_lesson12 VARCHAR(40)
    )"""
    

if __name__ == '__main__':
    connection = connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=DATABASE_NAME
    )

    diary_homework_db = DiaryHomeworkCommands(connection)

from database import *


class DiaryHomeworkCommands(DataBase):
    def __init__(self, connection: CMySQLConnection) -> None:
        """Initialization"""
        super().__init__(connection)

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(DiaryHomeworkQueries.create_table_diary_standard_week_query)
                cursor.execute(DiaryHomeworkQueries.create_table_diary_current_week_query)
                cursor.execute(DiaryHomeworkQueries.create_table_diary_next_week_query)

        except Error as e:
            print(e)

    def insert_classroom_id(self, classroom_id: int) -> None:
        """Inserts classroom_id into the tables"""
        with self.connection.cursor() as cursor:
            cursor.execute(DiaryHomeworkQueries.insert_classroom_id_standard_week_query.format(classroom_id))
            cursor.execute(DiaryHomeworkQueries.insert_classroom_id_current_week_query.format(classroom_id))
            cursor.execute(DiaryHomeworkQueries.insert_classroom_id_next_week_query.format(classroom_id))
            self.connection.commit()
        

class DiaryHomeworkQueries:
    create_table_diary_standard_week_query = """CREATE TABLE IF NOT EXISTS diary_standard_week(
        classroom_id INT,
        FOREIGN KEY (classroom_id) REFERENCES Classroom (classroom_id) ON DELETE CASCADE,
        
        monday_lesson1 TEXT,
        monday_lesson2 TEXT,
        monday_lesson3 TEXT,
        monday_lesson4 TEXT,
        monday_lesson5 TEXT,
        monday_lesson6 TEXT,
        monday_lesson7 TEXT,
        monday_lesson8 TEXT,
        monday_lesson9 TEXT,
        monday_lesson10 TEXT,
        monday_lesson11 TEXT,
        monday_lesson12 TEXT,
        
        tuesday_lesson1 TEXT,
        tuesday_lesson2 TEXT,
        tuesday_lesson3 TEXT,
        tuesday_lesson4 TEXT,
        tuesday_lesson5 TEXT,
        tuesday_lesson6 TEXT,
        tuesday_lesson7 TEXT,
        tuesday_lesson8 TEXT,
        tuesday_lesson9 TEXT,
        tuesday_lesson10 TEXT,
        tuesday_lesson11 TEXT,
        tuesday_lesson12 TEXT,
        
        wednesday_lesson1 TEXT,
        wednesday_lesson2 TEXT,
        wednesday_lesson3 TEXT,
        wednesday_lesson4 TEXT,
        wednesday_lesson5 TEXT,
        wednesday_lesson6 TEXT,
        wednesday_lesson7 TEXT,
        wednesday_lesson8 TEXT,
        wednesday_lesson9 TEXT,
        wednesday_lesson10 TEXT,
        wednesday_lesson11 TEXT,
        wednesday_lesson12 TEXT,
        
        thursday_lesson1 TEXT,
        thursday_lesson2 TEXT,
        thursday_lesson3 TEXT,
        thursday_lesson4 TEXT,
        thursday_lesson5 TEXT,
        thursday_lesson6 TEXT,
        thursday_lesson7 TEXT,
        thursday_lesson8 TEXT,
        thursday_lesson9 TEXT,
        thursday_lesson10 TEXT,
        thursday_lesson11 TEXT,
        thursday_lesson12 TEXT,
        
        friday_lesson1 TEXT,
        friday_lesson2 TEXT,
        friday_lesson3 TEXT,
        friday_lesson4 TEXT,
        friday_lesson5 TEXT,
        friday_lesson6 TEXT,
        friday_lesson7 TEXT,
        friday_lesson8 TEXT,
        friday_lesson9 TEXT,
        friday_lesson10 TEXT,
        friday_lesson11 TEXT,
        friday_lesson12 TEXT,
        
        saturday_lesson1 TEXT,
        saturday_lesson2 TEXT,
        saturday_lesson3 TEXT,
        saturday_lesson4 TEXT,
        saturday_lesson5 TEXT,
        saturday_lesson6 TEXT,
        saturday_lesson7 TEXT,
        saturday_lesson8 TEXT,
        saturday_lesson9 TEXT,
        saturday_lesson10 TEXT,
        saturday_lesson11 TEXT,
        saturday_lesson12 TEXT,
        
        sunday_lesson1 TEXT,
        sunday_lesson2 TEXT,
        sunday_lesson3 TEXT,
        sunday_lesson4 TEXT,
        sunday_lesson5 TEXT,
        sunday_lesson6 TEXT,
        sunday_lesson7 TEXT,
        sunday_lesson8 TEXT,
        sunday_lesson9 TEXT,
        sunday_lesson10 TEXT,
        sunday_lesson11 TEXT,
        sunday_lesson12 TEXT
    )"""

    create_table_diary_current_week_query = """CREATE TABLE IF NOT EXISTS diary_current_week(
        classroom_id INT,
        FOREIGN KEY (classroom_id) REFERENCES Classroom (classroom_id) ON DELETE CASCADE,   
        
        monday_lesson1 TEXT,
        monday_lesson2 TEXT,
        monday_lesson3 TEXT,
        monday_lesson4 TEXT,
        monday_lesson5 TEXT,
        monday_lesson6 TEXT,
        monday_lesson7 TEXT,
        monday_lesson8 TEXT,
        monday_lesson9 TEXT,
        monday_lesson10 TEXT,
        monday_lesson11 TEXT,
        monday_lesson12 TEXT,
        
        tuesday_lesson1 TEXT,
        tuesday_lesson2 TEXT,
        tuesday_lesson3 TEXT,
        tuesday_lesson4 TEXT,
        tuesday_lesson5 TEXT,
        tuesday_lesson6 TEXT,
        tuesday_lesson7 TEXT,
        tuesday_lesson8 TEXT,
        tuesday_lesson9 TEXT,
        tuesday_lesson10 TEXT,
        tuesday_lesson11 TEXT,
        tuesday_lesson12 TEXT,
        
        wednesday_lesson1 TEXT,
        wednesday_lesson2 TEXT,
        wednesday_lesson3 TEXT,
        wednesday_lesson4 TEXT,
        wednesday_lesson5 TEXT,
        wednesday_lesson6 TEXT,
        wednesday_lesson7 TEXT,
        wednesday_lesson8 TEXT,
        wednesday_lesson9 TEXT,
        wednesday_lesson10 TEXT,
        wednesday_lesson11 TEXT,
        wednesday_lesson12 TEXT,
        
        thursday_lesson1 TEXT,
        thursday_lesson2 TEXT,
        thursday_lesson3 TEXT,
        thursday_lesson4 TEXT,
        thursday_lesson5 TEXT,
        thursday_lesson6 TEXT,
        thursday_lesson7 TEXT,
        thursday_lesson8 TEXT,
        thursday_lesson9 TEXT,
        thursday_lesson10 TEXT,
        thursday_lesson11 TEXT,
        thursday_lesson12 TEXT,
        
        friday_lesson1 TEXT,
        friday_lesson2 TEXT,
        friday_lesson3 TEXT,
        friday_lesson4 TEXT,
        friday_lesson5 TEXT,
        friday_lesson6 TEXT,
        friday_lesson7 TEXT,
        friday_lesson8 TEXT,
        friday_lesson9 TEXT,
        friday_lesson10 TEXT,
        friday_lesson11 TEXT,
        friday_lesson12 TEXT,
        
        saturday_lesson1 TEXT,
        saturday_lesson2 TEXT,
        saturday_lesson3 TEXT,
        saturday_lesson4 TEXT,
        saturday_lesson5 TEXT,
        saturday_lesson6 TEXT,
        saturday_lesson7 TEXT,
        saturday_lesson8 TEXT,
        saturday_lesson9 TEXT,
        saturday_lesson10 TEXT,
        saturday_lesson11 TEXT,
        saturday_lesson12 TEXT,
        
        sunday_lesson1 TEXT,
        sunday_lesson2 TEXT,
        sunday_lesson3 TEXT,
        sunday_lesson4 TEXT,
        sunday_lesson5 TEXT,
        sunday_lesson6 TEXT,
        sunday_lesson7 TEXT,
        sunday_lesson8 TEXT,
        sunday_lesson9 TEXT,
        sunday_lesson10 TEXT,
        sunday_lesson11 TEXT,
        sunday_lesson12 TEXT
    )"""

    create_table_diary_next_week_query = """CREATE TABLE IF NOT EXISTS diary_next_week(
        classroom_id INT,
        FOREIGN KEY (classroom_id) REFERENCES Classroom (classroom_id) ON DELETE CASCADE,
        
        monday_lesson1 TEXT,
        monday_lesson2 TEXT,
        monday_lesson3 TEXT,
        monday_lesson4 TEXT,
        monday_lesson5 TEXT,
        monday_lesson6 TEXT,
        monday_lesson7 TEXT,
        monday_lesson8 TEXT,
        monday_lesson9 TEXT,
        monday_lesson10 TEXT,
        monday_lesson11 TEXT,
        monday_lesson12 TEXT,
        
        tuesday_lesson1 TEXT,
        tuesday_lesson2 TEXT,
        tuesday_lesson3 TEXT,
        tuesday_lesson4 TEXT,
        tuesday_lesson5 TEXT,
        tuesday_lesson6 TEXT,
        tuesday_lesson7 TEXT,
        tuesday_lesson8 TEXT,
        tuesday_lesson9 TEXT,
        tuesday_lesson10 TEXT,
        tuesday_lesson11 TEXT,
        tuesday_lesson12 TEXT,
        
        wednesday_lesson1 TEXT,
        wednesday_lesson2 TEXT,
        wednesday_lesson3 TEXT,
        wednesday_lesson4 TEXT,
        wednesday_lesson5 TEXT,
        wednesday_lesson6 TEXT,
        wednesday_lesson7 TEXT,
        wednesday_lesson8 TEXT,
        wednesday_lesson9 TEXT,
        wednesday_lesson10 TEXT,
        wednesday_lesson11 TEXT,
        wednesday_lesson12 TEXT,
        
        thursday_lesson1 TEXT,
        thursday_lesson2 TEXT,
        thursday_lesson3 TEXT,
        thursday_lesson4 TEXT,
        thursday_lesson5 TEXT,
        thursday_lesson6 TEXT,
        thursday_lesson7 TEXT,
        thursday_lesson8 TEXT,
        thursday_lesson9 TEXT,
        thursday_lesson10 TEXT,
        thursday_lesson11 TEXT,
        thursday_lesson12 TEXT,
        
        friday_lesson1 TEXT,
        friday_lesson2 TEXT,
        friday_lesson3 TEXT,
        friday_lesson4 TEXT,
        friday_lesson5 TEXT,
        friday_lesson6 TEXT,
        friday_lesson7 TEXT,
        friday_lesson8 TEXT,
        friday_lesson9 TEXT,
        friday_lesson10 TEXT,
        friday_lesson11 TEXT,
        friday_lesson12 TEXT,
        
        saturday_lesson1 TEXT,
        saturday_lesson2 TEXT,
        saturday_lesson3 TEXT,
        saturday_lesson4 TEXT,
        saturday_lesson5 TEXT,
        saturday_lesson6 TEXT,
        saturday_lesson7 TEXT,
        saturday_lesson8 TEXT,
        saturday_lesson9 TEXT,
        saturday_lesson10 TEXT,
        saturday_lesson11 TEXT,
        saturday_lesson12 TEXT,
        
        sunday_lesson1 TEXT,
        sunday_lesson2 TEXT,
        sunday_lesson3 TEXT,
        sunday_lesson4 TEXT,
        sunday_lesson5 TEXT,
        sunday_lesson6 TEXT,
        sunday_lesson7 TEXT,
        sunday_lesson8 TEXT,
        sunday_lesson9 TEXT,
        sunday_lesson10 TEXT,
        sunday_lesson11 TEXT,
        sunday_lesson12 TEXT
    )"""

    insert_classroom_id_standard_week_query = "INSERT into diary_standard_week (classroom_id) VALUES({})"
    insert_classroom_id_current_week_query = "INSERT into diary_current_week (classroom_id) VALUES({})"
    insert_classroom_id_next_week_query = "INSERT into diary_next_week (classroom_id) VALUES({})"


if __name__ == '__main__':
    connection = connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=DATABASE_NAME
    )

    diary_homework_db = DiaryHomeworkCommands(connection)
    # diary_homework_db.insert_classroom_id(2)

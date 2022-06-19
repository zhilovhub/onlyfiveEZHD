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

    def get_all_days_from_standard_week(self, classroom_id: int) -> list:
        """Gets everyday diary from standard week"""
        with self.connection.cursor() as cursor:
            cursor.execute(DiaryHomeworkQueries.get_all_days_from_standard_week_query.format(classroom_id))
            all_lessons = cursor.fetchone()[1:]

        return all_lessons

    def get_all_days_from_current_week(self, classroom_id: int) -> list:
        """Gets everyday diary from current week"""
        with self.connection.cursor() as cursor:
            cursor.execute(DiaryHomeworkQueries.get_all_days_from_current_week_query.format(classroom_id))
            all_lessons = cursor.fetchone()[1:]

        return all_lessons

    def get_all_days_from_next_week(self, classroom_id: int) -> list:
        """Gets everyday diary from next week"""
        with self.connection.cursor() as cursor:
            cursor.execute(DiaryHomeworkQueries.get_all_days_from_next_week_query.format(classroom_id))
            all_lessons = cursor.fetchone()[1:]

        return all_lessons

    def insert_classroom_id(self, classroom_id: int) -> None:
        """Inserts classroom_id into the tables"""
        with self.connection.cursor() as cursor:
            cursor.execute(DiaryHomeworkQueries.insert_classroom_id_standard_week_query.format(classroom_id))
            cursor.execute(DiaryHomeworkQueries.insert_classroom_id_current_week_query.format(classroom_id))
            cursor.execute(DiaryHomeworkQueries.insert_classroom_id_next_week_query.format(classroom_id))
            self.connection.commit()
        

class DiaryHomeworkQueries:
    @staticmethod
    def create_get_weekday_query(weekday: str, table_name: str) -> str:
        """Creates get_weekday query"""
        template = """SELECT 
                        weekday_lesson1,
                        weekday_lesson2,
                        weekday_lesson3,
                        weekday_lesson4,
                        weekday_lesson5,
                        weekday_lesson6,
                        weekday_lesson7,
                        weekday_lesson8,
                        weekday_lesson9,
                        weekday_lesson10,
                        weekday_lesson11,
                        weekday_lesson12
                      FROM table_name WHERE classroom_id={}"""
        return template.replace("weekday", weekday).replace("table_name", table_name)
    
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

    get_all_days_from_standard_week_query = """SELECT * FROM diary_standard_week WHERE classroom_id={}"""
    get_all_days_from_current_week_query = """SELECT * FROM diary_current_week WHERE classroom_id={}"""
    get_all_days_from_next_week_query = """SELECT * FROM diary_next_week WHERE classroom_id={}"""

    get_monday_from_standard_week_query = create_get_weekday_query("monday", "diary_standard_week")
    get_tuesday_from_standard_week_query = create_get_weekday_query("tuesday", "diary_standard_week")
    get_wednesday_from_standard_week_query = create_get_weekday_query("wednesday", "diary_standard_week")
    get_thursday_from_standard_week_query = create_get_weekday_query("thursday", "diary_standard_week")
    get_friday_from_standard_week_query = create_get_weekday_query("friday", "diary_standard_week")
    get_saturday_from_standard_week_query = create_get_weekday_query("saturday", "diary_standard_week")
    get_sunday_from_standard_week_query = create_get_weekday_query("sunday", "diary_standard_week")

    get_monday_from_current_week_query = create_get_weekday_query("monday", "diary_current_week")
    get_tuesday_from_current_week_query = create_get_weekday_query("tuesday", "diary_current_week")
    get_wednesday_from_current_week_query = create_get_weekday_query("wednesday", "diary_current_week")
    get_thursday_from_current_week_query = create_get_weekday_query("thursday", "diary_current_week")
    get_friday_from_current_week_query = create_get_weekday_query("friday", "diary_current_week")
    get_saturday_from_current_week_query = create_get_weekday_query("saturday", "diary_current_week")
    get_sunday_from_current_week_query = create_get_weekday_query("sunday", "diary_current_week")

    get_monday_from_next_week_query = create_get_weekday_query("monday", "diary_next_week")
    get_tuesday_from_next_week_query = create_get_weekday_query("tuesday", "diary_next_week")
    get_wednesday_from_next_week_query = create_get_weekday_query("wednesday", "diary_next_week")
    get_thursday_from_next_week_query = create_get_weekday_query("thursday", "diary_next_week")
    get_friday_from_next_week_query = create_get_weekday_query("friday", "diary_next_week")
    get_saturday_from_next_week_query = create_get_weekday_query("saturday", "diary_next_week")
    get_sunday_from_next_week_query = create_get_weekday_query("sunday", "diary_next_week")

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
    # diary_homework_db.insert_classroom_id(3)
    print(diary_homework_db.get_all_days_from_standard_week(3))
    print(diary_homework_db.get_all_days_from_standard_week(3))
